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
 * @file ${example_SD_card_get_list_of_files.py} 
 * @brief This example shows how to retrieve all files that are currently 
 * stored on SAGA’s onboard memory.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
import time

Example_dir = dirname(realpath(__file__))  # directory of this file
modules_dir = join(Example_dir, '..')  # directory with all modules
sys.path.append(modules_dir)

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device.tmsi_device_enums import MeasurementType

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
    
        # Enable backup logging of the device
        dev.set_device_backup_logging(prefix_filename='Example')
        
        # Perform 3 consecutive recordings
        dev.start_measurement(MeasurementType.SAGA_SIGNAL)
        time.sleep(2)
        dev.stop_measurement()
        time.sleep(1)
        
        dev.start_measurement(MeasurementType.SAGA_SIGNAL)
        time.sleep(2)
        dev.stop_measurement()
        time.sleep(1)
        
        dev.start_measurement(MeasurementType.SAGA_SIGNAL)
        time.sleep(2)
        dev.stop_measurement()
        
        # Check whehter the 3 recordings are available onboard
        recordings_list = dev.get_device_card_file_list()
        for rec_id in range(len(recordings_list)):
            print("{} - {}".format(rec_id, recordings_list[rec_id].RecFileName.decode('utf-8')))
            
        # Close the connection to the device
        dev.close()
    
except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()