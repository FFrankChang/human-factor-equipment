'''
(c) 2023 Twente Medical Systems International B.V., Oldenzaal The Netherlands

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#######  #     #   #####   #
   #     ##   ##  #        
   #     # # # #  #        #
   #     #  #  #   #####   #
   #     #     #        #  #
   #     #     #        #  #
   #     #     #  #####    #

/**
 * @file ${experiment_psychopy.py} 
 * @brief This file shows how to define an auditory oddball PsychoPy experiment,
 * and how to set up threads to simultaneously send triggers via the USB TTL module
 * and give auditory stimuli to the subject
 *
 */


'''

from psychopy import sound
from numpy.random import choice
# import random
import numpy as np
from PySide2 import  QtGui, QtCore, QtWidgets
from PySide2.QtCore import Qt
import time

import sys
from os.path import join, dirname, realpath, normpath, exists
Plugins_dir = dirname(realpath(__file__)) # directory of this file
measurements_dir = join(Plugins_dir, '../measurements') # directory with all measurements
modules_dir = normpath(join(Plugins_dir, '../')) # directory with all modules

from TMSiPlugins.external_devices.usb_ttl_device import USB_TTL_device, TTLError


class PsychopyExperimentSetup():
    """ A class that sets up the experiment properties based on the PsychoPy
        library and initializes the trigger setup for an oddball experiment
    """
    
    def __init__(self, TMSiDevice, COM_port, n_trials, target_value, nontarget_value, interval = 3, probability = 0.5, duration = 0.3):
        """ 
            Setting up the initial variables for an oddball auditory PsychoPy experiment
            with simultaneous triggers to TMSi SAGA or APEX
            
            Parameters (required)
                TMSiDevice: USB TTL module is TMSi-device specific. Please enter the 
                               desired device in the paramters ("SAGA" or "APEX")
                COM_port: define the port on the computer where the TTL module was installed   
                n_trials: define the number of stimuli that must be given to the participant
                target_value: define the value of the trigger for the target stimuli
                nontarget_value: define the value of the trigger for the non-target stimuli
                
            Parameters (optional):
                interval: define time interval between stimuli, defaults to 3 s
                duration: define length of trigger that is stored in TMSiDevice, defaults to 0.3 s
                probability: define the ratio between target/nontarget stimuli, defaults to 0.5 s
        """
        
        # Set trigger values for target and nontarget stimuli
        self.target_value = target_value
        self.nontarget_value = nontarget_value
        
        # if no probability parameter is given, set target/nontarget ratio 50/50.
        self.probability_target = probability
        self.probability_nontarget = 1-self.probability_target
        
        # if no duration argument is given, duration of trigger defaults to 0.3 s
        self.duration = duration
        
        # if  no interval argument is given, interval between stimuli defaults to 3 s
        self.interval = interval

        # Number of trials defined by user
        self.n_trials = n_trials
        
        # Conditions for the oddball paradigm
        self.conditions = ['non-target', 'target']
        
        # Set up the blackbox TTL module. Throw an error if module was not found correctly
        try:
            # TMSiDevice is SAGA or APEX
            self.ttl_module = USB_TTL_device(TMSiDevice, com_port = COM_port)
        except TTLError:
            raise TTLError("No trigger event cable is found")
        time.sleep(0.5)
        
        # Set target and nontarget trigger variables for the threads
        self.target = False
        self.nontarget = False
        self.target_cue = False
        self.nontarget_cue = False
        
        # Set up the experiment variables
        self.setupExperiment()
        
        # Set up threads for the stimuli and the ttl module
        self.setupThreads()
            
        
    def setupThreads(self):
        """ Set up the threads to send triggers and cues simoultaneously
        """
        # Create thread to send signal to SAGA/APEX
        self.thread_triggers = QtCore.QThread()
        
        # Create thread to perform the cues of the oddball 
        self.thread_play_cues = QtCore.QThread()
    
        # Instantiate the writing triggers class
        self.worker_triggers = triggerThread(self)
        
        # Instantiate the cue class
        self.worker_play_cues = cueThread(self)
    
        # Move the workers to Thread
        self.worker_triggers.moveToThread(self.thread_triggers)
        self.worker_play_cues.moveToThread(self.thread_play_cues)
        
        # Connect signals to slots of function that should start running
        self.thread_triggers.started.connect(self.worker_triggers.writeTrigger)
        self.thread_play_cues.started.connect(self.worker_play_cues.giveCue)
    
    def startThreads(self):
        """ Function to start the threads
        """
        self.thread_triggers.start()
        self.thread_play_cues.start()
        
    def stopThreads(self):
        """ Function to stop the threads
        """
        # Stop saga/apex triggers thread
        self.worker_triggers.stop()
        self.thread_triggers.quit()
        self.thread_triggers.wait()
        
        # Stop giving cues thread
        self.worker_play_cues.stop()
        self.thread_play_cues.quit()
        self.thread_play_cues.wait()

        
    def setupExperiment(self):
        """ Function to set up the cues of the (auditory) experiment
        """
        
        # Non-target sound
        self.non_target_sound = sound.Sound(value="A", secs=self.duration)
        
        # Target sound
        self.target_sound = sound.Sound(value="B", secs=self.duration)
    
    def runExperiment(self):
        """ Run the auditory oddball experiment with triggers and cues
        """
        # Start threads
        self.startThreads()
        # Wait for the threads to start
        time.sleep(0.1)
        # Perform the experiment with the different cues
        for i in range(self.n_trials):
            # Empty & initialize the con variable
            con = []
            # Define the con variable: a target or a non-target cue
            con = choice(self.conditions, 1, p = [self.probability_nontarget, self.probability_target])
            if con[0] == 'non-target':
                # Give non-target cue & write non-target value
                self.writeTriggerNontarget()
            elif con[0] == 'target':
                # Give target cue & write target value
                self.writeTriggerTarget()
            # After the stimulus, wait for a predefined amount of time
            time.sleep(self.interval)
        # When the experiment is done, wait for a bit
        time.sleep(0.5)
        
        # Kill the threads
        self.stopThreads()
        
        # Close the serial port of the TTL modle
        self.ttl_module.close()
        
        # Notify the researcher that the experiment is done
        print('Experiment is done, all trials are performed')

    
    def writeTriggerTarget(self):
        # Send signal to the trigger thread to write a target trigger to TMSi device
        self.worker_triggers.target = True
        # Send signal to cue thread to play target sound
        self.worker_play_cues.target_cue = True
        
        
    def writeTriggerNontarget(self):
        # Send signal to the trigger thread to write a nontarget trigger to TMSi device
        self.worker_triggers.nontarget = True
        # Send signal to cue thread to play a nontarget sound
        self.worker_play_cues.nontarget_cue = True
        
        



