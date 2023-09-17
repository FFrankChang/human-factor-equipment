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
 * @file ${envelope_plotter_helper.py}
 * @brief Plotter helper for creating an envelope plotter for EMG purposes.
 * More information about how to make your own plotters can be found in the documentation.
 *
 */
''' 

# Import relevant toolboxes and classes 
from scipy import signal
import numpy as np

from TMSiFrontend.plotters.signal_plotter import SignalPlotter

from TMSiBackend.data_consumer.consumer_thread import ConsumerThread
from TMSiBackend.data_consumer.consumer import Consumer
from TMSiBackend.buffer import Buffer
from TMSiBackend.data_monitor.monitor import Monitor

from TMSiSDK.tmsi_utilities.support_functions import array_to_matrix as Reshape

from .signal_plotter_helper import SignalPlotterHelper


class EnvelopeSignalPlotterHelper(SignalPlotterHelper):
    """ Plotter helper class to plot the signals as envelopes in the viewer for EMG measurements

        :param grid_type: type of grid that is used, defaults to None
        :param bpf_fc1: lower limit of the cut-off frequency of the bandpassfilter, defaults to 10
        :type bpf_fc1: int, optional
        :param bpf_fc2: upper limit of the cut-off frequency of the bandpassfilter, defaults to 500
        :type bpf_fc2: int, optional
        :param lpf_fc: cut-off frequency for the low-pass filter for smoothing
        :type lpf_fc: int, optional
        :param order: order of the filters
        :type order: int, optional
    """
    def __init__(self,  device, grid_type = None, bpf_fc1 = 10, bpf_fc2 = 500, lpf_fc = 10, order = 1):
        # call super of SignalAcquisitionHelper
        super(SignalPlotterHelper, self).__init__(device = device, monitor_class = Monitor, consumer_thread_class = EnvelopeConsumerThread)
        self.main_plotter = SignalPlotter()
        self.grid_type = grid_type
        self.bpf_fc1 = bpf_fc1
        self.bpf_fc2 = bpf_fc2
        self.lpf_fc = lpf_fc
        self.order = order

    def start(self):
        self.consumer = Consumer()
        self.consumer_thread = self.consumer_thread_class(
            consumer_reading_queue=self.consumer.reading_queue,
            sample_rate=self.device.get_device_sampling_frequency()
        )
        # Initialize filter
        self.consumer_thread.initialize_filter(bpf_fc1 = self.bpf_fc1, bpf_fc2 = self.bpf_fc2, lpf_fc = self.lpf_fc, order = self.order)
        self.consumer.open(
            server = self.device,
            reading_queue_id = self.device.get_id(),
            consumer_thread=self.consumer_thread)
        # Start measurement
        self.device.start_measurement(self.measurement_type)
        self.monitor = self.monitor_class(monitor_function = self.monitor_function, callback=self.callback, on_error=self.on_error)
        self.monitor.start()


    def monitor_function(self):
        return self.consumer_thread.filtered_buffer.copy()


class EnvelopeConsumerThread(ConsumerThread):
    """ Class to process the data for the plotter
    """
    def __init__(self, consumer_reading_queue, sample_rate):
        super().__init__(consumer_reading_queue, sample_rate)
        self.filtered_buffer = Buffer(sample_rate * 10)
    
    def initialize_filter(self, bpf_fc1 = 10, bpf_fc2 = 500, lpf_fc = 10, order = 1):
        """Initializes the bandpass and lowpass filter to be applied.

        :param bpf_fc1: lower limit of the cut-off frequency of the bandpassfilter, defaults to 10
        :type bpf_fc1: int, optional
        :param bpf_fc2: upper limit of the cut-off frequency of the bandpassfilter, defaults to 500
        :type bpf_fc2: int, optional
        :param lpf_fc: cut-off frequency for the low-pass filter for smoothing
        :type lpf_fc: int, optional
        :param order: order of the filters
        :type order: int, optional
        """
        # Check if band pass filter cut off frequency is within limits
        if (bpf_fc2 > self.sample_rate/2) or (bpf_fc2 == self.sample_rate/2):
            bpf_fc2 = (self.sample_rate-100)/2
            print('Cut-off of bandpass filter was adjusted due to Nyquist frequency, it is now: ', bpf_fc2, ' Hz')
        else:
            bpf_fc2 = bpf_fc2
            
        self._sos_lpf = signal.butter(order, lpf_fc, 'lowpass', fs = self.sample_rate, output='sos')
        self._sos_bpf = signal.butter(order, [bpf_fc1, bpf_fc2], 'bandpass', fs=self.sample_rate, output='sos')

    def process(self, sample_data):
        reshaped = np.array(Reshape(sample_data.samples, sample_data.num_samples_per_sample_set))
        # Update original buffer
        self.original_buffer.append(reshaped)
        # Do not filter if no filter is present
        if not hasattr(self, "_sos_lpf") or self._sos_lpf is None:
            self.filtered_buffer.append(reshaped)
            return None
        # Construct initial conditions for both filters
        if not hasattr(self, "_z_sos_lpf"):
            self._z_sos_lpf0 = signal.sosfilt_zi(self._sos_lpf)
            self._z_sos_lpf = np.repeat(
                self._z_sos_lpf0[:, np.newaxis, :], np.shape(reshaped)[0], axis=1)
            self._z_sos_bpf0 = signal.sosfilt_zi(self._sos_bpf)
            self._z_sos_bpf = np.repeat(
                self._z_sos_bpf0[:, np.newaxis, :], np.shape(reshaped)[0], axis=1)
        
        # 1. Bandpass filter the data
        filtered_bpf, self._z_sos_bpf = self.__filter(reshaped, self._sos_bpf, self._z_sos_bpf)
        # Do not filter STATUS and COUNTER channel
        filtered_bpf[-2] = reshaped[-2]
        filtered_bpf[-1] = reshaped[-1]

        # 2. Rectify the signal
        rectified_samples = np.abs(filtered_bpf)
        rectified_samples[-2] = reshaped[-2]
        rectified_samples[-1] = reshaped[-1]

        # 3. Smoothen envelope: low pass filter
        envelope, self._z_sos_lpf = self.__filter(rectified_samples, self._sos_lpf, self._z_sos_lpf)
        envelope[-2] = reshaped[-2]
        envelope[-1] = reshaped[-1]

        # Store samples in the filtered buffer to show
        self.filtered_buffer.append(envelope)

    def __filter(self, reshaped, sos, z_sos):
        filtered, z_sos = signal.sosfilt(
                sos, reshaped, zi=z_sos)
        return filtered, z_sos

    