# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_discover.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogDiscover(object):
    def setupUi(self, DialogDiscover):
        if not DialogDiscover.objectName():
            DialogDiscover.setObjectName(u"DialogDiscover")
        DialogDiscover.resize(549, 305)
        self.centralwidget = QWidget(DialogDiscover)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gb_device = QGroupBox(self.centralwidget)
        self.gb_device.setObjectName(u"gb_device")
        self.device_layout = QHBoxLayout(self.gb_device)
        self.device_layout.setObjectName(u"device_layout")

        self.gridLayout.addWidget(self.gb_device, 1, 1, 1, 2)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_5, 3, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 1, 1, 2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_6, 1, 3, 1, 1)

        self.btn_discover = QPushButton(self.centralwidget)
        self.btn_discover.setObjectName(u"btn_discover")
        self.btn_discover.setEnabled(False)
        self.btn_discover.setMaximumSize(QSize(200, 16777215))
        self.btn_discover.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout.addWidget(self.btn_discover, 5, 2, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 4, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 5, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 1, 0, 1, 1)

        self.gb_dr_interface = QGroupBox(self.centralwidget)
        self.gb_dr_interface.setObjectName(u"gb_dr_interface")
        self.dr_layout = QHBoxLayout(self.gb_dr_interface)
        self.dr_layout.setObjectName(u"dr_layout")

        self.gridLayout.addWidget(self.gb_dr_interface, 3, 1, 1, 2)

        self.gb_ds_interface = QGroupBox(self.centralwidget)
        self.gb_ds_interface.setObjectName(u"gb_ds_interface")
        self.ds_layout = QHBoxLayout(self.gb_ds_interface)
        self.ds_layout.setObjectName(u"ds_layout")

        self.gridLayout.addWidget(self.gb_ds_interface, 4, 1, 1, 2)

        DialogDiscover.setCentralWidget(self.centralwidget)

        self.retranslateUi(DialogDiscover)

        QMetaObject.connectSlotsByName(DialogDiscover)
    # setupUi

    def retranslateUi(self, DialogDiscover):
        DialogDiscover.setWindowTitle(QCoreApplication.translate("DialogDiscover", u"Dialog Discover", None))
        self.gb_device.setTitle(QCoreApplication.translate("DialogDiscover", u"Device", None))
        self.btn_discover.setText(QCoreApplication.translate("DialogDiscover", u"Discover", None))
        self.gb_dr_interface.setTitle(QCoreApplication.translate("DialogDiscover", u"DR Interface", None))
        self.gb_ds_interface.setTitle(QCoreApplication.translate("DialogDiscover", u"DS Interface", None))
    # retranslateUi

