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
 * @file ${example_load_save_configurations.py} 
 * @brief This example shows how to load/save several different configurations 
 * from/to a file (in the “configs” directory).
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
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
        
        # Upload a configuration from file to the device and print the active channel list
        # of this configuration
        print('Loading a configuration with one active UNI-channel : \n')
        if dev.get_num_channels()<64:
            dev.import_configuration(join(configs_dir, "saga_config_minimal32.xml"))
        else:
            dev.import_configuration(join(configs_dir, "saga_config_minimal.xml"))
        
        for idx, ch in enumerate(dev.get_device_active_channels()):
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch.get_channel_name(), ch.get_channel_unit_name()))
    
        # Enable all UNI-channels, print the updated active channel list and save the new configuration to file
        print('\nActivate all UNI-channels : ')
        if dev.get_num_channels()<64:
            dev.set_device_active_channels(range(1,33), True)
        else:
            dev.set_device_active_channels(range(1,65), True)
        for idx, ch in enumerate(dev.get_device_active_channels()):
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch.get_channel_name(), ch.get_channel_unit_name()))
    
        print('\nSave the configuration to the file [..\\TMSiSDK\\tmsi_resources\\saga_config_current.xml]')
        dev.export_configuration(join(configs_dir, "saga_config_current.xml"))
    
        # Close the connection to the SAGA-system
        dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()