class triggerThread((QtCore.QObject)):
    """  Class to write triggers to the TMSi device when a signal from the main thread is given
    """
    def __init__(self, main_class):
        """ Set up the initial variables based on the main class of the experiment

        """
        QtCore.QObject.__init__(self)
        
        self.target = main_class.target
        self.nontarget = main_class.nontarget
        # Define a variable to keep the thread running
        self.triggering = True
        # Get variables from the main class
        self.ttl_module = main_class.ttl_module
        self.target_value = main_class.target_value
        self.nontarget_value = main_class.nontarget_value

    @QtCore.Slot()
    def writeTrigger(self):
        while self.triggering:
            if self.target == True:
                # Write trigger target
                self.ttl_module.write_trigger(trigger_value = self.target_value, duration = 0.2)
                # Stop writing trigger target
                self.target = False
            elif self.nontarget == True:
                # Write non trigger target
                self.ttl_module.write_trigger(trigger_value = self.nontarget_value, duration = 0.2)
                # Stop writing non trigger target
                self.nontarget = False
            # Put some time to perform the actions
            time.sleep(0.0001)
                
    def stop(self):
        """ Method that is executed when the thread is terminated. 
            This stop event stops the triggers.
        """
        self.triggering = False


class cueThread((QtCore.QObject)):
    """  Class to perform the cues on the computer
    """
    def __init__(self, main_class):
        QtCore.QObject.__init__(self)
        
        self.target_cue = main_class.target_cue
        self.nontarget_cue = main_class.nontarget_cue
        self.duration = main_class.duration
        self.non_target_sound = main_class.non_target_sound
        self.target_sound = main_class.target_sound
        # Set up variable to keep the thread running
        self.triggering = True 

    @QtCore.Slot()
    def giveCue(self):
        """ Function to give the auditory cues on the computer based on the 
        input of the main thread

        """
        while self.triggering:
            if self.target_cue == True:
                # Play target sound
                self.target_sound.play()
                time.sleep(self.duration)
                # Stop target sound
                self.target_sound.stop()
                # Make variable false again
                self.target_cue = False
            elif self.nontarget_cue == True:
                # Play nontarget sound
                self.non_target_sound.play()
                time.sleep(self.duration)
                # Stop nontarget sound
                self.non_target_sound.stop()
                # Make variable false again
                self.nontarget_cue = False
            time.sleep(0.0001)
                
    def stop(self):
        """ Method that is executed when the thread is terminated. 
            This stop event stops the cues.
        """
        self.triggering = False

