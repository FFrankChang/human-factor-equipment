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
 * @file ${example_SD_card_configuration.py} 
 * @brief This example shows the functionality to get and set the 
 * configuration of the onboard memory of SAGA. The prefix file name is 
 * changed in the example.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
import datetime

Example_dir = dirname(realpath(__file__))  # directory of this file
modules_dir = join(Example_dir, '..')  # directory with all modules
sys.path.append(modules_dir)


from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import SagaStructureGenerator, SagaEnums

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
        
        # Disable backup logging of recordings to the SD card
        dev.set_device_repair_logging(enable_repair_logging = False)
        
        # Get the device's card configuration and print the file Pre-fix
        device_amb_conf = dev.get_card_recording_config()
        print("T1: " + "".join(map(lambda x: chr(x) if x >=
              0 else " ", device_amb_conf.PrefixFileName[:])))
        
        # Check the current bandwidth that's in use (this may not exceed 2Mbit/s for card recordings)
        current_bandwidth = dev.get_device_bandwidth()
        print('The currently used bandwidth is {:} bit/s'.format(current_bandwidth['in use']))
        print('Maximum bandwidth for card measurements is {:} bit/s'.format(current_bandwidth['internal memory']))
        
        # Enable button start of card recordings
        config = SagaStructureGenerator.create_card_record_configuration(
            device = dev,
            start_control = SagaEnums.SagaStartCardRecording.Button,
            prefix_file_name = "ButtonRec")
        dev.set_card_recording_config(config)
        
        # Get the device's card configuration and print the file Pre-fix
        device_amb_conf2 = dev.get_card_recording_config()
        print("T2: " + "".join(map(lambda x: chr(x) if x >=
              0 else " ", device_amb_conf2.PrefixFileName[:])))
        
        # Close the connection to the device
        dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()
