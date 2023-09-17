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
 * @file ${example_config_settings.py} 
 * @brief This example shows the different configuration options, more detailed
 * explanations can be found in the examples of individual properties.
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
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate, RefMethod, AutoRefMethod
from TMSiSDK.device import ChannelType



try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]

        # Open a connection to the SAGA-system
        dev.open()

        # Print current device configuation
        print('Current device configuration:')
        print('Base-sample-rate: {0} Hz'.format(dev.get_device_sampling_frequency(detailed=True)['base_sampling_rate']))
        print('Sample-rate: {0} Hz'.format(dev.get_device_sampling_frequency()))
        print('Interface-bandwidth: {0} b/s'.format(dev.get_device_bandwidth()))
        print('Reference Method: ', dev.get_device_references())
        print('Sync out configuration: ', dev.get_device_sync_out_config())
        print('Triggers: ', dev.get_device_triggers() )

        # Update the different configuration options:

        # Set base sample rate: either 4000 Hz (default, Decimal)or 4096 Hz (Binary).
        dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Decimal)

        # Set sample rate to 2000 Hz (base_sample_rate/2)
        dev.set_device_sampling_config(channel_type = ChannelType.all_types, channel_divider = 2)

        # Specify the reference method and reference switch method that are used during sampling
        dev.set_device_references(reference_method = RefMethod.Common, auto_reference_method = AutoRefMethod.Fixed)

        # Set the trigger settings
        dev.set_device_triggers(True)

        # Set the sync out configuration
        dev.set_device_sync_out_config(marker=False, frequency=1, duty_cycle=50)

        # Print new device configuation
        print('\n\nNew device configuration:')
        print('Base-sample-rate: {0} Hz'.format(dev.get_device_sampling_frequency(detailed=True)['base_sampling_rate']))
        print('Sample-rate: {0} Hz'.format(dev.get_device_sampling_frequency()))
        print('Interface-bandwidth: {0} b/s'.format(dev.get_device_bandwidth()))
        print('Reference Method: ', dev.get_device_references())
        print('Sync out configuration: ', dev.get_device_sync_out_config())
        print('Triggers:', dev.get_device_triggers() )

        # Close the connection to the SAGA device
        dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()