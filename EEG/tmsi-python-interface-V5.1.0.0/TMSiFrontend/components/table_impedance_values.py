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
 * @file table_impedance_values.py 
 * @brief 
 * Component to collect and show information about impedance values.
 */


'''
import math

from PySide2 import QtWidgets, QtCore

MAX_COLUMN_VALS = 32

class TableImpedanceValues:
    """TableImpedanceValues object"""
    def __init__(self,
        layout, 
        widget):
        """Initialize the table impedance values

        :param layout: layout to add the table to
        :type layout: QLayout
        :param widget: widget to add the table to
        :type widget: QtWidgets
        """
        self._parent_layout = layout
        self._parent_widget = widget
        self._table_impedance_values = QtWidgets.QTableWidget(self._parent_widget)
        self._table_impedance_values.setObjectName(u"table_impedance_values")
        self._table_impedance_values.setGridStyle(QtCore.Qt.NoPen)
        self._table_impedance_values.setCornerButtonEnabled(False)
        self._table_impedance_values.verticalHeader().setVisible(False)
        self._parent_layout.addWidget(self._table_impedance_values)
        self._chb_channels = []
        self.max_col_vals = MAX_COLUMN_VALS

    def get_channels_status(self):
        """Get the channels status (enabled/disabled)

        :return: a dictionary with info about the channels in the table
        :rtype: dict
        """
        response = {}
        for i in range(len(self._chb_channels)):
            response[i] = {
                "name": self._chb_channels[i].text(), 
                "enabled": self._chb_channels[i].isChecked()}
        return response

    def reset_table(self):
        """Reset the table"""
        self._table_impedance_values.clearContents()  # Clear the cell contents
        self._table_impedance_values.setRowCount(0)  # Remove all rows
        self._table_impedance_values.setColumnCount(0)  # Remove all columns

    def set_channels(self, channels):
        """Set channels on the table"""
        self.reset_table()
        self._chb_channels = []
        headers = ["Name", "Impedance"]
        if len(channels) < 60:
            self.max_col_vals = 17
        else:
            self.max_col_vals = 22
        n_columns = math.ceil(len(channels)/self.max_col_vals)
        headers = headers * n_columns
        self.set_headers(headers = headers)
        self._table_impedance_values.setRowCount(self.max_col_vals)
        n_row = 0
        for channel in channels:
            alt_name = QtWidgets.QCheckBox(text = channel.get_channel_name())
            alt_name.setChecked(True)
            real = QtWidgets.QTableWidgetItem("k\u03A9")
            real.setFlags(QtCore.Qt.ItemIsEnabled)
            self._table_impedance_values.setCellWidget(n_row % self.max_col_vals, n_row // self.max_col_vals * 2, alt_name)
            self._table_impedance_values.cellWidget(n_row % self.max_col_vals, n_row // self.max_col_vals * 2).setStyleSheet("margin-left: 20px;") 
            self._table_impedance_values.setItem(n_row % self.max_col_vals, n_row // self.max_col_vals * 2 + 1, real)
            n_row += 1
            self._chb_channels.append(alt_name)

    def set_headers(self, headers):
        """Set headers of the table"""
        self._table_impedance_values.setColumnCount(len(headers))
        self._table_impedance_values.setHorizontalHeaderLabels(headers)
        self._table_impedance_values.horizontalHeader().setStretchLastSection(True) 
        self._table_impedance_values.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def set_values(self, values):
        """Set values on the table"""
        n_row = 0
        for value in values:
            real = QtWidgets.QTableWidgetItem("{} k\u03A9".format(value))
            real.setFlags(QtCore.Qt.ItemIsEnabled)
            self._table_impedance_values.setItem(n_row % self.max_col_vals, n_row // self.max_col_vals * 2 + 1, real)
            n_row += 1
