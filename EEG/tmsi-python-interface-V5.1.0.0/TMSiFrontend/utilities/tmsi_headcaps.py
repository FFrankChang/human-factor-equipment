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
 * @file tmsi_headcaps.py 
 * @brief 
 * Singleton class which handles the available TMSi headcaps.
 */


'''
from .singleton import Singleton

class TMSiHeadcaps(metaclass = Singleton):
    """Singleton class which handles the available TMSi headcaps"""
    def __init__(self):
        """Initializes the object."""
        self.headcaps = {}
        self.headcaps["mocked"]={
            "0" : {"radius": 0.7, "angle": 180}
        }
        self.headcaps["eeg32"]={
            "0": {"radius": 0.7, "angle": -175},
            "1": {"radius": 0.479000000000000, "angle":-18},
            "2": {"radius": 0.471000000000000, "angle": 0},
            "3": {"radius": 0.479000000000000, "angle": 18},
            "4": {"radius": 0.491000000000000, "angle":-54},
            "5": {"radius": 0.318000000000000, "angle":-39},
            "6": {"radius": 0.234000000000000, "angle": 0},
            "7": {"radius": 0.318000000000000, "angle": 39},
            "8": {"radius": 0.491000000000000, "angle": 54},
            "9": {"radius": 0.382000000000000, "angle":-69},
            "10": {"radius": 0.167000000000000, "angle":-45},
            "11": {"radius": 0.167000000000000, "angle": 45},
            "12": {"radius": 0.382000000000000, "angle": 69},
            "13": {"radius": 0.500000000000000, "angle":-100},
            "14": {"radius": 0.500000000000000, "angle":-90},
            "15": {"radius": 0.247000000000000, "angle":-90},
            "16": {"radius": 0, "angle": 0},
            "17": {"radius": 0.247000000000000, "angle": 90},
            "18": {"radius": 0.500000000000000, "angle": 90},
            "19": {"radius": 0.500000000000000, "angle": 100},
            "20": {"radius": 0.382000000000000, "angle":-111},
            "21": {"radius": 0.168000000000000, "angle":-136},
            "22": {"radius": 0.168000000000000, "angle": 136},
            "23": {"radius": 0.382000000000000, "angle": 111},
            "24": {"radius": 0.491000000000000, "angle":-126},
            "25": {"radius": 0.321000000000000, "angle":-141},
            "26": {"radius": 0.239000000000000, "angle": 180},
            "27": {"radius": 0.321000000000000, "angle": 141},
            "28": {"radius": 0.491000000000000, "angle": 126},
            "29": {"radius": 0.350000000000000, "angle": 180},
            "30": {"radius": 0.482000000000000, "angle":-169},
            "31": {"radius": 0.472000000000000, "angle": 180},
            "32": {"radius": 0.482000000000000, "angle": 169},
            "33": {"radius": 0.7, "angle": 175}
        }
        self.headcaps["eeg24"]={
            "0": {"radius": 0.7, "angle": -175},
            "1": {"radius": 0.479000000000000, "angle":-18},
            "2": {"radius": 0.471000000000000, "angle": 0},
            "3": {"radius": 0.479000000000000, "angle": 18},
            "4": {"radius": 0.491000000000000, "angle":-54},
            "5": {"radius": 0.318000000000000, "angle":-39},
            "6": {"radius": 0.234000000000000, "angle": 0},
            "7": {"radius": 0.318000000000000, "angle": 39},
            "8": {"radius": 0.491000000000000, "angle": 54},
            "13": {"radius": 0.500000000000000, "angle":-100},
            "14": {"radius": 0.500000000000000, "angle":-90},
            "15": {"radius": 0.247000000000000, "angle":-90},
            "16": {"radius": 0, "angle": 0},
            "17": {"radius": 0.247000000000000, "angle": 90},
            "18": {"radius": 0.500000000000000, "angle": 90},
            "19": {"radius": 0.500000000000000, "angle": 100},
            "24": {"radius": 0.491000000000000, "angle":-126},
            "25": {"radius": 0.321000000000000, "angle":-141},
            "26": {"radius": 0.239000000000000, "angle": 180},
            "27": {"radius": 0.321000000000000, "angle": 141},
            "28": {"radius": 0.491000000000000, "angle": 126},
            "29": {"radius": 0.350000000000000, "angle": 180},
            "30": {"radius": 0.482000000000000, "angle":-169},
            "31": {"radius": 0.472000000000000, "angle": 180},
            "32": {"radius": 0.482000000000000, "angle": 169},
            "33": {"radius": 0.7, "angle": 175}
        }
        self.headcaps["apex24"]={
            "0": {"radius": 0.7, "angle": -175},
            "1": {"radius": 0.479000000000000, "angle":-18},
            "2": {"radius": 0.471000000000000, "angle": 0},
            "3": {"radius": 0.479000000000000, "angle": 18},
            "4": {"radius": 0.491000000000000, "angle":-54},
            "5": {"radius": 0.318000000000000, "angle":-39},
            "6": {"radius": 0.234000000000000, "angle": 0},
            "7": {"radius": 0.318000000000000, "angle": 39},
            "8": {"radius": 0.491000000000000, "angle": 54},
            "9": {"radius": 0.500000000000000, "angle":-100},
            "10": {"radius": 0.500000000000000, "angle":-90},
            "11": {"radius": 0.247000000000000, "angle":-90},
            "12": {"radius": 0, "angle": 0},
            "13": {"radius": 0.247000000000000, "angle": 90},
            "14": {"radius": 0.500000000000000, "angle": 90},
            "15": {"radius": 0.500000000000000, "angle": 100},
            "16": {"radius": 0.491000000000000, "angle":-126},
            "17": {"radius": 0.321000000000000, "angle":-141},
            "18": {"radius": 0.239000000000000, "angle": 180},
            "19": {"radius": 0.321000000000000, "angle": 141},
            "20": {"radius": 0.491000000000000, "angle": 126},
            "21": {"radius": 0.350000000000000, "angle": 180},
            "22": {"radius": 0.482000000000000, "angle":-169},
            "23": {"radius": 0.472000000000000, "angle": 180},
            "24": {"radius": 0.482000000000000, "angle": 169},
            "25": {"radius": 0.7, "angle": 175}
        }
        self.headcaps["eeg64"] = {
            "0": {"radius": 0.7, "angle": -175},
            "1": {"radius": 0.479000000000000, "angle": -18},
            "2": {"radius": 0.471000000000000, "angle": 0},
            "3": {"radius": 0.479000000000000, "angle": 18},
            "4": {"radius": 0.491000000000000, "angle": -54},
            "5": {"radius": 0.318000000000000, "angle": -39},
            "6": {"radius": 0.234000000000000, "angle": 0},
            "7": {"radius": 0.318000000000000, "angle": 39},
            "8": {"radius": 0.491000000000000, "angle": 54},
            "9": {"radius": 0.382000000000000, "angle": -69},
            "10": {"radius": 0.167000000000000, "angle": -45},
            "11": {"radius": 0.167000000000000, "angle": 45},
            "12": {"radius": 0.382000000000000, "angle": 69},
            "13": {"radius": 0.500000000000000, "angle": -100},
            "14": {"radius": 0.500000000000000, "angle": -90},
            "15": {"radius": 0.247000000000000, "angle": -90},
            "16": {"radius": 0, "angle": 0},
            "17": {"radius": 0.247000000000000, "angle": 90},
            "18": {"radius": 0.500000000000000, "angle": 90},
            "19": {"radius": 0.500000000000000, "angle": 100},
            "20": {"radius": 0.382000000000000, "angle": -111},
            "21": {"radius": 0.168000000000000, "angle": -136},
            "22": {"radius": 0.168000000000000, "angle": 136},
            "23": {"radius": 0.382000000000000, "angle": 111},
            "24": {"radius": 0.491000000000000, "angle": -126},
            "25": {"radius": 0.321000000000000, "angle": -141},
            "26": {"radius": 0.239000000000000, "angle": 180},
            "27": {"radius": 0.321000000000000, "angle": 141},
            "28": {"radius": 0.491000000000000, "angle": 126},
            "29": {"radius": 0.350000000000000, "angle": 180},
            "30": {"radius": 0.482000000000000, "angle": -169},
            "31": {"radius": 0.472000000000000, "angle": 180},
            "32": {"radius": 0.482000000000000, "angle": 169},
            "33": {"radius": 0.470000000000000, "angle": -36},
            "34": {"radius": 0.395000000000000, "angle": -23},
            "35": {"radius": 0.395000000000000, "angle": 23},
            "36": {"radius": 0.470000000000000, "angle": 36},
            "37": {"radius": 0.404000000000000, "angle": -50},
            "38": {"radius": 0.258000000000000, "angle": -23},
            "39": {"radius": 0.258000000000000, "angle": 23},
            "40": {"radius": 0.404000000000000, "angle": 50},
            "41": {"radius": 0.266000000000000, "angle": -62},
            "42": {"radius": 0.118000000000000, "angle": 0},
            "43": {"radius": 0.266000000000000, "angle": 62},
            "44": {"radius": 0.372000000000000, "angle": -90},
            "45": {"radius": 0.125000000000000, "angle": -90},
            "46": {"radius": 0.125000000000000, "angle": 90},
            "47": {"radius": 0.372000000000000, "angle": 90},
            "48": {"radius": 0.267000000000000, "angle": -118},
            "49": {"radius": 0.118000000000000, "angle": 180},
            "50": {"radius": 0.267000000000000, "angle": 118},
            "51": {"radius": 0.403000000000000, "angle": -131},
            "52": {"radius": 0.259000000000000, "angle": -157},
            "53": {"radius": 0.259000000000000, "angle": 157},
            "54": {"radius": 0.403000000000000, "angle": 131},
            "55": {"radius": 0.437000000000000, "angle": -150},
            "56": {"radius": 0.395000000000000, "angle": -158},
            "57": {"radius": 0.395000000000000, "angle": 158},
            "58": {"radius": 0.437000000000000, "angle": 150},
            "59": {"radius": 0.496000000000000, "angle": -72},
            "60": {"radius": 0.496000000000000, "angle": 72},
            "61": {"radius": 0.496000000000000, "angle": -109},
            "62": {"radius": 0.496000000000000, "angle": 109},
            "63": {"radius": 0.489000000000000, "angle": -145},
            "64": {"radius": 0.489000000000000, "angle": 145},
            "65": {"radius": 0.7, "angle": 175}
        }