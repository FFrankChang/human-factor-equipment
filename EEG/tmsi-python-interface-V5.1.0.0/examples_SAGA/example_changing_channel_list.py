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
 * @file ${example_changing_channel_list.py} 
 * @brief This example shows the manipulation of the active channel list and 
 * demonstrates how the channel names can be changed.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiSDK.device import ChannelType
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

        print('The active channels are : \n')
        channels = dev.get_device_active_channels()
        for idx, ch in enumerate(channels):
             ch_name = ch.get_channel_name()
             ch_unit_name = ch.get_channel_unit_name()
             bandwidth = ch.get_channel_bandwidth()
             print('[{0}] : [{1}] in [{2}], bw = [{3}]'.format(idx, ch_name, ch_unit_name, bandwidth))          
    
        # Enable all AUX-channels, print the updated active channel list
        #
        # Note : To change channel-properties next steps are executed:
        #
        #           1. Request the current total channel list, which can be
        #              retrieved with statement [ch_list = dev.get_device_channels()]
        #           2. Check which channels should be activated/deactivated
        #           3. Write changes you want to make back to the device-object with the statement
        #              [dev.set_device_active_channels(indices, activate)]
        #
        # Note : The channels of type ChannelType.status and ChannelType.counter can
        #        not be disabled. The device will ignore such changes.
        ch_list = dev.get_device_channels()
        enable_channels = []
        disable_channels = []
        for idx, ch in enumerate(ch_list):
            if (ch.get_channel_type() == ChannelType.AUX):
                enable_channels.append(idx)
            else :
                disable_channels.append(idx)
        dev.set_device_active_channels(enable_channels, True)
        dev.set_device_active_channels(disable_channels, False)
    
        print('\nActivated only AUX-channels, de-activated the other channels, the active channels are now :')
        for idx, ch in enumerate(dev.get_device_active_channels()):
             ch_name = ch.get_channel_name()
             ch_unit_name = ch.get_channel_unit_name()
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch_name, ch_unit_name))
    
        # Rename some AUX-channels, print the updated active channel list
        #
        # Note : The name of the channels of type ChannelType.status and ChannelType.counter
        #        can not be changed. The device will ignore such changes.
        for idx, ch in enumerate(dev.get_device_channels()):
            if (ch.get_channel_name() == 'AUX 1-1'):
                 dev.set_device_channel_names(['Light'], [idx])
            if (ch.get_channel_name() == 'AUX 2-2'):
                 dev.set_device_channel_names(['Y'], [idx])

    
        print('\nRenamed channels [AUX 1-1] and [AUX 2-2], the names of the active channels are now :')
        for idx, ch in enumerate(dev.get_device_active_channels()):
             ch_name = ch.get_channel_name()
             ch_unit_name = ch.get_channel_unit_name()
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch_name, ch_unit_name))
             
             
        # Enable a subset of UNI-channels, print the updated channel list
        #
        # Note : The channels of type ChannelType.status and ChannelType.counter can
        #        not be disabled. The device will ignore such changes.
        
        # Enable the first 24 UNI channels, skipping CREF
        dev.set_device_active_channels(range(1,25), True)
           
        print('\nActivated the first 24 UNI-channels, de-activated other UNI-channels, the active channels are now :')
        for idx, ch in enumerate(dev.get_device_active_channels()):
             ch_name = ch.get_channel_name()
             ch_unit_name = ch.get_channel_unit_name()
             print('[{0}] : [{1}] in [{2}]'.format(idx, ch_name, ch_unit_name))
    
        # Close the connection to the SAGA-system
        dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()