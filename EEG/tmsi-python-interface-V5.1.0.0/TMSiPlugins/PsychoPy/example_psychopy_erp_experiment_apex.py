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
 * @file ${example_psychopy_erp_experiment_apex.py} 
 * @brief This example shows how to combine sending triggers to APEX with running a 
 * pre-coded experiment with PsychoPy with the TTL trigger module
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Plugin_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Plugin_dir, '..', '..') # directory with all modules
measurements_dir = join(Plugin_dir, '../../measurements') # directory with all measurements
configs_dir = join(Plugin_dir, '../../TMSiSDK\\tmsi_resources') # directory with configurations
sys.path.append(modules_dir)
import os
from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable

from PySide2.QtWidgets import *
from TMSiGui.gui import Gui
from TMSiPlotterHelpers.impedance_plotter_helper import ImpedancePlotterHelper
from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper
from TMSiFileFormats.file_writer import FileWriter, FileFormat
from experiment_psychopy import PsychopyExperimentSetup
from TMSiPlugins.external_devices.usb_ttl_device import TTLError
import time
from threading import Thread

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(DeviceType.apex, DeviceInterfaceType.bluetooth)
    dongle = TMSiSDK().get_dongle_list(DeviceType.apex)[0]
    discoveryList = TMSiSDK().get_device_list(DeviceType.apex)

    # Set up device
    if (len(discoveryList) > 0):
        # Get the handle to the paired device.
        for i, dev_i in enumerate(discoveryList):
            if dev_i.get_dongle_serial_number() == dongle.get_serial_number():
                dev_id = i   
        dev = discoveryList[dev_id]
        
        # Open a connection to the APEX-system
        dev.open(dongle_id = dongle.get_id())
        
        # Load the EEG channel set and configuration (in this case for 32 channels)
        print("load EEG config")
        dev.import_configuration(join(configs_dir, 'APEX_config_EEG32.xml'))
        
    
        # Initialize PsychoPy Experiment, for arguments description see class
        print('\n Initializing PsychoPy experiment and TTL module \n')
        print('\n  Please check if red and green LEDs are turned on ... \n')
        # !! NOTE: Available options for the (non)target_value inputs are all EVEN numbers between 2 and 30 for APEX
        experiment = PsychopyExperimentSetup(TMSiDevice="APEX", COM_port = 'COM3', n_trials = 3, target_value = 16, nontarget_value= 2)
        
        # Check if there is already a plotter application in existence
        app = QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not app:
            app = QApplication(sys.argv)
        
        # Initialise the helper
        plotter_helper = ImpedancePlotterHelper(device=dev,
                                                layout='head', 
                                                file_storage = join(measurements_dir,"Example_PsychoPy_ERP_experiment"))
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
            # Enter the event loop
        app.exec_()
        
        # Pause for a while to properly close the GUI after completion
        print('\n Wait for a bit while we close the plot... \n')
        time.sleep(1)
        
        # Initialise a file-writer class (Poly5-format) and state its file path
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"Example_PsychoPy_ERP_experiment.poly5"))
            
        # # Define the handle to the device
        file_writer.open(dev)
        
        # Define thread to run the experiment
        thread = Thread(target=experiment.runExperiment)
        

        # Initialise the new plotter helper
        plotter_helper = SignalPlotterHelper(device=dev)
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
        # Open the plot window, start the PsychoPy thread and show the signals
        thread.start()
        app.exec_()

        # Close the file writer after GUI termination
        file_writer.close()
        
        # Close the connection to APEX
        dev.close()
        

except TMSiError as e:
    print(e)

except TTLError as e:
   raise TTLError("Is the TTL module connected? Please try again")

        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()