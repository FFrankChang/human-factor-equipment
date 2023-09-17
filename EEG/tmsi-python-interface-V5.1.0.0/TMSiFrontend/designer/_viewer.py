# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viewer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Viewer(object):
    def setupUi(self, Viewer):
        if not Viewer.objectName():
            Viewer.setObjectName(u"Viewer")
        Viewer.resize(757, 490)
        self.verticalLayout_2 = QVBoxLayout(Viewer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_plotter = QFrame(Viewer)
        self.frame_plotter.setObjectName(u"frame_plotter")
        self.frame_plotter.setFrameShape(QFrame.StyledPanel)
        self.frame_plotter.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_plotter)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_plotter = QVBoxLayout()
        self.layout_frame_plotter.setSpacing(0)
        self.layout_frame_plotter.setObjectName(u"layout_frame_plotter")
        self.layout_frame_plotter.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addLayout(self.layout_frame_plotter)


        self.verticalLayout_2.addWidget(self.frame_plotter)

        self.time_scrollbar = QScrollBar(Viewer)
        self.time_scrollbar.setObjectName(u"time_scrollbar")
        self.time_scrollbar.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.time_scrollbar)


        self.retranslateUi(Viewer)

        QMetaObject.connectSlotsByName(Viewer)
    # setupUi

    def retranslateUi(self, Viewer):
        Viewer.setWindowTitle(QCoreApplication.translate("Viewer", u"Form", None))
    # retranslateUi

