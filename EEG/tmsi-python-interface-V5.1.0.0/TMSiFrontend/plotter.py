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
 * @file plotter.py 
 * @brief 
 * Plotter object
 */


'''
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QSize

from .designer._plotter import Ui_Plotter
from .chart import Chart
from .utilities.tmsi_style import TMSiStyle

MAX_SIZE = 16777215
MAX_SIZE_SIDEBAR = 300
MIN_SIZE_SIDEBAR = 45
HEIGHT_BUTTON = 38

class Plotter(QtWidgets.QWidget, Ui_Plotter):
    """Plotter interface
    """
    def __init__(self, name = "Plotter"):
        """Initialize Plotter

        :param name: name of the plotter, defaults to "Plotter"
        :type name: str, optional
        """
        super().__init__()
        self._max_side_bar = MAX_SIZE_SIDEBAR
        self._name = name
        self.setupUi(self)
        self.label_logo.setPixmap(QtGui.QPixmap(u"TMSiFrontend/media/images/TMSi_logo.PNG"))
        self.setStyleSheet(TMSiStyle)
        self._local_setup_ui()
        self.legend.setVisible(False)
        self.lbl_sidebar_title.setText("")
        self.btn_hide_sidebar.clicked.connect(self.toggle_sidebar)
        self.btn_freeze.clicked.connect(self._enable_update_chart)
        self.is_chart_update_enabled = True
        self._enabled_channels = []
        self._scales = {}
        self._offsets = {}

    def toggle_sidebar(self):
        """Toggle the visibility of the sidebar
        """
        set_visible = not self.scrollArea.isVisible()
        for widget in self.frame_sidebar.children():
            if widget.objectName() == "lbl_sidebar_title":
                if set_visible:
                    widget.setMaximumHeight(0)
                else:
                    widget.setMaximumHeight(MAX_SIZE)
                continue
            if widget.objectName() == "btn_hide_sidebar":
                if set_visible:
                    widget.setText("<<")
                    self.frame_sidebar.setMaximumSize(QSize(self._max_side_bar, MAX_SIZE))
                    self.frame_sidebar.setMinimumSize(QSize(self._max_side_bar, MAX_SIZE))
                    self.btn_hide_sidebar.setMinimumSize(QSize(self._max_side_bar-2,HEIGHT_BUTTON))
                    self.btn_hide_sidebar.setMaximumSize(QSize(self._max_side_bar-2,HEIGHT_BUTTON))
                else:
                    widget.setText(">>")
                    self.frame_sidebar.setMaximumSize(QSize(MIN_SIZE_SIDEBAR, MAX_SIZE))
                    self.frame_sidebar.setMinimumSize(QSize(MIN_SIZE_SIDEBAR, MAX_SIZE))
                    self.btn_hide_sidebar.setMinimumSize(QSize(MIN_SIZE_SIDEBAR-2,HEIGHT_BUTTON))
                    self.btn_hide_sidebar.setMaximumSize(QSize(MIN_SIZE_SIDEBAR-2,HEIGHT_BUTTON))
                continue
            if hasattr(widget,"setVisible"):
                if widget.isEnabled():
                    widget.setVisible(set_visible)
            

    def update_chart(self, data_to_plot):
        """Update chart with data

        :param data_to_plot: data to be plotted
        :type data_to_plot: list[list]
        """
        if not self.is_chart_update_enabled:
            return
        self.chart.update_chart(data_to_plot)
    
    def _enable_update_chart(self):
        if self.is_chart_update_enabled:
            self.chart.snap()
        self.is_chart_update_enabled = not self.is_chart_update_enabled
        if self.is_chart_update_enabled:
            self.btn_freeze.setText("Pause Viewer")
        else:
            self.btn_freeze.setText("Continue Viewer")
            
    def _local_setup_ui(self):
        return