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
 * @file ${example_SD_card_download.py} 
 * @brief This example shows how to download card recordings that are stored on 
 * SAGA’s onboard memory.
 *
 */


'''

import sys
from os.path import join, dirname, realpath

Example_dir = dirname(realpath(__file__))  # directory of this file
modules_dir = join(Example_dir, '..')  # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable

from TMSiFileFormats.file_writer import FileWriter, FileFormat

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
    
        # Create a file writer object to download the onboard recording (if there is any)
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_SD_card_download.poly5"))
        file_writer.open(dev)
        
        # Get a list of all available recordings
        recordings_list = dev.get_device_card_file_list()
        if len(recordings_list) <= 0:
            raise(IndexError)
                
        # Start downloading the most recent file from the onboard memory
        dev.download_file_from_device(file_id= recordings_list[-1].RecFileID)
                
        # Close the file writer after completion of the download
        file_writer.close()
        
        # Close the connection to the device
        dev.close()

except IndexError:
    print("device memory is empty, impossible to download any file")
    
    # Close the connection to the device
    dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()