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
 * @file ${example_bipolar_and_auxiliary_measurement.py} 
 * @brief This example shows the functionality to display the output of an AUX 
.* sensor and the output of a simultaneously sampled BIP channel on 
.* the screen. To do so, the channel configuration is updated and a 
.* call is made to update the sensor channels. The data is saved to a 
.* Poly5 file.
 */


'''

from PySide2.QtWidgets import *
import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiSDK.device import ChannelType
from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate

from TMSiFileFormats.file_writer import FileWriter, FileFormat
from TMSiGui.gui import Gui
from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
        
        # Set the sample rate of the BIP and AUX channels to 2000 Hz
        dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Decimal,  channel_type = ChannelType.BIP, channel_divider =1)
        dev.set_device_sampling_config(channel_type = ChannelType.AUX, channel_divider = 1)
        
        # Enable BIP 01, AUX 1-1, 1-2 and 1-3
        AUX_list = [0,1,2]
        BIP_list = [0]
        
        # Retrieve all channels from the device and update which should be enabled
        ch_list = dev.get_device_channels()
        
        # The counters are used to keep track of the number of AUX and BIP channels 
        # that have been encountered while looping over the channel list
        AUX_count = 0
        BIP_count = 0
        enable_channels = []
        disable_channels = []
        for idx, ch in enumerate(ch_list):
            if (ch.get_channel_type() == ChannelType.AUX):
                if AUX_count in AUX_list:
                    enable_channels.append(idx)
                else:
                    disable_channels.append(idx)
                AUX_count += 1
            elif (ch.get_channel_type()== ChannelType.BIP):
                if BIP_count in BIP_list:
                    enable_channels.append(idx)
                else:
                    disable_channels.append(idx)
                BIP_count += 1
            else :
                disable_channels.append(idx)
    
        dev.set_device_active_channels(enable_channels, True)
        dev.set_device_active_channels(disable_channels, False)
        
        # Initialise a file-writer class (Poly5-format) and state its file path
        file_writer = FileWriter(FileFormat.poly5, join(measurements_dir,"Example_BIP_and_AUX_measurement.poly5"))

        # Define the handle to the device
        file_writer.open(dev)
        
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
        
        # Close the file writer after GUI termination
        file_writer.close()
        
        # Close the connection to the SAGA device
        dev.close()
    
except TMSiError as e:
    print(e)
    
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()