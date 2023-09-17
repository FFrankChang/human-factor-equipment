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
 * @file ${gui.py}
 * @brief This file is used as general GUI for the different plotter helpers
    
'''

from PySide2.QtWidgets import *
from TMSiFrontend import TMSiStyle

class Gui:
    def __init__(self,plotter_helper):
        self.plotter_helper = plotter_helper
        self.window = QMainWindow()
        self.window.setWindowTitle("Signal Acquisition")
        self.main_plotter = plotter_helper.main_plotter
        self.window.setCentralWidget(self.main_plotter)
        self.window.resize(self.main_plotter.size())
        self.window.closeEvent = self.closeEvent
        self.window.setStyleSheet(TMSiStyle)
        self.window.showMaximized()
        self.plotter_helper.initialize()
        self.plotter_helper.start()

    def closeEvent(self, event):
        print("closing")
        self.plotter_helper.stop()
