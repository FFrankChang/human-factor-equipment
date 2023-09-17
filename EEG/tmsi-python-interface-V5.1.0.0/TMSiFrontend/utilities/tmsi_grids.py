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
 * @file tmsi_grids.py 
 * @brief 
 * Singleton class which handles the available TMSi grids.
 */


'''
from .singleton import Singleton

class TMSiGrids(metaclass = Singleton):
    """Singleton class which handles the available TMSi grids"""
    def __init__(self):
        """Initializes the object."""
        self.grids = {}
        self.reorder = {}
        self.grids["3-8"] = {"0": (0.125, -0.7), "25": (-0.125, -0.7)}
        self.grids["4-8"] = {"0": (0.125, -0.7), "33": (-0.125, -0.7)}
        self.grids["8-8"] = {"0": (0.125, -0.7), "65": (-0.125, -0.7)}
        self.grids["6-11"] = {"0": (0.125, -0.7), "65": (-0.125, -0.7)}
        self.grids["6-11-1"] = {"0": (0.125, -0.7), "33": (-0.125, -0.7)}
        self.grids["6-11-2"] = {"0": (0.125, -0.7), "33": (-0.125, -0.7)}
        for i in range(24):
            self.grids["3-8"]["{}".format(i + 1)] = (float(i % 8) / 8.0 - 0.5 , -float(i // 8) / 8.0 + 0.5)
        for i in range(32):
            self.grids["4-8"]["{}".format(i + 1)] = (float(i % 8) / 8.0 - 0.5 , -float(i // 8) / 8.0 + 0.5)
        for i in range(64):
            self.grids["8-8"]["{}".format(i + 1)] = (float(i % 8) / 8.0 - 0.5, -float(i // 8) / 8.0 + 0.5)
            if i < 10:
                j = i
            else:
                j = i + 1
            if i < 32:
                self.grids["6-11-1"]["{}".format(i + 1)] = (float(j % 11) / 11.0 - 0.5 , -float(j // 11) / 11.0 + 0.25)
            else:
                self.grids["6-11-2"]["{}".format((j - 33) + 1)] = (float((j - 33) % 11) / 11.0 - 0.5 , -float((j - 33) // 11) / 11.0 + 0.25)
            self.grids["6-11"]["{}".format(i + 1)] = (float(j % 11) / 11.0 - 0.5 , -float(j // 11) / 11.0 + 0.25)
        