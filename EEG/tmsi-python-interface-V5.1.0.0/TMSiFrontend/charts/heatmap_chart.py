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
 * @file heatmap_chart.py 
 * @brief 
 * Heatmap Chart object
 */


'''

import math
import numpy as np
import pyqtgraph as pg
from scipy import interpolate

from ..chart import Chart

class HeatmapChart(Chart):
    """Heatmap Chart object"""
    def __init__(self, plotter_chart, resolution = 100.0, title = None):
        """Initialize heatmap chart

        :param plotter_chart: plotter chart where to place the chart
        :type plotter_chart: GraphicsLayoutWidget
        :param resolution: points of the heatmap, defaults to 100.0
        :type resolution: float, optional
        :param title: title of the heatmap, defaults to None
        :type title: str, optional
        """
        self._is_headcap = False
        self._resolution = resolution
        self._title = title
        super().__init__(plotter_chart)

    def initUI(self):
        """Initialize UI"""
        self._plotter_chart.setBackground(None)
        self._plotter_chart.setEnabled(False)
        self._plotter_chart.window = self._plotter_chart.addPlot(title=self._title)
        self._plotter_chart.window.setAspectLocked(lock=True, ratio = 1)
        dummy_vals = np.zeros((1000,1000))
        self._img = pg.ImageItem(image = dummy_vals)
        self._plotter_chart.window.addItem(self._img)
        self._plotter_chart.window.hideAxis('left')
        self._plotter_chart.window.hideAxis('bottom')
        self._upper_lim = 100
        self._lower_lim = 0
        self._cm = pg.colormap.get('CET-R4')
        self._bar = pg.ColorBarItem(values = (self._lower_lim, self._upper_lim), colorMap=self._cm, interactive = False, label = 'RMS (\u03BCVolt)', )
        self._bar.setImageItem(self._img, insert_in = self._plotter_chart.window)
        
    def place_electrodes(self, channels, coordinates):
        """Place electrodes in position

        :param channels: list of channels
        :type channels: list
        :param coordinates: coordinates of the channel
        :type coordinates: dict
        """
        if isinstance(coordinates["1"], tuple):
            cartesian = True
        else:
            cartesian = False
        if not cartesian:
            for key in coordinates.keys():
                coordinates[key] = self._from_polar_to_cartesian(
                    radius = coordinates[key]["radius"],
                    angle = coordinates[key]["angle"])
        electrode_positions = []
        electrode_labels = []
        for channel in channels:
            idx = str(channel.get_channel_index())
            if idx in coordinates:
                new_pos = (coordinates[idx][0] + 0.5, coordinates[idx][1] + 0.5)
                electrode_positions.append(new_pos)
                electrode_labels.append(channel.get_channel_name())
        self.__max_x = math.ceil(max([x[0] for x in electrode_positions]))
        self.__max_y = math.ceil(max([x[1] for x in electrode_positions]))
        self._step = max(self.__max_x, self.__max_y) / self._resolution
        self._x_interpolate, self._y_interpolate = np.mgrid[0:self.__max_x:self._step,0:self.__max_y:self._step]
        self._electrode_positions = electrode_positions
        self._electrode_labels = electrode_labels
        self.initialize_electrode_labels()
        self.set_ranges([0,1],[0,1])
        if self._is_headcap:
            self.set_ranges([-self.__max_x * 0.1, self.__max_x * 1.1], [-self.__max_y * 0.1, self.__max_y * 1.1])
            corners = [[i,j] for i in range(0,self.__max_x+1,self.__max_x) for j in range(0,self.__max_y+1,self.__max_y)]
            self._electrode_positions.extend(corners)

    def initialize_electrode_labels(self):
        """Initialize electrode labels on the chart"""
        if not self._electrode_labels:
            return
        for i,x in enumerate(self._electrode_positions):
            text=self._electrode_labels[i]
            t_item = pg.TextItem(text, (128, 128, 128), anchor=(0, 0))
            t_item.setPos(x[0] / self._step, x[1] / self._step)
            self._plotter_chart.window.addItem(t_item) 

    def draw_headcap(self):
        """Draw head on the chart"""
        self._is_headcap = True
        self._x_offset = self._resolution / 2
        self._y_offset = self._resolution / 2
        self._radius = self._resolution / 2
        
        #Plot a circle
        theta=np.arange(0, 2.02*math.pi, math.pi/50)
        x_circle = self._x_offset + self._radius*np.cos(theta)
        y_circle = self._y_offset + self._radius*np.sin(theta)
        head = pg.PlotCurveItem()
        head.setData(x_circle, y_circle, pen=pg.mkPen((70, 69, 69), width=10))
        self._plotter_chart.window.addItem(head) 
        
        #Plot a nose
        y_nose = np.array([x_circle[2], x_circle[0] + self._resolution * 0.05, x_circle[-3]])
        x_nose = np.array([y_circle[2], y_circle[0], y_circle[-3]])
        nose = pg.PlotCurveItem()
        nose.setData(x_nose, y_nose, pen=pg.mkPen((70, 69, 69), width=5))
        self._plotter_chart.window.addItem(nose)
        
        #Plot ears
        x_ears = np.array([self._resolution * 0.99,  self._resolution * 1.02,  self._resolution * 1.03,  self._resolution * 1.04, self._resolution * 1.05, self._resolution * 1.05, self._resolution * 1.06, self._resolution * 1.04, self._resolution * 1.02, self._resolution * 0.985])
        y_ears = np.array([self._resolution/2 + self._resolution * 0.10, self._resolution/2 + self._resolution * 0.1175, self._resolution/2 + self._resolution * 0.1185, self._resolution/2 + self._resolution * 0.1145, self._resolution/2 + self._resolution * 0.0955, self._resolution/2 - self._resolution * 0.055, self._resolution/2 - self._resolution * 0.0930, self._resolution/2 - self._resolution * 0.1315, self._resolution/2 - self._resolution * 0.1385, self._resolution/2 - self._resolution * 0.12])
        ear = pg.PlotCurveItem()
        ear.setData(x_ears, y_ears, pen=pg.mkPen((70, 69, 69), width=5))
        self._plotter_chart.window.addItem(ear)
        ear = pg.PlotCurveItem()
        ear.setData(-x_ears+self._resolution, y_ears, pen=pg.mkPen((70, 69, 69), width=5))
        self._plotter_chart.window.addItem(ear)
        
    def set_ranges(self, x_ranges, y_ranges):
        """Set ranges for the chart

        :param x_ranges: ranges x axis
        :type x_ranges: list with min and max
        :param y_ranges: ranges y axis
        :type y_ranges: list with min and max
        """
        self._plotter_chart.window.setXRange(x_ranges[0] / self._step, x_ranges[1] / self._step, padding = 0)
        self._plotter_chart.window.setYRange(y_ranges[0] / self._step, y_ranges[1] / self._step, padding = 0)
        
    def update_cm(self, style):
        """Update the color map with the desired style

        :param style: style of the color map
        :type style: str
        """
        self._cm = pg.colormap.get(style)
        self.update_bar()
    
    def update_bar(self, upper_limit = None, lower_limit = None):
        """Update the bar with new limits

        :param upper_limit: higher limit of the bar, defaults to None
        :type upper_limit: float, optional
        :param lower_limit: lower limit of the bar, defaults to None
        :type lower_limit: float, optional
        """
        if upper_limit is not None:
            self._upper_lim = upper_limit
        if lower_limit is not None:
            self._lower_lim = lower_limit
        self._plotter_chart.window.layout.removeItem(self._bar)
        self._bar.deleteLater()
        self._bar = pg.ColorBarItem(values = (self._lower_lim, self._upper_lim), colorMap=self._cm, interactive = False, label = None, )
        self._bar.setImageItem(self._img, insert_in = self._plotter_chart.window)

    def update_chart(self, data_to_plot):
        """Update chart with new values

        :param data_to_plot: values to represent
        :type data_to_plot: list
        """
        heatmap = self._from_data_to_heatmap(data_to_plot)
        if self._is_headcap:
            heatmap = self._filter_outside_headcap(heatmap)
        self._draw_heatmap(heatmap)
 
    def _draw_heatmap(self, heatmap):
        self._img.setImage(heatmap, autoRange=False, autoLevels=False)


    def _filter_outside_headcap(self, heatmap):
        heatmap = [[np.nan if (x - self._x_offset + 0.5 )**2+(y - self._y_offset + 0.5)**2 >= (self._radius**2) else heatmap[y][x] for x in range(len(heatmap))] for y in range(len(heatmap[0]))]
        heatmap = np.array(heatmap)
        return heatmap

 
    def _from_data_to_heatmap(self, data_to_plot):
        if self._is_headcap:
            data_to_plot = np.pad(data_to_plot, 4)[4:]
        return interpolate.griddata(self._electrode_positions, data_to_plot, (self._x_interpolate, self._y_interpolate), method='cubic')
    
    def _from_polar_to_cartesian(self, radius, angle):
        col = radius * math.cos(angle/180*math.pi)
        row = radius * math.sin(angle/180*math.pi)
        return (row, col)