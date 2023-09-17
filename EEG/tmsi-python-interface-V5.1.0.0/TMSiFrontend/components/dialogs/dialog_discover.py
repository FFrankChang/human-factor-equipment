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
 * @file dialog_discover.py 
 * @brief 
 * Dialog object to communicate with the user to get discover action.
 */


'''
from PySide2 import QtWidgets, QtCore

from ..designer._dialog_discover import Ui_DialogDiscover

class DialogDiscover(QtWidgets.QMainWindow, Ui_DialogDiscover):
    """DialogDiscover object"""
    def __init__(self, combinations_available, callback_discover):
        """Initialize Dialog Discover

        :param combinations_available: available discoveries
        :type combinations_available: dict
        :param callback_discover: callback function when discover
        :type callback_discover: function
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.combinations_available = combinations_available
        self.callback_discover = callback_discover
        self.list_devices = []
        self.list_drs = []
        self.list_dss = []
        self.gb_dr_interface.setVisible(False)
        self.gb_ds_interface.setVisible(False)
        self.btn_discover.clicked.connect(self.click_discover)
        for dev in self.combinations_available.keys():
            radio_btn = QtWidgets.QRadioButton(self.gb_device)
            radio_btn.setObjectName("dev_{}".format(dev))
            radio_btn.setText("{}".format(dev))
            radio_btn.toggled.connect(self.update_interfaces)
            self.device_layout.addWidget(radio_btn)
            self.list_devices.append(radio_btn)
        if len(self.list_devices) == 1:
            self.list_devices[0].setChecked(True)

    def click_discover(self):
        """Click discover action"""
        args = dict()
        for dev in self.list_devices:
            if dev.isChecked():
                args["device"] = dev.text()
                break
        for dev in self.list_drs:
            if dev.isChecked():
                args["dr"] = dev.text()
                break
        for dev in self.list_dss:
            if dev.isChecked():
                args["ds"] = dev.text()
                break
        self.close()
        self.callback_discover(args)

    def update_discover(self):
        """Update discover"""
        discover_enabled = False
        for dev in self.list_devices:
            if dev.isChecked():
                discover_enabled = True
                if len(self.list_drs) > 0:
                    discover_enabled = False
                    for dr in self.list_drs:
                        if dr.isChecked():
                            discover_enabled = True
                            break
                if len(self.list_dss) > 0:
                    discover_enabled = False
                    for ds in self.list_dss:
                        if ds.isChecked():
                            discover_enabled = True
                            break
                break
        self.btn_discover.setEnabled(discover_enabled)

    def update_drs(self):
        """Update Device Recorder interfaces"""
        for dev in self.list_devices:
            if dev.isChecked():
                device = self.combinations_available[dev.text()]
                if "dr_interface" not in device:
                    self.gb_dr_interface.setVisible(False)
                    return
                for dr in device["dr_interface"]:
                    self.gb_dr_interface.setVisible(True)
                    radio_btn = QtWidgets.QRadioButton(self.gb_dr_interface)
                    radio_btn.setObjectName("dr_{}".format(dr))
                    radio_btn.setText("{}".format(dr))
                    radio_btn.toggled.connect(self.update_discover)
                    self.dr_layout.addWidget(radio_btn)
                    self.list_drs.append(radio_btn)
                if len(self.list_drs) == 1:
                    self.list_drs[0].setChecked(True)
                break

    def update_dss(self):
        """Update dock station interfaces"""
        for dev in self.list_devices:
            if dev.isChecked():
                device = self.combinations_available[dev.text()]
                if "ds_interface" not in device:
                    self.gb_ds_interface.setVisible(False)
                    return
                for ds in device["ds_interface"]:
                    self.gb_ds_interface.setVisible(True)
                    radio_btn = QtWidgets.QRadioButton(self.gb_ds_interface)
                    radio_btn.setObjectName("ds_{}".format(ds))
                    radio_btn.setText("{}".format(ds))
                    radio_btn.toggled.connect(self.update_discover)
                    self.ds_layout.addWidget(radio_btn)
                    self.list_dss.append(radio_btn)
                if len(self.list_dss) == 1:
                    self.list_dss[0].setChecked(True)
                break
    
    def update_interfaces(self):
        """Update interfaces"""
        self.btn_discover.setEnabled(False)
        self._clean_drs()
        self._clean_dss()
        self.update_drs()
        self.update_dss()

    def _clean_drs(self):
        self.list_drs = []
        while True:
            wid = self.dr_layout.takeAt(0)
            if wid is None:
                break
            wid.widget().deleteLater()

    def _clean_dss(self):
        self.list_dss = []
        while True:
            wid = self.ds_layout.takeAt(0)
            if wid is None:
                break
            wid.widget().deleteLater()