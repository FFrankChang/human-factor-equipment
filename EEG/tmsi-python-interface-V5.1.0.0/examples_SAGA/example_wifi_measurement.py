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
 * @file ${example_wifi_measurement.py} 
 * @brief This example shows how to perform a measurement over the wireless 
 * interface, while data is backed up to the SD card. Finally, the full 
 * recording is downloaded from the device.
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
from PySide2.QtWidgets import *

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import ChannelType
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate, RefMethod

from TMSiFileFormats.file_writer import FileWriter, FileFormat

from TMSiGui.gui import Gui
from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Create the device object to interface with the SAGA-system.
        dev = discoveryList[0]
    
        # Find and open a connection to the SAGA-system
        dev.open()
        
        # Check the current bandwidth that's in use
        current_bandwidth = dev.get_device_bandwidth()
        print('The current bandwidth in use is {:} bit/s'.format(current_bandwidth['in use']))
        print('Maximum bandwidth for wifi measurements is {:} bit/s'.format(current_bandwidth['wifi']))
        
        # Maximal allowable sample rate with all enabled channels is 1000 Hz
        dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Decimal,  channel_type = ChannelType.all_types, channel_divider = 4)

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
    
        # Check the current bandwidth that's in use
        current_bandwidth = dev.get_device_bandwidth()
        print('The current bandwidth in use is {:} bit/s'.format(current_bandwidth['in use']))

        # Choose the desired DR-DS interface type 
        dev.set_device_interface(DeviceInterfaceType.wifi)
        
        # Close the connection to the device (with the original interface type)
        dev.close()
        
        # Wait for a bit while the connection is closed
        time.sleep(1)
    
    # Discover the device object with the new interface type. Important: number of retries should be more than default. 
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.wifi, ds_interface = DeviceInterfaceType.usb, num_retries = 10)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    
    if (len(discoveryList) > 0):
        # Create the device object to interface with the SAGA-system.
        dev = discoveryList[-1]
        
        # Find and open the connection to the SAGA-system
        dev.open()
        
        # Before the measurement starts first a file-writer-object must be created and opened.
        # Upon creation specify :
        #   - the data-format 'poly5' to be used
        #   - the filepath/name, where the file must be stored
        # then 'link' the file-writer-instance to the device.
        # The file-writer-object is now ready to capture the measurement-data and
        # write it to the specified file.
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"example_wifi_measurement.poly5"))
        file_writer.open(dev)
        
        # Enable backup logging of the device
        dev.set_device_repair_logging(enable_repair_logging = True)
    
        # Check if there is already a plotter application in existence
        app = QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not app:
            app = QApplication(sys.argv)
        
        plotter_helper = SignalPlotterHelper(device=dev)
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
         # Enter the event loop
        app.exec_()
    
        # Close the file-writer-instance.
        # The sample-data of the measurement has been archived into the specified file.
        file_writer.close()
        
        # Close the connection over the current interface
        dev.close()
        
    # Discover the device via the docked interface again
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    
    if (len(discoveryList) > 0):
        # Create the device object to interface with the SAGA-system.
        dev = discoveryList[0]
         
        # Reopen the connection to the device
        dev.open()
        
        # Retrieve the recordings list with the full file on there
        recordings_list = dev.get_device_card_file_list()
        
        # Configure a file writer to save the backed up data
        file_writer_backup = FileWriter(FileFormat.poly5, join(measurements_dir,"example_wifi_measurement_backup_logging.poly5"))
        file_writer_backup.open(dev)
        
        # Get the handle to the latest file and start downloading the data
        dev.download_file_from_device(file_id= recordings_list[-1].RecFileID)
    
        # Close the file writer after download completion
        file_writer_backup.close()
    
        # Close the connection to the SAGA-system
        dev.close()

except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()
