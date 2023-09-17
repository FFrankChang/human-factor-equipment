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
 * @file heatmap_plotter.py 
 * @brief 
 * HeatmapPlotter object.
 */


'''
from copy import deepcopy

from PySide2 import QtWidgets

from ..plotter import Plotter
from ..charts import HeatmapChart

class HeatmapPlotter(Plotter):
    "Heatmap plotter object"
    def __init__(self, device_type = "saga", is_headcap = False, name="Heat Map Plotter"):
        """Initialize Heatmap plotter

        :param electrodes: electrodes of the map, defaults to None
        :type electrodes: list, optional
        :param name: name of the plotter, defaults to "Heat Map Plotter"
        :type name: str, optional
        """
        super().__init__(name)
        self.chart = HeatmapChart(self.chart)
        if is_headcap:
            self.chart.draw_headcap()
    
    def set_electrode_position(self, channels, coordinates, reordered_indices = None):
        """Set position of the electode on the chart

        :param channels: list of channels
        :type channels: list
        :param coordinates: coordinates of the electrodes
        :type coordinates: TMSiGrids or TMSiHeadcaps
        :param reordered_indices: reordered indices, defaults to None
        :type reordered_indices: list, optional
        """
        self._reordered_grid = deepcopy(coordinates)
        self._reordered_channels = deepcopy(channels)
        self._reordered_indices = reordered_indices
        if self._reordered_indices:
            for i in range(len(self._reordered_indices)):
                self._reordered_grid[str(self._reordered_indices[i])] = coordinates[str(i + 1)]
        self.chart.place_electrodes(channels=self._reordered_channels, coordinates=self._reordered_grid)

    def _local_setup_ui(self):
        self.spin_amplitude.setValue(100)
        self.spin_amplitude.valueChanged.connect(self._slider_value_changed)
        self.frame_colormap = QtWidgets.QFrame(self.frame_sidebar)
        self.colormap_layout = QtWidgets.QHBoxLayout(self.frame_colormap)
        self.colormap_layout.setObjectName(u"colormap_layout")
        self.radio_rainbow = QtWidgets.QRadioButton(self.frame_colormap)
        self.radio_rainbow.setObjectName(u"radio_rainbow")
        self.radio_rainbow.setText("Rainbow")
        self.radio_rainbow.setChecked(True)
        self.radio_rainbow.toggled.connect(lambda: self._colormap_style_changed("CET-R4", self.radio_rainbow))
        self.radio_heat = QtWidgets.QRadioButton(self.frame_colormap)
        self.radio_heat.setObjectName(u"radio_heat")
        self.radio_heat.setText("Heat")
        self.radio_heat.setChecked(False)
        self.radio_heat.toggled.connect(lambda: self._colormap_style_changed("CET-L4", self.radio_heat))
        self.radio_differential = QtWidgets.QRadioButton(self.frame_colormap)
        self.radio_differential.setObjectName(u"radio_differential")
        self.radio_differential.setText("Differential")
        self.radio_differential.setChecked(False)
        self.radio_differential.toggled.connect(lambda: self._colormap_style_changed("CET-D4", self.radio_differential))
        self.colormap_layout.insertWidget(0, self.radio_rainbow)
        self.colormap_layout.insertWidget(0, self.radio_heat)
        self.colormap_layout.insertWidget(0, self.radio_differential)
        self.verticalLayout.insertWidget(1, self.frame_colormap)
        self.btn_freeze.setVisible(False)
        self.btn_freeze.setVisible(False)
        self.group_channels.setVisible(False)
        self.group_channels.setEnabled(False)
        self.scrollArea.setStyleSheet("border: none;")
        
    def _colormap_style_changed(self, style, radio):
        if radio.isChecked():
            self.chart.update_cm(style)
        
    def _slider_value_changed(self):
        self.chart.update_bar(self.spin_amplitude.value())