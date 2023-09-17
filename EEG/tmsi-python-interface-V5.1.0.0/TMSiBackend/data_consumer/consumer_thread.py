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
 * @file consumer_thread.py 
 * @brief 
 * Class to handle the thread of the consumer.
 */


'''

import threading
import numpy as np

from TMSiSDK.tmsi_utilities.support_functions import array_to_matrix as Reshape

from ..buffer import Buffer

class ConsumerThread(threading.Thread):
    def __init__(self, consumer_reading_queue, sample_rate):
        super().__init__()
        self.consumer_reading_queue = consumer_reading_queue
        self.sampling = False
        self.sample_rate = sample_rate
        self.original_buffer = Buffer(sample_rate * 10)

    def process(self, sample_data):
        reshaped = np.array(Reshape(sample_data.samples, sample_data.num_samples_per_sample_set))
        self.original_buffer.append(reshaped)

    def run(self):
        self.sampling = True
        while self.sampling or (not self.consumer_reading_queue.empty()):
            sample_data = self.consumer_reading_queue.get()
            self.consumer_reading_queue.task_done()
            self.process(sample_data)

    def stop_sampling(self):
        self.sampling = False