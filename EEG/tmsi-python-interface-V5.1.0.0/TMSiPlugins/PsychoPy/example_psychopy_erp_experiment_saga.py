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
 * @file ${example_psychopy_erp_experiment_saga.py} 
 * @brief This example shows how to combine sending triggers to SAGA with running a 
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

from PySide2.QtWidgets import *

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate
from TMSiSDK.device import ChannelType

from TMSiGui.gui import Gui
from TMSiPlotterHelpers.impedance_plotter_helper import ImpedancePlotterHelper
from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper
from TMSiFileFormats.file_writer import FileWriter, FileFormat

from experiment_psychopy import PsychopyExperimentSetup
import time
from threading import Thread
from TMSiSDK.tmsi_utilities.mask_type import MaskType
from TMSiPlugins.external_devices.usb_ttl_device import TTLError


try:
      # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)
    
    if (len(discoveryList)>0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
        
        # Load the EEG channel set and configuration
        print("load EEG config")
        if dev.get_num_channels()<64:
            dev.import_configuration(join(configs_dir, "saga_config_EEG32.xml"))
        else:
            dev.import_configuration(join(configs_dir, "saga_config_EEG64.xml")) 
        
        # Set the sample rate of the AUX channels to 4000 Hz
        dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Decimal)
        dev.set_device_triggers(True)
               
        # Downsample
        dev.set_device_sampling_config(channel_type = ChannelType.UNI, channel_divider = 4)
        dev.set_device_sampling_config(channel_type = ChannelType.BIP, channel_divider = 4)
        dev.set_device_sampling_config(channel_type = ChannelType.AUX, channel_divider = 4)
                
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
        
        # Find the trigger channel index number
        channels = dev.get_device_active_channels()
        for i in range(len(channels)):   
            if channels[i].get_channel_name() == 'TRIGGERS':
                trigger_channel = i    

        # Apply mask on trigger channel. This mask is applied because SAGA TRIGGER input has inverse logic. 
        # By applying the mask, the baseline of the triggers is low again
        dev.apply_mask([trigger_channel],[MaskType.REVERSE])

        # Initialize PsychoPy Experiment, for arguments description see class
        print('\n Initializing PsychoPy experiment and TTL module \n')
        print('\n  Please check if red LED is turned on ... \n')
        # !! NOTE: Available options for the (non)target_value inputs are all numbers between 1 and 255 for SAGA
        experiment = PsychopyExperimentSetup(TMSiDevice="SAGA", COM_port = 'COM3', n_trials = 8, target_value = 128, nontarget_value= 64)
        
        # Initialise a file-writer class (Poly5-format) and state its file path
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"Example_PsychoPy_ERP_experiment.poly5"))
            
        # # Define the handle to the device
        file_writer.open(dev)
        
        # Start measurement & define thread to start experiment
        thread = Thread(target=experiment.runExperiment)

        # Initialise the new plotter helper
        plotter_helper = SignalPlotterHelper(device=dev)
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
        thread.start()
        # Open the plot window, start the PsychoPy thread and show the signals
        app.exec_()
    
        # Close the file writer after GUI termination
        file_writer.close()
        # Close the connection to the SAGA device
        dev.close()
    

        
except TMSiError as e:
    print(e)

except TTLError:
    raise TTLError("Please try again and check if LEDs blink")

        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()