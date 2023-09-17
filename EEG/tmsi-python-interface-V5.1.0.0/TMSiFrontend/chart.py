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
 * @file chart.py 
 * @brief 
 * Chart object
 */


'''
import datetime
import os
from sys import platform
if platform == "win32":
    import ctypes.wintypes

import pyqtgraph.exporters as exporters

class Chart:
    """Chart interface
    """
    def __init__(self, plotter_chart):
        """Initialize chart

        :param plotter_chart: widget where the chart is going to lay.
        :type plotter_chart: QWidget
        """
        self._plotter_chart = plotter_chart
        self._plotter_chart.scene().sigMouseMoved.connect(self._on_mouse_move)
        self.initUI()
        self.tmsi_folder = self._initialize_folder(os.path.join(self._get_documents_path(), "TMSi"))
        self.tmsi_images_folder = self._initialize_folder(os.path.join(self.tmsi_folder,"Images"))

    def initUI(self):
        """Initialize the UI
        """
        pass

    def snap(self):
        """Export the image of the chart
        """
        exporter = exporters.ImageExporter(self._plotter_chart.window)
        exporter.export(os.path.join(self.tmsi_images_folder,"snap-{}.png".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))))

    def update_chart(self, data_to_plot):
        """Update chart with ner data

        :param data_to_plot: data to be plotted
        :type data_to_plot: list[list]
        """
        pass

    def _initialize_folder(self, path):
        if not os.path.exists(path):
                os.makedirs(path)
        return path

    def _get_documents_path(self):
        CSIDL_PERSONAL = 5
        SHGFP_TYPE_CURRENT = 0
        buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        return buf.value

    def _on_mouse_move(self, evt):
        mouse_point = self._plotter_chart.window.vb.mapSceneToView(evt)
        x, y = mouse_point.x(), mouse_point.y()
        channel = round(y / self._plot_offset)