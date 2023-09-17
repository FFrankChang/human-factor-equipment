'''
(c) 2023 Twente Medical Systems International B.V., Oldenzaal The Netherlands

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
 * @file ${impedance_plotter_helper.py}
 * @brief This file is used as helper to make an impedance plotter in the GUI
 *
 */
'''

import numpy as np
import collections
import pandas as pd
from os.path import join, dirname, realpath, normpath, exists
import json
import datetime

from TMSiFrontend.plotters.impedance_plotter import ImpedancePlotter
from TMSiFrontend.utilities.tmsi_grids import TMSiGrids
from TMSiFrontend.utilities.tmsi_headcaps import TMSiHeadcaps

from TMSiBackend.data_consumer.consumer import Consumer
from TMSiBackend.data_consumer.consumer_thread import ConsumerThread
from TMSiBackend.data_monitor.monitor import Monitor

from TMSiSDK.device.tmsi_device_enums import MeasurementType

from .plotter_helper import PlotterHelper


Plotter_dir = dirname(realpath(__file__)) # directory of this file
measurements_dir = join(Plotter_dir, '../../measurements') # directory with all measurements
modules_dir = normpath(join(Plotter_dir, '..')) # directory with all modules

class ImpedancePlotterHelper(PlotterHelper):
    def __init__(self,  device, layout = None, file_storage = None):
        super().__init__(device=device, monitor_class = Monitor, consumer_thread_class = ConsumerThread)
        self._save_impedances = file_storage

        # Set measurement type, monitor funtion and layout
        self._read_grid_info()
        if device.get_device_type() == 'SAGA':
            self.measurement_type = MeasurementType.SAGA_IMPEDANCE
            self.monitor_function = self.monitor_function_saga
            if layout in self.conversion_data or layout == 'head':
                self.layout = layout
            else: 
                self.layout = 'grid'
        elif device.get_device_type() == 'APEX':
            self.measurement_type = MeasurementType.APEX_IMPEDANCE
            self.monitor_function = self.monitor_function_apex
            if layout != 'grid':
                self.layout = 'head'
            else:
                self.layout = layout

        # Initialize plotter
        if self.layout == 'head':
            self.main_plotter = ImpedancePlotter(device_type = device.get_device_type(), is_headcap=True)
        else:
            self.main_plotter = ImpedancePlotter(device_type = device.get_device_type(), is_headcap=False)

    def callback(self, response):
        # Get impedance values
        if "impedances" in response:
            data_to_plot=[response["impedances"][i]["Re"] for i in range(len(response["impedances"]))]
            # Overwrite value if checkbox is disabled
            for ch in self.disable_channels:
                data_to_plot[ch] = 5000
            # Sent data to plotter
            self.main_plotter.update_chart(data_to_plot)
            self.impedances = data_to_plot

    def initialize(self):
        self.channels_default =self.device.get_device_impedance_channels() 
        # Get and setelectrode coordinates
        coordinates = self._get_coordinates()
        if hasattr(self, 'conversion_list'): 
            self.main_plotter.set_electrode_position(channels = self.channels_default, coordinates = coordinates, reordered_indices=self.conversion_list.tolist())
        else:
            self.main_plotter.set_electrode_position(channels = self.channels_default, coordinates = coordinates)

        if self.device.get_device_type() == 'SAGA':
            for idx, ch in enumerate(self.channels_default):
                # Connect checkboxes
                self.main_plotter.table_impedance_values._chb_channels[idx].clicked.connect(self._update_channels_status)
                # Uncheck and disable checkbox if channel is already disabled
                if hasattr(self, 'conversion_list'):
                    if idx in self.conversion_list:
                        ch = self.channels_default[self.conversion_list[idx-1]]
                if not ch._enabled:
                    self.main_plotter.table_impedance_values._chb_channels[idx].setChecked(False)
                    self.main_plotter.table_impedance_values._chb_channels[idx].setEnabled(False)
        else:
            channels=self.device.get_device_channels()
            for idx, ch in enumerate(self.channels_default):
                 # Connect checkboxes
                 self.main_plotter.table_impedance_values._chb_channels[idx].clicked.connect(self._update_channels_status)
                 # Uncheck and disable checkbox if channel is not in reference
                 if idx == 0 or not channels[idx-1]._is_reference:
                     self.main_plotter.table_impedance_values._chb_channels[idx].setChecked(False)
                     self.main_plotter.table_impedance_values._chb_channels[idx].setEnabled(False)
            self.remove_bad_channels = []
        self.disable_channels = []

    def monitor_function_saga(self):
        # Create dictionary
        reading=dict()
        reading["status"] = 200
        # Request latest reading 
        last_values = self.consumer_thread.original_buffer.get_last_value()
        if last_values is None:
            return reading
        # Place values in dictionary
        reading["impedances"] = []
        output_dict = dict()
        for i in range(len(last_values)):
             output_dict[i] = {"Re": last_values[i]}
        reading["impedances"] = collections.OrderedDict(output_dict.items())
        return reading
    
    def monitor_function_apex(self):
        # Create dictionary
        reading=dict()
        reading["status"] = 200
        # Request latest reading 
        last_values = self.consumer_thread.original_buffer.get_last_value()
        if last_values is None:
            return reading
        # Place values in dictionary
        reading["impedances"] = []
        output_dict = dict()
        for i in range(0,len(last_values),2):
             output_dict[i//2] = {"Re":last_values[i],"Im":last_values[i+1]}
        reading["impedances"] = collections.OrderedDict(output_dict.items())
        return reading
    
    def on_error(self, response):
        print("ERROR! {}".format(response))
    
    def start(self):
        # Initialize queue
        self.consumer = Consumer()
        # Initialize thread
        self.consumer_thread = self.consumer_thread_class(
            consumer_reading_queue=self.consumer.reading_queue,
            sample_rate=self.device.get_device_sampling_frequency())
        # Register device to sample data server and start reading samples
        self.consumer.open(
            server = self.device,
            reading_queue_id = self.device.get_id(),
            consumer_thread=self.consumer_thread)
        # Start measurement
        self.device.start_measurement(self.measurement_type)
        # Apply monitor function and send data to callback
        self.monitor = self.monitor_class(monitor_function = self.monitor_function, callback=self.callback, on_error=self.on_error)
        self.monitor.start()

    def stop(self):
        super().stop()
        if self.device.get_device_type() == 'SAGA':
            # Disable deselected channels
            if self.disable_channels:
                print('Disable channels:' )
                for ch in self.disable_channels:
                    print(self.channels_default[ch].get_channel_name())
            self.device.set_device_active_channels(self.disable_channels, False)
        elif self.device.get_device_type() == 'APEX':
            # Remove bad channels from reference
            if self.remove_bad_channels:
                print('Remove channels from reference:')
                channels = self.device.get_device_channels()
                for ch in self.remove_bad_channels:
                    if channels[ch]._is_reference:
                        print(channels[ch].get_channel_name())
                self.device.set_device_references(list_references = [0 if i in self.remove_bad_channels else 1 for i in range(len(channels))],
                                  list_indices = [i for i in range(len(channels))])
                
        if self._save_impedances:
            store_imp=[]

            for i in range(len(self.impedances)):
                if hasattr(self, 'conversion_list'):
                    if i in self.conversion_list:
                        i = self.conversion_list[i-1]
                store_imp.append(f"{self.channels_default[i].get_channel_name()}\t{self.impedances[i]}\t"+"kOhm")
    
            now = datetime.datetime.now()
            filetime = now.strftime("%Y%m%d_%H%M%S")
            filename = self._save_impedances + '-' + filetime
            
            with open(filename + '.txt', 'w') as f:
                for item in store_imp:
                    f.write(item + "\n")

    def _read_grid_info(self):
        file_dir = dirname(realpath(__file__)) # directory of this file
        # Get the HD-EMG conversion file
        config_file = join(file_dir, '../TMSiSDK/tmsi_resources', 'HD_EMG_grid_channel_configuration.json')
        
        # Open the file if it exists, notify the user if it does not
        if exists(config_file):
            # Get the HD-EMG conversion table
            with open(config_file) as json_file:
                self.conversion_data = json.load(json_file)
        else:
            self.conversion_data = []
            print("Couldn't load HD-EMG conversion file. Default channel order is used.")
    
    def _get_coordinates(self):
        # Get electrode positions and channel conversion list 
        if self.layout == 'head':
            if len(self.channels_default) < 32:
                coordinates = TMSiHeadcaps().headcaps["apex24"]
            elif len(self.channels_default) <64:
                coordinates = TMSiHeadcaps().headcaps["eeg32"]
            else:
                coordinates = TMSiHeadcaps().headcaps["eeg64"]
        else:              
            if self.layout in self.conversion_data:
                self.conversion_list= np.array(self.conversion_data[self.layout]['channel_conversion'])
            if len(self.channels_default)<64:
                if '6' in self.layout:
                    if self.layout[-1]=='2':
                        coordinates = TMSiGrids().grids["6-11-2"]
                    else:
                        coordinates = TMSiGrids().grids["6-11-1"]
                else:
                    coordinates = TMSiGrids().grids["4-8"]
            else:
                if '6' in self.layout:
                    if self.layout[-1]=='2':
                        coordinates = TMSiGrids().grids["6-11-2"]
                    else:
                        coordinates = TMSiGrids().grids["6-11"]
                else:
                    coordinates = TMSiGrids().grids["8-8"]

        return coordinates

    def _update_channels_status(self):
        # Get channel checkbox status
        channels_status = self.main_plotter.get_channels_status()
        
        if self.device.get_device_type() == 'SAGA':
            # Disable channels
            remove_bad_channels = []
            for ch in channels_status:
                if not channels_status[ch]['enabled']:
                    if hasattr(self, 'conversion_list'):
                        if ch in self.conversion_list:
                            ch = self.conversion_list[ch-1]
                        
                    if self.channels_default[ch]._enabled:
                        remove_bad_channels.append(ch)
            self.disable_channels=remove_bad_channels
        elif self.device.get_device_type() == 'APEX':
            # Remove channels from reference
            remove_bad_channels = []
            for ch in channels_status:
                if not channels_status[ch]['enabled'] and ch>0:
                    remove_bad_channels.append(ch-1)
            self.remove_bad_channels = remove_bad_channels
       
