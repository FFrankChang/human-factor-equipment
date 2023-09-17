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
 * @file consumer.py 
 * @brief 
 * Consumer object.
 */


'''

import queue

from TMSiSDK.sample_data_server import SampleDataServer
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode

class Consumer:
    def __init__(self):
        self.reading_queue = queue.Queue(1000)
        self.consumer_thread = None
        
    def close(self):
        if self.consumer_thread is not None:
            self.consumer_thread.stop_sampling()
            self.consumer_thread.join()
            
        SampleDataServer().unregister_consumer(self.reading_queue_id, self)
    
    def open(self, server, reading_queue_id, consumer_thread):
        self.server = server
        self.reading_queue_id = reading_queue_id
        try:
            SampleDataServer().register_consumer(self.reading_queue_id, self)
            self.consumer_thread = consumer_thread
            self.consumer_thread.start()
        except OSError as e:
            raise TMSiError(TMSiErrorCode.file_writer_error)
        except Exception as e:
            raise TMSiError(TMSiErrorCode.file_writer_error)
        
    def put(self, sample_data):
        try:
            self.reading_queue.put(sample_data)
        except:
            raise TMSiError(TMSiErrorCode.file_writer_error)