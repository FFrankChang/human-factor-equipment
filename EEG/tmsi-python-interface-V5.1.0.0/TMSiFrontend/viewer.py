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
 * @file viewer.py 
 * @brief 
 * Viewer object
 */


'''
import math
import numpy as np

from PySide2 import QtWidgets

from .designer._viewer import Ui_Viewer
from . import plotters

SCROLL_RATIO = 10.0

class Viewer(QtWidgets.QWidget, Ui_Viewer):
    """Viewer interface
    """
    def __init__(self, reader, name = "Viewer"):
        """Initialize Viewer

        :param reader: file reader to use
        :type reader: TMSiReader
        :param name: name of the viewer, defaults to "Viewer"
        :type name: str, optional
        """
        super().__init__()
        self._reader = reader
        self._name = name
        self.slider_pressed = False
        self.setupUi(self)
        self._local_setup_ui()
        self.main_plotter.btn_freeze.setVisible(False)
        self.main_plotter.initialize_channels_components(self._reader.get_reader_channels())
        self._update_time_scroll_bar()

    def zoom_in(self):
        """Zooms in the time scale.
        """
        time_scale = self.main_plotter.window_size // 2
        if time_scale < 1:
            time_scale = 1
        self.main_plotter.window_size = time_scale
        self.main_plotter.chart.set_time_range(self.main_plotter.window_size)
        self._update_time_scroll_bar(new_value = self.time_scrollbar.value() * 2)

    def zoom_out(self):
        """Zooms out the time scale
        """
        time_scale = self.main_plotter.window_size * 2
        if time_scale > 100:
            time_scale = 100
        if time_scale > self.total_time:
            time_scale = self.total_time
        self.main_plotter.window_size = time_scale
        self.main_plotter.chart.set_time_range(self.main_plotter.window_size)
        self._update_time_scroll_bar(new_value = self.time_scrollbar.value() // 2)
        
    def _local_setup_ui(self):
        self.main_plotter = plotters.SignalPlotter(get_data_callback = self._update_data)
        self.layout_frame_plotter.insertWidget(0, self.main_plotter)
        self.main_plotter.window_size = 5
        self.main_plotter.chart.set_time_range(self.main_plotter.window_size)
        self.time_scrollbar.valueChanged.connect(self._scroll_value_changed)
        self.total_time = self._reader.get_reader_number_of_samples() / self._reader.get_reader_sampling_frequency()

    def _scroll_slider_pressed(self):
        self.slider_pressed = True
        
    def _scroll_slider_released(self):
        self.slider_pressed = False
        self._update_data()

    def _scroll_value_changed(self):
        if self.slider_pressed:
            return
        self._update_data()

    def _update_data(self):
        start_time = self.time_scrollbar.value() * self.main_plotter.window_size
        start_time = start_time / SCROLL_RATIO
        start_time -= 1.0 / SCROLL_RATIO * self.main_plotter.window_size
        if start_time < 0:
            start_time = 0
        start_time = round(start_time, 2)
        end_time = start_time + self.main_plotter.window_size
        matrix = self._reader.get_reader_data(start_time, end_time)
        matrix = np.array(matrix)
        time_span = np.arange(0 , end_time - start_time, 1.0/self._reader.get_reader_sampling_frequency())
        self.main_plotter.update_chart(data_to_plot = matrix[:][0:len(time_span)], time_span = time_span)
        self.main_plotter.update_time_ticks(start_time = start_time, end_time = end_time)
        
    def _update_time_scroll_bar(self, new_value = None):
        self.time_scrollbar.setMinimum(1)
        self.time_scrollbar.setMaximum(math.ceil((self.total_time - self.main_plotter.window_size) / self.main_plotter.window_size * SCROLL_RATIO) + 2)
        if new_value is None:
            self._update_data()
            return
        self.time_scrollbar.setValue(new_value)

    