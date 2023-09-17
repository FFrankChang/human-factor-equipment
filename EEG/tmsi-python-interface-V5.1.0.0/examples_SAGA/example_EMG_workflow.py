'''
(c) 2022, 2023 Twente Medical Systems International B.V., Oldenzaal The Netherlands

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
 * @file ${example_EMG_workflow.py} 
 * @brief This example shows the functionality of the impedance plotter and an
 * HD-EMG heatmap. The user can disable channels based on measured impedances.
 * The heatmap displays the RMS value per channel, combined with linear 
 * interpolation to fill the space between channels.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
configs_dir = join(Example_dir, '../TMSiSDK\\tmsi_resources') # directory with configurations
sys.path.append(modules_dir)
import time

from PySide2.QtWidgets import *

from TMSiFileFormats.file_writer import FileWriter, FileFormat

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable

from TMSiGui.gui import Gui
from TMSiPlotterHelpers.impedance_plotter_helper import ImpedancePlotterHelper
from TMSiPlotterHelpers.heatmap_plotter_helper import HeatmapPlotterHelper

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
        
        grid_type = '8-8-S'
        # options:'4-8-L', '6-11-L', '6-11-S', '8-8-L', '8-8-S', '6-11-L-1', '6-11-L-2', '6-11-S-1', '6-11-S-2', '8-8-L-1', '8-8-L-2', '8-8-S-1', '8-8-S-2'
        
        # Load the HD-EMG channel set and configuration
        print("load HD-EMG config")
        if dev.get_num_channels()<64:
            dev.import_configuration(join(configs_dir, "saga32_config_textile_grid_" + grid_type + ".xml"))
        else:
            dev.import_configuration(join(configs_dir, "saga64_config_textile_grid_" + grid_type + ".xml"))
        
        # Check if there is already a plotter application in existence
        app = QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not app:
            app = QApplication(sys.argv)
        
        # Initialise the helper
        plotter_helper = ImpedancePlotterHelper(device=dev,
                                                 layout=grid_type, 
                                                 file_storage = join(measurements_dir,"example_EMG_workflow"))
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
            file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_EMG_workflow.poly5"))
        elif file_format.lower()=='xdf':
            file_writer = FileWriter(FileFormat.xdf, join(measurements_dir,"example_EMG_workflow.xdf"), add_ch_locs=True)
        else:
            print('File format not supported. File is saved to Poly5-format.')
            file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_EMG_workflow.poly5"))
        
        # Define the handle to the device
        file_writer.open(dev)
    
        # Initialise the new plotter helper and filter
        # In case you want to use the signal plotter, use the grid_type argument to order the channels
        # following the order of the channels in the grid, see example_filter_and_plot
        plotter_helper = HeatmapPlotterHelper(device=dev, layout=grid_type, hpf=5, order=1)
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
         # Enter the event loop
        app.exec_()
        
        # Close the file writer after GUI termination
        file_writer.close()
        
        # Close the connection to the SAGA device
        dev.close()
    
except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()