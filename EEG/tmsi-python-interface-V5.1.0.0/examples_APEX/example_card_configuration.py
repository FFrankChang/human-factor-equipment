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
 * @file ${example_card_configuration.py} 
 * @brief This example shows how to change the card recording configuration.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
from datetime import datetime, timedelta

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)


from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceInterfaceType, DeviceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import ApexStructureGenerator, ApexEnums



try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(DeviceType.apex, DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.apex)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to APEX
        dev.open()
        
        # Create device card recording configuration
        # Set start and stop time to 1 and 2 minutes from now
        # Start control can be either 'Time' or 'Button', start and stop time
        # are ignored when 'Button' is used
        config = ApexStructureGenerator.create_card_record_configuration(
            device = dev,
            start_control = ApexEnums.ApexStartCardRecording.Time,
            prefix_file_name = "TimedRec",
            start_time = datetime.now() + timedelta(minutes = 1),
            stop_time = datetime.now() + timedelta(minutes = 2))
        
        # Set the card recording configuration.
        dev.set_card_recording_config(config)
        
        # Close the connection to the device
        dev.close()

except TMSiError as e:
    print(e)
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()