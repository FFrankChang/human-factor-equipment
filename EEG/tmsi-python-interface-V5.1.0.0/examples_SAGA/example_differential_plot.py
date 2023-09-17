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
 * @file ${example_differential_plot.py} 
 * @brief This file shows how to make a differential signal plotter for HD-EMG purposes.
 * The channel names are used to detect which channels have to be subtracted from each other.
 * The original data is shown in one window, while the differentials are shown in a second window.
 * Note that channels are just substracted from each other, no out of range detection is applied.
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
from PySide2.QtWidgets import *

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceInterfaceType, DeviceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable

from TMSiGui.gui_2windows import Gui
from TMSiPlotterHelpers.differential_signal_plotter_helper import DifferentialSignalPlotterHelper

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(
        dev_type=DeviceType.saga,
        dr_interface=DeviceInterfaceType.docked,
        ds_interface=DeviceInterfaceType.usb
    )
    discoveryList = TMSiSDK().get_device_list(dev_type=DeviceType.saga)

    if len(discoveryList)>0:
        # Get the handle to the first discovered device.
        dev = discoveryList[0]

        # Open a connection to the SAGA-system
        dev.open()
        print("saga opened")

        grid_type = '4-8-L'

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
            
        # Initialise the helper. 
        # Note that the grid type argument is only used in the main plotter
        # In the differential plotter the channel names are use to detect which channels have to be subtracted from each other.
        plotter_helper = DifferentialSignalPlotterHelper(device=dev, grid_type=grid_type)
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
         # Enter the event loop
        app.exec_()

        # Close the connection to the SAGA device
        dev.close()
        print("saga closed")

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()