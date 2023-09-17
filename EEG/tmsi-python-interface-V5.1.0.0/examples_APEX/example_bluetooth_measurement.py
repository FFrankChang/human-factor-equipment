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
 * @file ${example_bluetooth_measurement.py} 
 * @brief This example shows how to discover and connect to a device over the 
 * bluetooth interface
 */


'''


from PySide2.QtWidgets import *
import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
configs_dir = join(Example_dir, '../TMSiSDK\\tmsi_resources') # directory with configurations
sys.path.append(modules_dir)

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable

from TMSiGui.gui import Gui
from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(DeviceType.apex, DeviceInterfaceType.bluetooth)
    dongle = TMSiSDK().get_dongle_list(DeviceType.apex)[0]
    discoveryList = TMSiSDK().get_device_list(DeviceType.apex)

    if (len(discoveryList) > 0):
        # Get the handle to the paired device.
        for i, dev_i in enumerate(discoveryList):
            if dev_i.get_dongle_serial_number() == dongle.get_serial_number():
                dev_id = i   
        dev = discoveryList[dev_id]
        
        # Open a connection to the APEX-system
        dev.open(dongle_id = dongle.get_id())
        
        # Check if there is already a plotter application in existence
        app = QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not app:
            app = QApplication(sys.argv)
        
        plotter_helper = SignalPlotterHelper(device=dev)
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
         # Enter the event loop
        app.exec_()
        
        # Close the connection to the device
        dev.close()
    
except TMSiError as e:
    print(e)

        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()

