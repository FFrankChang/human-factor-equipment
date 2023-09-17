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
 * @file buffer.py 
 * @brief 
 * A buffer to keep data coming from the devices.
 */


'''

import numpy as np


class Buffer:
    """Class to handle circular buffer of data.
    """
    def __init__(self, size: int):
        """Constructor of the buffer.

        :param size: maximum number of samples per channel.
        :type size: int
        """
        self.size_buffer = int(size)
        self.pointer_buffer = 0

    def copy(self) -> 'Buffer':
        """Return a copy of the buffer.

        :return: a copy of the buffer.
        :rtype: Buffer
        """
        buffer_copy = Buffer(self.size_buffer)
        buffer_copy.pointer_buffer = self.pointer_buffer
        buffer_copy.dataset = self.dataset.copy() if hasattr(self, "dataset") else None
        return buffer_copy

    def get_last_value(self) -> list:
        """Return the last value received of each chanel.

        :return: last value received of each channel.
        :rtype: list[int]
        """
        if hasattr(self, "dataset"):
            try:    
                return self.dataset[:,self.pointer_buffer - 1]
            except:
                return []

    def append(self, samples):
        """Append new data to the buffer.

        :param samples: samples to append.
        :type samples: 2D list
        """
        if not hasattr(self, "dataset"):
            self.dataset = np.array([[]] * np.shape(samples)[0])

        samples_chunk = np.shape(samples)[1]

        if np.shape(self.dataset)[1] < self.size_buffer:  # still filling the dataset
            # if the new datapack does not overflow the buffersize
            if self.pointer_buffer + samples_chunk <= self.size_buffer:
                self.dataset = np.append(self.dataset, samples, 1)
                self.pointer_buffer += samples_chunk
            else:  # i need to break the datapack and loop
                first_chunk = self.size_buffer - self.pointer_buffer
                second_chunk = samples_chunk - first_chunk
                self.dataset = np.append(
                    self.dataset, samples[:, 0:first_chunk], 1)
                self.dataset[:,
                             0:second_chunk] = samples[:,
                                                       first_chunk:samples_chunk]
                self.pointer_buffer = second_chunk
        else:  # replacing old data
            # if the new datapack does not overflow the buffersize
            if self.pointer_buffer + samples_chunk <= self.size_buffer:
                self.dataset[:, self.pointer_buffer:self.pointer_buffer +
                             samples_chunk] = samples[:, :]
                self.pointer_buffer += samples_chunk
            else:  # i need to break the datapack and loop
                first_chunk = self.size_buffer - self.pointer_buffer
                second_chunk = samples_chunk - first_chunk
                if first_chunk > 0:
                    self.dataset[:,
                             self.pointer_buffer:self.size_buffer] = samples[:,
                                                                             0:first_chunk]
                if second_chunk > 0:
                    self.dataset[:,
                             0:second_chunk] = samples[:,
                                                       first_chunk:samples_chunk]
                self.pointer_buffer = second_chunk