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
 * @file ${signal_plotter_helper.py}
 * @brief This file is used as helper to make a signal plotter in the GUI
 *
 */   
'''

import numpy as np
from os.path import join, dirname, realpath, normpath, exists
import json

from TMSiFrontend.plotters.signal_plotter import SignalPlotter

from TMSiBackend.data_consumer.consumer import Consumer
from TMSiBackend.data_consumer.consumer_thread import ConsumerThread
from TMSiBackend.data_monitor.monitor import Monitor

from TMSiSDK.device.tmsi_device_enums import MeasurementType

from .plotter_helper import PlotterHelper

class SignalPlotterHelper(PlotterHelper):
    def __init__(self, device, grid_type = None):
        super().__init__(device = device, monitor_class = Monitor, consumer_thread_class = ConsumerThread) 
        self.main_plotter = SignalPlotter()
        self.grid_type = grid_type      

    def callback(self, response):
        pointer_data_to_plot = response.pointer_buffer
        data_to_plot = response.dataset
        # Wait untill data is coming in
        if data_to_plot is None:
            return
        size_dataset = np.shape(data_to_plot)[1]
        n_channels = np.shape(data_to_plot)[0]
        # add whitening zone 
        if pointer_data_to_plot != size_dataset:
            num_time_samples = self.sampling_frequency * self.main_plotter.window_size
            whitening_zone = int(self.whitening_zone * num_time_samples)
            space_to_fill = size_dataset - pointer_data_to_plot
            if space_to_fill < whitening_zone:
                data_to_plot[:, pointer_data_to_plot:] = \
                    np.full((n_channels, space_to_fill), np.nan)
            else:
                data_to_plot[:, pointer_data_to_plot:pointer_data_to_plot+whitening_zone] = \
                    np.full((n_channels, whitening_zone), np.nan)
        # Reorder data 
        # Send data to plotter and update chart
        self.main_plotter.update_chart(data_to_plot = data_to_plot[self.channel_conversion_list], time_span=self.time_span)

    def initialize(self):
        if self.device.get_device_type() == 'SAGA':
            self.measurement_type = MeasurementType.SAGA_SIGNAL
        elif self.device.get_device_type() == 'APEX':
            self.measurement_type = MeasurementType.APEX_SIGNAL
        self.whitening_zone = 0.02
        self.time_span = np.arange(0,10,1.0/self.sampling_frequency)

        self.channels_default =self.device.get_device_active_channels() 
        self._read_grid_info()    
        self._get_channel_conversion_list()
        # Reorder channels, reorders the channel names and controls;
        # Data is reordered in callback
        self.channels=[self.channels_default[idx] for idx in self.channel_conversion_list] 
        # Initialize components to control the plotting of the channels
        self.main_plotter.initialize_channels_components(self.channels)
        
    def monitor_function(self):
        return self.consumer_thread.original_buffer.copy()
    
    def on_error(self, response):
        print("ERROR! {}".format(response))
    
    def start(self):
        # Initialize queue
        self.consumer = Consumer()
        # Initialize thread
        self.consumer_thread = self.consumer_thread_class(
            consumer_reading_queue=self.consumer.reading_queue,
            sample_rate=self.device.get_device_sampling_frequency()
        )
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

    def _get_channel_conversion_list(self):
        if self.grid_type in self.conversion_data:
            # Read conversion list of the specified grid type
            conversion_list= np.array(self.conversion_data[self.grid_type]['channel_conversion'])

            # Check number of channels in grid
            if '4' in self.grid_type or self.grid_type[-1]=='1' or self.grid_type[-1]==2:
                nChan_grid=32
            else:
                nChan_grid=64

            # Check whether grid type can be used with device
            if self.device.get_num_channels() > nChan_grid:
                print('Use grid channel order of grid type ', self.grid_type)
                offset = 0
                #Add CREF channel and remove disabled channels, when present in conversion_list
                conversion_list = np.hstack((0, conversion_list))
                for ch_idx, ch in enumerate(self.device.get_device_channels()):
                    if not ch._enabled:
                        if ch_idx<(nChan_grid+1):
                            conversion_list = np.delete(conversion_list,(conversion_list == ch_idx-offset))
                            conversion_list[conversion_list>(ch_idx-offset)] = conversion_list[conversion_list>(ch_idx-offset)] - 1
                            offset = offset + 1

                # add other device channels
                self.channel_conversion_list = np.hstack((conversion_list, np.arange(len(conversion_list), len(self.channels_default),dtype=int)))
            else:
                print('Can not use ordening of 64channel grid on 32channel device. Default channel ordening is used.')
                self.channel_conversion_list = np.arange(len(self.channels_default), dtype=int)
        else:
            print('Default channel ordening is used.')
            self.channel_conversion_list = np.arange(len(self.channels_default), dtype=int)
    
