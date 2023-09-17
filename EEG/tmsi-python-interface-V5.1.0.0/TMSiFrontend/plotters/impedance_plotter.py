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
 * @file impedance_plotter.py 
 * @brief 
 * ImpedancePlotter object.
 */


'''
from copy import deepcopy

from PySide2 import QtWidgets

from ..plotter import Plotter
from ..charts import ImpedanceChart
from ..legends.impedance_legend import ImpedanceLegend
from ..components import TableImpedanceValues

class ImpedancePlotter(Plotter):
    """ImpedancePlotter object"""
    def __init__(self, device_type = "saga", is_headcap = False, name = "Impedance Plotter"):
        """Initialize impedance plotter

        :param device_type: devuce type. saga or apex
        :type device_type: str, optional
        :param is_headcap: show or not the head on the background, defaults to True
        :type is_headcap: bool, optional
        :param name: name of the plotter, defaults to "Impedance Plotter"
        :type name: str, optional
        """
        super().__init__(name = name)
        self._device_type = device_type
        self.legend = ImpedanceLegend(legend_chart = self.legend, device_type = device_type)
        self.legend.setVisible(True)
        self.chart = ImpedanceChart(plotter_chart = self.chart, legend = self.legend, head_enabled = is_headcap)
        self.verticalSpacer.changeSize(20, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    def get_channels_status(self):
        """Get channels status from the table

        :return: return the status of the channel in the table (checked or not)
        :rtype: dict()
        """
        return self.table_impedance_values.get_channels_status()

    def initialize_table_impedance_values(self, channels):
        """Initialize the table of impedances

        :param channels: list of impedance channels
        :type channels: list
        """
        self.table_impedance_values.set_channels(channels = channels)

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
                self._reordered_channels[i + 1] = channels[self._reordered_indices[i]]
        self.chart.place_electrodes(channels=self._reordered_channels, coordinates=self._reordered_grid)
        self.initialize_table_impedance_values(channels = self._reordered_channels)

    def update_chart(self, data_to_plot):
        """Update chart

        :param data_to_plot: data to be plotted
        :type data_to_plot: list
        """
        super().update_chart(data_to_plot)
        if self._reordered_indices:
            reordered_values = [data_to_plot[i.get_channel_index()] for i in self._reordered_channels]
        else:
            reordered_values = data_to_plot
        self.table_impedance_values.set_values(values = reordered_values)

    def _local_setup_ui(self):
        self.group_amplitude.setVisible(False)
        self.btn_freeze.setVisible(False)
        self.group_channels.setVisible(False)
        self.group_amplitude.setEnabled(False)
        self.btn_freeze.setEnabled(False)
        self.group_channels.setEnabled(False)
        self.frame_sidebar.setMinimumWidth(600)
        self._max_side_bar = 600
        self.horizontalSpacer_logo1.changeSize(216,20)
        self.table_impedance_values = TableImpedanceValues(
            layout = self.layout_channels,
            widget = self.scrollAreaWidgetContents)