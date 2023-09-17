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
 * @file impedance_chart.py 
 * @brief 
 * Impedance Chart object
 */


'''
import math

import numpy as np
import pyqtgraph as pg
from PySide2 import  QtGui

from ..chart import Chart
from ..legends.impedance_legend import ImpedanceLegend

class Electrode:
    """Electrode Object"""
    def __init__(self, channel, coordinates, cartesian):
        self.channel = channel
        if cartesian:
            self.x = coordinates[0]
            self.y = coordinates[1]
        else:
            self.x = coordinates["radius"] * np.sin(np.deg2rad(coordinates["angle"]))
            self.y = coordinates["radius"] * np.cos(np.deg2rad(coordinates["angle"]))

class ImpedanceChart(Chart):
    """ImpedanceChart object"""
    def __init__(self, plotter_chart, legend, head_enabled = True):
        """Initialize impedance chart

        :param plotter_chart: plotter chart where to place the chart
        :type plotter_chart: GraphicsLayoutWidget
        :param legend: impedance legend where to read the color corresponding to the value
        :type legend: ImpedanceLegend
        :param head_enabled: is head to be shown on the background, defaults to True
        :type head_enabled: bool, optional
        """
        self.head_enabled = head_enabled
        self.legend = legend
        super().__init__(plotter_chart)
        self._plotter_chart.window.disableAutoRange()
        self._plotter_chart.setEnabled(False)
        self.__electrodes = []

    def initUI(self):
        """InitUI of Impedance chart"""
        # Set view settings
        self._plotter_chart.setBackground(None)
        self._plotter_chart.showMaximized()
        
        # Add plot window for the channels
        self._plotter_chart.window = self._plotter_chart.addPlot()
        self._plotter_chart.window.getViewBox().invertY(False)
        self._plotter_chart.window.setAspectLocked(lock=True, ratio = 1)
        self._plotter_chart.window.setXRange(-0.8, 0.8, padding = 0)
        self._plotter_chart.window.setYRange(-0.8, 0.8, padding = 0)       
        self._plotter_chart.window.hideAxis('left')
        self._plotter_chart.window.hideAxis('bottom')

        if self.head_enabled:
            #Plot a circle
            theta=np.arange(0, 2.02*math.pi, math.pi/50)
            x_circle = 0.5*np.cos(theta)
            y_circle = 0.5*np.sin(theta)
            head = pg.PlotCurveItem()
            head.setData(x_circle, y_circle, pen=pg.mkPen((70, 69, 69), width=5))
            self._plotter_chart.window.addItem(head) 
            
            #Plot a nose
            y_nose = np.array([x_circle[2], 0.55, x_circle[-3]])
            x_nose = np.array([y_circle[2], 0, y_circle[-3]])
            nose = pg.PlotCurveItem()
            nose.setData(x_nose, y_nose, pen=pg.mkPen((70, 69, 69), width=5))
            self._plotter_chart.window.addItem(nose)
            
            #Plot ears
            x_ears = np.array([0.49,  0.51,  0.52,  0.53, 0.54, 0.54, 0.55, 0.53, 0.51, 0.485])
            y_ears = np.array([0.10, 0.1175, 0.1185, 0.1145, 0.0955, -0.0055, -0.0930, -0.1315, -0.1385, -0.12])
            ear = pg.PlotCurveItem()
            ear.setData(x_ears, y_ears, pen=pg.mkPen((70, 69, 69), width=5))
            self._plotter_chart.window.addItem(ear)
            ear = pg.PlotCurveItem()
            ear.setData(-x_ears, y_ears, pen=pg.mkPen((70, 69, 69), width=5))
            self._plotter_chart.window.addItem(ear)

    def place_electrodes(self, channels, coordinates):
        """Place electrodes in position

        :param channels: list of channels
        :type channels: list
        :param coordinates: coordinates of the channel
        :type coordinates: dict
        """
        self._spots = []
        counter = 0
        for i in range(len(self._plotter_chart.window.items)):
            if isinstance(self._plotter_chart.window.items[counter], pg.TextItem) \
                or isinstance(self._plotter_chart.window.items[counter], pg.ScatterPlotItem):
                self._plotter_chart.window.removeItem(self._plotter_chart.window.items[counter])
            else:
                counter = counter + 1
        self.__electrodes = []
        for channel in channels:
            idx = str(channel.get_channel_index())
            if isinstance(coordinates["1"], tuple):
                cartesian = True
            else:
                cartesian = False
            if idx in coordinates:
                self.__electrodes.append(Electrode(
                    channel = channel, 
                    coordinates = coordinates[idx], 
                    cartesian = cartesian))
        self.__init_electrodes()

    def update_chart(self, values):
        """Update chart

        :param values: impedance values
        :type values: list
        """
        max_electrode = len(values)
        for n_electrode in range(len(self.__electrodes)):
            electrode = self.__electrodes[n_electrode]
            electrode_index = electrode.channel.get_channel_index()
            if  electrode_index < max_electrode:
                self.spots[n_electrode]['brush'] = QtGui.QBrush(self.legend.lookup_table(values[electrode_index]))
        self.c.setData(self.spots)
        
    def __init_electrodes(self):
        # Initialise the standard format for the different indicators
        self.spots = [{'pos': (0,0), 'size': 20, 'pen': 'k', 'brush': QtGui.QBrush(QtGui.QColor(0, 0, 0))} \
                        for i in range(len(self.__electrodes))]

        # Set the position for each indicator
        self.label_channel_names = []
        for i in range(len(self.__electrodes)):
            x=self.__electrodes[i].x
            y=self.__electrodes[i].y
            self.spots[i]['pos'] = (x,y)
                
            # Place the name of each channel below the respective indicator
            text = f'{self.__electrodes[i].channel.get_channel_name(): ^10}'
            t_item = pg.TextItem(text, (128, 128, 128, 204), anchor=(0, 0))
            t_item.setPos(self.spots[i]['pos'][0] -.03, self.spots[i]['pos'][1] - .02)
            self.label_channel_names.append(t_item)
            self._plotter_chart.window.addItem(t_item)

        # Add all indicators to the plot
        self.c = pg.ScatterPlotItem(self.spots)
        self._plotter_chart.window.addItem(self.c)