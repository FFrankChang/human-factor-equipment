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
 * @file ${differential_signal_plotter_helper.py}
 * @brief Plotter helper for creating a differential plotter for HD-EMG purposes.
 *  The plotter plots the difference between successive electrode based on 
 * channel names.
 *
 */
''' 

import numpy as np 
from operator import itemgetter

from TMSiFrontend.plotters.signal_plotter import SignalPlotter

from .filtered_signal_plotter_helper import FilteredSignalPlotterHelper

class DifferentialSignalPlotterHelper(FilteredSignalPlotterHelper):
    def __init__(self, device, grid_type=None, hpf=0, lpf=0, order=1):
        super().__init__(device=device, grid_type=grid_type, hpf=hpf, lpf=lpf, order=order)
        self.plotter2 = SignalPlotter()
    
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
        # Send data to plotter and update chart
        self.main_plotter.update_chart(data_to_plot = data_to_plot[self.channel_conversion_list], time_span=self.time_span)
        
        # Update plotter2 depending on refresh rate
        if self.main_plotter_refresh_counter % self.plotter2_refresh_rate == 0:
            if size_dataset < response.size_buffer:
                data_to_return = np.empty((n_channels, response.size_buffer))
                data_to_return[:] = np.nan
                data_to_return[:,response.size_buffer - pointer_data_to_plot:] = data_to_plot[:,:pointer_data_to_plot]
            else:
                # Flip data such that the newest data is on the end
                data_to_return = np.ones_like(data_to_plot)
                data_to_return[:,size_dataset - pointer_data_to_plot:] = data_to_plot[:,:pointer_data_to_plot]
                data_to_return[:,:size_dataset - pointer_data_to_plot] = data_to_plot[:,pointer_data_to_plot:]
            
            # Calculate differential data
            SD_data = np.matmul(self.SD_matrix, data_to_return[:,-len(self.differential_time_span):])
            # Send data to plotter and update chart
            self.plotter2.update_chart(data_to_plot = SD_data, time_span=self.differential_time_span)
        self.main_plotter_refresh_counter += 1

    def initialize(self):
        super().initialize()
        # Set time span of secondary window to 0.2 s
        self.plotter2.chart.set_time_min_max(0, 0.2)
        self.differential_time_span = np.arange(0,0.2,1.0/self.sampling_frequency)
        # Set refresh rate to update every 10 times (=1Hz) to have readible signals
        self.plotter2_refresh_rate = 10
        self.main_plotter_refresh_counter = 0
        # Generate single differential matrix and corresponding channel names
        self.SD_matrix, ch_names_diff = self.get_single_differential_matrix()

        # Get type of channels instance
        SignalType = self.channels[0].__class__
        # Generate channels list with differential channel names
        differential_signals = []
        for i in ch_names_diff:
            sig = SignalType()
            sig.set_channel_name(alternative_channel_name= i)
            differential_signals.append(sig)
        # Initialize channel components
        self.plotter2.initialize_channels_components(differential_signals)


    def _get_grid_order(self):
        # Detect row and column number based on channel name 
        RC_order = []
        for i, ch in enumerate(self.channels_default):
            if ch.get_channel_name().find('R') == 0:
                R,C = ch.get_channel_name()[1:].split('C')
                RC_order.append((int(R),int(C),i))

        RC_order.sort()     
        
        # Create matrix with channel number for each position
        RC_matrix=np.zeros((max(RC_order, key=itemgetter(0))[0],max(RC_order, key=itemgetter(1))[1]))*np.nan
        for i in range(len(RC_order)):
            R,C, ch = RC_order[i]
            R = R - 1
            C = C - 1
            RC_matrix[R,C] = ch
            
        return RC_order, RC_matrix
        
    def get_single_differential_matrix(self):
        RC_order, RC_matrix = self._get_grid_order()
        
        # Initialize channel names
        ch_names_diff = ['R1C1 - R1C2']
        skip = 0
        # Single differential matrix
        SD_matrix = np.zeros((np.shape(RC_matrix)[0]*(np.shape(RC_matrix)[1]-1), len(self.device.get_device_active_channels())))
        n_C = np.shape(RC_matrix)[1]-1
        for r in range(0, max(RC_order, key=itemgetter(0))[0]):
            for c in range(0, max(RC_order, key=itemgetter(1))[1]-1):
                # If channel RC and R(C+1) are available, 
                # RC - R(C+1) 
                # SD = np.matmul(SD_matrix. samples) 
                if not np.isnan(RC_matrix[r,c]) and not np.isnan(RC_matrix[r,c+1]):
                    SD_matrix[n_C*r + c - skip, int(RC_matrix[r,c])] = 1
                    SD_matrix[n_C*r + c -skip, int(RC_matrix[r,c+1])] = -1
                    # Create channel name
                    ch_names_diff = np.vstack((ch_names_diff, 'R'+str(r+1)+'C'+str(c+1) + ' - ' + 'R'+str(r+1)+'C'+str(c+2)))
                else:
                    # Delete row when not available
                    SD_matrix = np.delete(SD_matrix, n_C*r + c-skip, 0)
                    skip = skip + 1 
        # Remove initial channel name
        ch_names_diff = ch_names_diff[1:,:]
        return SD_matrix, ch_names_diff