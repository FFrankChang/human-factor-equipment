'''
Copyright 2021 John Veillette (https://gitlab.com/john-veillette)
(c) 2022 Twente Medical Systems International B.V., Oldenzaal The Netherlands

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
 * @file ${lsl_stream_writer.py} 
 * @brief Labstreaminglayer Writer
 *
 */


'''

import sys
from datetime import datetime
import os
import struct
import time
from pylsl import StreamInfo, StreamOutlet, local_clock

from TMSiSDK.device.tmsi_device import TMSiDevice
from TMSiSDK.sample_data_server.sample_data_server import SampleDataServer 
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode, DeviceErrorLookupTable
from TMSiSDK.device import ChannelType

class LSLConsumer:
    '''
    Provides the .put() method expected by TMSiSDK.sample_data_server

    liblsl will handle the data buffer in a seperate thread. Since liblsl can
    bypass the global interpreter lock and python can't, and lsl uses faster
    compiled code, it's better to offload this than to create our own thread.
    '''

    def __init__(self, lsl_outlet):
        self._outlet = lsl_outlet

    def put(self, sd):
        '''
        Pushes sample data to pylsl outlet, which handles the data buffer

        sd (TMSiSDK.sample_data.SampleData): provided by the sample data server
        '''
        try:
            # split into list of arrays for each sampling event
            signals = [sd.samples[i*sd.num_samples_per_sample_set : \
                                (i+1)*sd.num_samples_per_sample_set] \
                                    for i in range(sd.num_sample_sets)]
            # and push to LSL
            self._outlet.push_chunk(signals, local_clock())
        except:
            raise TMSiError(TMSiErrorCode.file_writer_error)

class LSLWriter:
    '''
    A drop-in replacement for a TSMiSDK filewriter object
    that streams data to labstreaminglayer
    '''

    def __init__(self, stream_name = ''):

        self._name = stream_name if stream_name else 'tmsi'
        self._consumer = None
        self.device = None
        self._date = None
        self._outlet = None


    def open(self, device):
        '''
        Input is an open TMSiSDK device object
        '''

        self.device = device
        print("LSLWriter-open")

        try:
            self._date = datetime.now()
            self._sample_rate = self.device.get_device_sampling_frequency()
            self._num_channels = self.device.get_num_active_channels()
        
            # Calculate nr of sample-sets within one sample-data-block:
            # This is the nr of sample-sets in 150 milli-seconds or when the
            # sample-data-block-size exceeds 64kb the it will become the nr of
            # sample-sets that fit in 64kb
            self._num_sample_sets_per_sample_data_block = int(self._sample_rate * 0.15)
            size_one_sample_set = self._num_channels * 4
            if ((self._num_sample_sets_per_sample_data_block * size_one_sample_set) > 64000):
                self._num_sample_sets_per_sample_data_block = int(64000 / size_one_sample_set)
        
            # provide LSL with metadata
            info = StreamInfo(
                self._name,
                'EEG',
                self._num_channels,
                self._sample_rate,
                'float32',
                'tmsi-' + str(self.device.get_device_serial_number()), 
                ) 
            chns = info.desc().append_child("channels")
            for idx, ch in enumerate(self.device.get_device_active_channels()): # active channels
                 chn = chns.append_child("channel")
                 chn.append_child_value("label", ch.get_channel_name())
                 chn.append_child_value("index", str(idx))
                 chn.append_child_value("unit", ch.get_channel_unit_name())
                 if (ch.get_channel_type().value == ChannelType.UNI.value) and not ch.get_channel_name()=='CREF':
                     chn.append_child_value("type", 'EEG')
                 elif (ch.get_channel_type().value == ChannelType.status.value):
                     chn.append_child_value("type", 'STATUS')
                 elif (ch.get_channel_type().value == ChannelType.counter.value):
                     chn.append_child_value("type", 'COUNTER')
                 else:
                     chn.append_child_value("type", '-')
            info.desc().append_child_value("manufacturer", "TMSi")
            sync = info.desc().append_child("synchronization")
            sync.append_child_value("offset_mean", str(0.0335)) 
            sync.append_child_value("offset_std", str(0.0008)) # jitter AFTER jitter correction by pyxdf
        
            # start sampling data and pushing to LSL
            self._outlet = StreamOutlet(info, self._num_sample_sets_per_sample_data_block)
            self._consumer = LSLConsumer(self._outlet)
            SampleDataServer().register_consumer(self.device.get_id(), self._consumer)
            
        except:
            raise TMSiError(TMSiErrorCode.file_writer_error)




    def close(self):

        print("LSLWriter-close")
        SampleDataServer().unregister_consumer(self.device.get_id(), self._consumer)
        # let garbage collector take care of destroying LSL outlet
        self._consumer = None
        self._outlet = None
