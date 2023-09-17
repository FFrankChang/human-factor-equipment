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
 * @file ${example_changing_sample_rate.py} 
 * @brief This example shows how to change the Base Sample Rate property of 
 * SAGA, as well as how the active sample rate of individual channels can be 
 * changed.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import ChannelType
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()

        fs_info= dev.get_device_sampling_frequency(detailed=True)
        print('The current base-sample-rate is {0} Hz.'.format(fs_info['base_sampling_rate']))
        print('\nThe current sample-rates per channel-type-group are :')
    
        for fs in fs_info:
            if fs != 'base_sampling_rate':
                print('{0} = {1} Hz'.format(fs, fs_info[fs]))

    
        # The sample-rate of the channel-type-groups are derivated from the base-sample-rate.
        # Changing the base-sample-rate will therefor also automatically change the
        # sample-rate of the channel-type-groups.
        #
        # Note: The SAGA-systems 'knows' 2 base-sample-rates : 4000 Hz (default, Decimal) and 4096 Hz (Binary).
        dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Binary)
        
        fs_info= dev.get_device_sampling_frequency(detailed=True)
        print('\n\nThe updated base-sample-rate is {0} Hz.'.format(fs_info['base_sampling_rate']))
        print('\nThe updated sample-rates per channel-type-group are :')
    
        for fs in fs_info:
            if fs != 'base_sampling_rate':
                print('{0} = {1} Hz'.format(fs, fs_info[fs]))

    
        # It is also possible to change the sample-rate per channel-type-group individually.
        # The sample-rate is a derivate from the actual base-sample-rate. The sample-rate
        # must be set as a portion of the base-sample-rate. This can be done as next:
        #       
        #       -1 (= channels disabled),
        #       1 ( = 100% of the base-sample-rate),
        #       2 ( =  50% of the base-sample-rate),
        #       4 ( =  25% of the base-sample-rate) or
        #       8 ( =  12.5% of the base-sample-rate)
        #
        # Other values then -1,1,2,4 or 8 are not possible.
        #
        # To set a sample-rate of 512 Hz for all channel-type-groups, the base-sample-rate
        # must be 4096 Hz an the divider-value must be 8
        #
        # The sample-rate can be set per channel-type-group or for all channel-type-groups
        # at once as demostrated in the next example.
        dev.set_device_sampling_config(channel_type = ChannelType.all_types, channel_divider = 2)
        dev.set_device_sampling_config(channel_type = ChannelType.BIP, channel_divider = 4)
        dev.set_device_sampling_config(channel_type = ChannelType.UNI, channel_divider = 8)
    
        fs_info= dev.get_device_sampling_frequency(detailed=True)
        print('\n\nThe base-sample-rate is still {0} Hz.'.format(fs_info['base_sampling_rate']))
        print('\nThe updated sample-rates per channel-type-group are now :')
    
        for fs in fs_info:
            if fs != 'base_sampling_rate':
                print('{0} = {1} Hz'.format(fs, fs_info[fs]))
    
        # Close the connection to the SAGA-system
        dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()