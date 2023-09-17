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
 * @file ${example_config_settings.py} 
 * @brief This example shows how load and save .xml-configuration files for 
 * APEX.
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

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable


try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(DeviceType.apex, DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.apex)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the APEX-system
        dev.open()
        
        # Save the current device configuration to file
        dev.export_configuration(join(configs_dir, 'APEX_current_config.xml'))
    
        if dev.get_num_channels()<32:
            # Load the EEG channel set and configuration
            print("load EEG config 24")
            dev.import_configuration(join(configs_dir, 'APEX_config_EEG24.xml'))
        else:
            # Load the EEG channel set and configuration
            print("load EEG config 32")
            dev.import_configuration(join(configs_dir, 'APEX_config_EEG32.xml'))
        
        # Close the connection to the device
        dev.close()  
    
except TMSiError as e:
    print(e)
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()