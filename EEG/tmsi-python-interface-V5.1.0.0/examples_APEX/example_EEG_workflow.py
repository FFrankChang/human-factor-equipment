'''
(c) 2022,2023 Twente Medical Systems International B.V., Oldenzaal The Netherlands

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
 * @file ${example_EEG_workflow.py} 
 * @brief This example shows the functionality of the impedance plotter and the 
 * data stream plotter. The example is structured as if an EEG measurement is
 * performed, so the impedance plotter is displayed in head layout. The channel 
 * names are set to the name convention of the TMSi EEG cap using a 
 * pre-configured EEG configuration. Measurement data is saved to poly5 or 
 * xdf-file, depending on user input.
 *
 */


'''
from PySide2.QtWidgets import *
import sys
import time
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
configs_dir = join(Example_dir, '../TMSiSDK\\tmsi_resources') # directory with configurations
sys.path.append(modules_dir)

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiFileFormats.file_writer import FileWriter, FileFormat

from TMSiGui.gui import Gui
from TMSiPlotterHelpers.impedance_plotter_helper import ImpedancePlotterHelper
from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper


try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(DeviceType.apex, DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.apex)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to APEX
        dev.open()
        
        if dev.get_num_channels()<32:
            # Load the EEG channel set and configuration
            print("load EEG config 24")
            dev.import_configuration(join(configs_dir, 'APEX_config_EEG24.xml'))
        else:
            # Load the EEG channel set and configuration
            print("load EEG config 32")
            dev.import_configuration(join(configs_dir, 'APEX_config_EEG32.xml'))
        
        # Check if there is already a plotter application in existence
        app = QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not app:
            app = QApplication(sys.argv)
        
        # Initialise the helper
        plotter_helper = ImpedancePlotterHelper(device=dev,
                                                 layout='head', 
                                                 file_storage = join(measurements_dir,"example_impedance_plot"))
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
         # Enter the event loop
        app.exec_()
        
        # Pause for a while to properly close the GUI after completion
        print('\n Wait for a bit while we close the plot... \n')
        time.sleep(1)
        
        # Ask for desired file format
        file_format=input("Which file format do you want to use? (Options: poly5 or xdf)\n")
        
        # Initialise the desired file-writer class and state its file path
        if file_format.lower()=='poly5':
            file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_EEG_workflow.poly5"))
        elif file_format.lower()=='xdf':
            file_writer = FileWriter(FileFormat.xdf, join(measurements_dir,"example_EEG_workflow.xdf"), add_ch_locs=True)
        else:
            print('File format not supported. File is saved to Poly5-format.')
            file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_EEG_workflow.poly5"))
        
        # Define the handle to the device
        file_writer.open(dev)
    
        # Initialise the new plotter helper
        plotter_helper = SignalPlotterHelper(device=dev)
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
         # Enter the event loop
        app.exec_()
        
        # Close the file writer after GUI termination
        file_writer.close()
        
        # Close the connection to the device
        dev.close()
    
except TMSiError as e:
    print(e)
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()
