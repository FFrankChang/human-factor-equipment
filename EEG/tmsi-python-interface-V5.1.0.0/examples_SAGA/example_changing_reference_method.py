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
 * @file ${example_changing_reference_method.py} 
 * @brief This example shows how to change the applied reference method. The
 * configurable options are RefMethod.common and RefMethod.average.
 * In case of common reference, the reference switch method can be set to 
 * AutoRefMethod.Fixed or AutoRefMethod.Average. In case of 
 * AutoRefMethod.Average, reference method automatically swithces to average 
 * reference when the common reference signal is out of range
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)
import time

from TMSiFileFormats.file_writer import FileWriter, FileFormat
from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import ChannelType
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate, RefMethod, AutoRefMethod
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
    
        # Set the sample rate of all channels to 1000 Hz
        dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Decimal,  channel_type = ChannelType.all_types, channel_divider = 4)
        
        # Specify the reference method and reference switch method that are used during sampling 
        # RefMethod: Average or Common
        # AutoRefMethod: Fixed or Average
        dev.set_device_references(reference_method = RefMethod.Common, auto_reference_method = AutoRefMethod.Fixed)
        
        # Check whether device is a SAGA 64+ or SAGA 32+ system
        # Enable all UNI-channels
        nCh = dev.get_num_channels()
        if nCh > 64:
            dev.set_device_active_channels(range(1,65), True)
        else:
            dev.set_device_active_channels(range(1,33), True)
        
        # When the device samples in average reference method, the CREF channel can be disabled
        if dev.get_device_references()['reference'] == RefMethod.Average:
            dev.set_device_active_channels([0], False)   
    
        # Before the measurement starts first a file-writer-object must be created and opened.
        # Upon creation specify :
        #   - the data-format 'poly5' to be used
        #   - the filepath/name, where the file must be stored
        # then 'link' the file-writer-instance to the device.
        # The file-writer-object is now ready to capture the measurement-data and
        # write it to the specified file.
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir, "changed_reference_method_measurement.poly5"))
        file_writer.open(dev)
    
        # Start the measurement and wait 10 seconds. In the mean time the file-writer-instance
        # will capture the sampling data and store it into the specified file in the 'poly5'-data format.
        dev.start_measurement(MeasurementType.SAGA_SIGNAL)
    
        # Wait for 10 seconds
        time.sleep(10)
    
        # Stop the measurement
        dev.stop_measurement()
    
        # Close the file-writer-instance.
        # The sample-data of the measurement has been archived into the specified file.
        file_writer.close()
    
        # Close the connection to the SAGA-system
        dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()