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
 * @file impedance_legend.py 
 * @brief 
 * Impedance legend.
 */


'''
import pyqtgraph as pg
from PySide2 import  QtGui

class ImpedanceLegend:
    """ImpedanceLegend object"""
    def __init__(self, legend_chart, device_type):
        """Initialize the impedance legend

        :param legend_chart: place where to place the legend 
        :type legend_chart: GraphicsLayoutWidget
        """
        self._legend_chart = legend_chart
        self.InitUI()
        self.lookup_table = None
        self.generate_legend(device = device_type)

    def InitUI(self):
        """Initialization of the UI of the legend"""
        # Add viewbox for the legend
        self.vb_legend = self._legend_chart.addViewBox()
        self._legend_chart.setBackground(None)
        self._legend = pg.LegendItem()
        self._legend.setParentItem(self.vb_legend)
            
    def generate_legend(self, device):
        """ Method that generates the legend of the chart

        :param device: can be saga or apex
        :type device: str
        """
        if device.lower() == "saga":
            labels = [
                '0 - 5 k\u03A9',
                '5 - 30 k\u03A9',
                '30 - 50 k\u03A9',
                '50 - 100 k\u03A9',
                '100 - 200 k\u03A9',
                '200 - 400 k\u03A9',
                '400 - 500 k\u03A9',
                '≥ 500 k\u03A9',
                'Disabled',
                'Odd/even error',
                'PGND disconnected'
            ]
            values = [0, 5, 30, 50, 100, 200, 400, 500, 5000, 5100, 5200]
            self.lookup_table = ImpedanceLegend.lookup_table_saga
        elif device.lower() == "apex":
            labels = [
                '0 - 5 k\u03A9',
                '5 - 30 k\u03A9',
                '30 - 50 k\u03A9',
                '50 - 100 k\u03A9',
                '100 - 200 k\u03A9',
                '200 - 400 k\u03A9',
                '400 - 1000 k\u03A9',
                '≥ 1000 k\u03A9',
                'Disabled',
                'Odd/even error',
                'PGND disconnected'
            ]
            values = [0, 5, 30, 50, 100, 200, 400, 1000]
            self.lookup_table = ImpedanceLegend.lookup_table_apex
        else:
            return
        
        legend_spots = [{'pos': (0,0), 'size': 10, 'pen': 'k', 'brush': QtGui.QBrush() , 'name': ''} for i in range(len(values))]
        for i in range(len(values)):
            legend_spots[i]['name'] = labels[i]
            legend_spots[i]['brush'] = QtGui.QBrush(self.lookup_table(values[i]))
        
        # Generate the legend by using dummy plots 
        self.legend_entries = []
        for i in range(len(legend_spots)):
            
            lg_plt = pg.ScatterPlotItem(pos= [(0,0),(0,0)], size = 20,
                                        pen = legend_spots[i]['pen'], brush = legend_spots[i]['brush'],
                                        name = legend_spots[i]['name'])
            self._legend.addItem(lg_plt, legend_spots[i]['name'])
            lg_plt.clear()

    def lookup_table_apex(value):
        """Look up table to convert impedances to color coding"""
        if value < 5:
            color_code = QtGui.QColor(205, 251, 205)
        elif value >= 5 and value < 30:
            color_code = QtGui.QColor(0, 252, 128)
        elif value >= 30 and value < 50:
            color_code = QtGui.QColor(34, 139, 34)
        elif value >= 50 and value < 100:
            color_code = QtGui.QColor(204, 181, 0)
        elif value >= 100 and value < 200:
            color_code = QtGui.QColor(255, 142, 39)
        elif value >= 200 and value < 400:
            color_code = QtGui.QColor(255, 0, 0)
        elif value >= 400 and value < 1000:
            color_code = QtGui.QColor(150, 0, 0)
        elif value == 5000:
            color_code = QtGui.QColor(175, 175, 175)
        elif value == 5100:
            color_code = QtGui.QColor(204, 0, 102)
        elif value == 5200:
            color_code = QtGui.QColor(0, 0, 179)
        else:
            color_code = QtGui.QColor(76, 76, 76)
        return color_code

    def lookup_table_saga(value):
        """Look up table to convert impedances to color coding"""
        if value < 5:
            color_code = QtGui.QColor(205, 251, 205)
        elif value >= 5 and value < 30:
            color_code = QtGui.QColor(0, 252, 128)
        elif value >= 30 and value < 50:
            color_code = QtGui.QColor(34, 139, 34)
        elif value >= 50 and value < 100:
            color_code = QtGui.QColor(204, 181, 0)
        elif value >= 100 and value < 200:
            color_code = QtGui.QColor(255, 142, 39)
        elif value >= 200 and value < 400:
            color_code = QtGui.QColor(255, 0, 0)
        elif value >= 400 and value < 500:
            color_code = QtGui.QColor(150, 0, 0)
        elif value == 5000:
            color_code = QtGui.QColor(175, 175, 175)
        elif value == 5100:
            color_code = QtGui.QColor(204, 0, 102)
        elif value == 5200:
            color_code = QtGui.QColor(0, 0, 179)
        else:
            color_code = QtGui.QColor(76, 76, 76)
        return color_code

    def setVisible(self, visible):
        """Set the visibility of the legend

        :param visible: True if to set visible, False otherwise
        :type visible: bool
        """
        self._legend_chart.setVisible(visible)

    