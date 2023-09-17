'''
(c) 2022 Twente Medical Systems International B.V., Oldenzaal The Netherlands

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
 * @file ${example_poly5_to_edf.py} 
 * @brief This example shows the functionality to convert a single poly5-file  
.* to edf-format. The data is bandpass filtered to remove offset and drift  
 * while maintaining as much as much relevant information as possible in the 
 * conversion from 32-bit to 16-bit file format.
 */


'''
import sys
from os.path import join, dirname, realpath

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_formats import Poly5_to_EDF_Converter

# The Poly5Converter opens a recorded Poly5 file. Both a specific file-path can be provided,
# as well as no path, which prompts a dialog window. Pre-processing steps (band-pass filter),
# are to be configured (0.1 - 100 Hz is selected in this example)
Poly5Converter = Poly5_to_EDF_Converter(f_c = [0.1, 100])

