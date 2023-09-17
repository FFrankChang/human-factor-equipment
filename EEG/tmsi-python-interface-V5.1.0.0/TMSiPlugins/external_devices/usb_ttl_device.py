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
 * @file ${usb_ttl_device.py} 
 * @brief This class provides code to write triggers with the USB TTL module
 *
 */


'''

import serial
import time
import serial.tools.list_ports

# ---- DEFINE TMSI DEVICE TO USE -------
# The USB TTL module is TMSi device specific. Please make sure to call the correct
# device in the USB_TTL_device() input


class USB_TTL_device():
    "Class that interfaces the Black Box Toolkit USB-TTL module to Python"
    def __init__(self, TMSiDevice, com_port = False):
        """
            Initialize the USB TTL device. 
            Parameters:
                TMSiDevice (String): Choose the TMSi Device that is used in combination with the USB TTL module (options are "SAGA" or "APEX")
                com_port (String): Port on which the USB TTL module was installed, defaults to False
        """
        
        # Find on which virtual COM port the device is located
        ports = serial.tools.list_ports.comports(include_links = False)
        print(ports)
        self.output_times = []
        self.input_times = []
        self.device = TMSiDevice
        
        # Port[0] on laptops that can automatically detect connected ports. 
        # For other laptops need to manually check the port the trigger cable is connected to.
        if ports and not com_port:
            com_port = ports[0] 
        try:
            self.ttl_device = serial.Serial(port=com_port, baudrate = 115200, timeout=0.0001)
            # Serial reset, reset COM port
            self.ttl_device.reset_output_buffer()
            # Reset module. For robust use, multiple resets are required
            self.ttl_device.flush()
            self.ttl_device.write(b'RR')
            
            # For robust use, close the port and reopen again
            self.ttl_device.close()
            self.ttl_device = serial.Serial(port=com_port, baudrate = 115200, timeout=0.0001)
            # Serial reset, reset COM port
            self.ttl_device.reset_output_buffer()
            print('Trigger event cable is ready!')
            # Reset module multiple times for robust use
            self.ttl_device.flush()
            self.ttl_device.write(b'RR')
            self.ttl_device.flush()
            self.ttl_device.write(b'RR')
            # Turn on red LED for 5 seconds
            self.ttl_device.write(b'0xff')
            self.ttl_device.flush()
            time.sleep(5)
            if self.device.upper() == "SAGA":
                # Write no bits as to get 0-baseline
                self.ttl_device.write(b'0x00')
            elif self.device.upper() == "APEX":
                # Write all bits as to get 0-baseline
                self.ttl_device.write(b'0xff')
        except:
            print('No Trigger event cable is found')
            raise TTLError("No trigger event cable is found")
            
    
    def write_trigger(self, trigger_value, duration = 0.01):
        """Function that controls the trigger generation of the USB-TTL module.
        Each trigger event lasts for 10ms by default (duration param)
        Specific functions for SAGA or APEX are defined
        """
        if self.device.upper() =="SAGA":
            # Convert the input value to a hexa-decimal format
            ser_write = '0x' + hex(trigger_value)[2:].zfill(2)
            # Convert to a byte format
            ser_write = bytes(ser_write, 'utf-8')
        elif self.device.upper() == "APEX":
            # Divide number by 2 to get correct alignment with TTL module
            trigger_value = trigger_value/2
            # Invert trigger value to get correct baseline
            trigger_value = (~int(trigger_value) & 0xff)
            ser_write = '0x' + hex(trigger_value)[2:].zfill(2)
            # Convert to a byte format
            ser_write = bytes(ser_write, 'utf-8')
        print(ser_write)
        # Write the trigger value to the device, which generates the hardware trigger.
        self.ttl_device.write(ser_write)
        
        self.output_times.append(time.perf_counter_ns())

        # Introduce delay for trigger to be detected using any sampling frequency
        time.sleep(duration) 
        # End trigger writing, get baseline back to 0
        if self.device == "SAGA":
            # Reset all bits as to get 0-baseline
            self.ttl_device.write(b'0x00')
        elif self.device == "APEX":
            # Write all bits as to get 0-baseline
            self.ttl_device.write(b'0xff')
        time.sleep(duration)
        
    def read_trigger(self):
        """Function that reads the Trigger In lines of the USB-TTL module"""
        trigger_in = self.ttl_device.readline()
        self.input_times.append(time.perf_counter_ns())
        if trigger_in ==  b'' :
            return None
        else:
            return bin(int(trigger_in, 16))[2:-8].zfill(8)
    
    def close(self):
        self.ttl_device.write(b'RR')
        self.ttl_device.close()

class TTLError(Exception):
    "Raised when the TTL module or Trigger cable is not found"
    pass

        
if __name__ == '__main__':
    # Create the handle to the module
    ttl_module = USB_TTL_device(com_port = 'COM7')

    # Write 10 trigger events, and print the read value
    for i in range(5):
        ttl_module.write_trigger(trigger_value = 255 - i, duration = 0.5)
        time.sleep(1)

    ttl_module.close()
