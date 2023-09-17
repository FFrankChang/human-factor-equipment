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
 * @file ${plotter_helper.py}
 * @brief This file is a general helper to make a plotter in the GUI
 *
 */
'''

class PlotterHelper:
    def __init__(self, device, monitor_class, consumer_thread_class):
        self.device = device
        self.sampling_frequency = self.device.get_device_sampling_frequency()
        self.monitor_class = monitor_class
        self.consumer_thread_class = consumer_thread_class
        

    def callback(self, response):
        print("callback plotter helper")
    
    def initialize(self):
        print("initialize function plotter helper")

    def monitor_function(self):
        print("monitor function plotter helper")

    def on_error(self, response):
        print("on_error plotter helper")

    def start(self, measurement_type):
        raise NotImplementedError("This method must be implemented for each plotter helper")

    def stop(self):
        self.monitor.stop()
        self.consumer.close()
        self.device.stop_measurement()
        