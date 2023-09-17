# Copyright (C) Smart Eye AB 2002-2018
# THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
'''Module containing functionality regarding getting logs out from CAN connection

    Intended to receive the data output from SmartEyePro application and
    log it in a JSON structured logfile.

    Example on how to use it:
    client = can_client.CanClient()

    client.init()
    client.set_start_frame(start_frame)
    client.set_stop_frame(stop_frame)
    client.receive()
'''
from __future__ import absolute_import
from __future__ import print_function

import ctypes
import json
import can_types

XL_SUCCESS = 0
XL_BUS_TYPE_CAN = 0x00000001
XL_INVALID_PORTHANDLE = -1
XL_INTERFACE_VERSION = 3
XL_ACTIVATE_NONE = 0
RECEIVE_EVENT_SIZE = 1
XL_ERR_QUEUE_IS_EMPTY = 10
XL_RECEIVE_MSG = 1


class CanClient(object):
    '''
    CanClient class for connecting to SEP and handle can messages.
    '''
    vxlapi_path = ''
    vxlapi = None
    app_name = "SeCanClient".encode()
    hw_type = ctypes.pointer(ctypes.c_int())
    hw_index = ctypes.pointer(ctypes.c_int())
    hw_channel = ctypes.pointer(ctypes.c_int())

    channel_mask = can_types.XLACCESS(1)
    permission_mask = can_types.XLACCESS(1)
    port_handle = can_types.XLporthandle(XL_INVALID_PORTHANDLE)
    handle = ctypes.pointer(ctypes.c_uint())
    msgsrx = ctypes.pointer(ctypes.c_int())

    xl_event = ctypes.pointer(can_types.SXlEvent())

    # Holds received data that will be written to
    # json log file
    json_data = {}

    frame_number = 0
    frame_number_non_real = 0

    start_frame = -1
    stop_frame = -1

    output_file = "can_log.json"

    @staticmethod
    def get_data(nr_of_bytes, data, offset):
        ''' Returns nr_of_bytes from data with a certain offset'''
        result = 0
        count = 0
        for byte_data in range(0 + offset, nr_of_bytes + offset):
            temp_data = data[byte_data]
            result += (temp_data << (count * 8))
            count = count + 1
        return result

    @staticmethod
    def get_data_signed(nr_of_bytes, data, offset):
        ''' Returns signed nr_of_bytes from data with a certain offset'''
        result = 0
        count = 0
        for byte_data in range(0 + offset, nr_of_bytes + offset):
            temp_data = data[byte_data]
            result += (temp_data << (count * 8))
            count = count + 1
        if nr_of_bytes == 2:
            return ctypes.c_int16(result).value
        if nr_of_bytes == 4:
            return ctypes.c_int32(result).value

    def set_vxlapi_path(self, path):
        self.vxlapi_path = path

    def init(self):
        print("Init can connection...")
        print("Loading vxlapi: '{}'.".format(self.vxlapi_path))
        try:
            self.vxlapi = ctypes.windll.LoadLibrary(self.vxlapi_path)
        except OSError as error:
            print("vxlapi.dll could not be loaded: {}".format(error))
            return False
        ''' Initializes the can client to be able to receive messages'''
        result = self.__open_driver()
        if result != XL_SUCCESS:
            print("xlOpenDriver failure errorCode: %s" % result)
            return False
        result = self.__get_appl_config()
        if result != XL_SUCCESS:
            print("xlGetApplConfig failure errorCode: %s" % result)
            return False
        result = self.__get_channel_mask()
        if not self.channel_mask:
            print("xlGetChannelMask failure")
            return False
        result = self.__open_port()
        if result != XL_SUCCESS:
            print("xlOpenPort failure errorCode: %s" % result)
            return False
        result = self.__activate_channel()
        if result != XL_SUCCESS:
            print("xlActivateChannel failure errorCode: %s" % result)
            return False
        result = self.__set_notification()
        if result != XL_SUCCESS:
            print("xlSetNotification failure errorCode: %s" % result)
            return False
        print("Connection established\n")
        return True

    def __open_driver(self):
        ''' Open the xl driver '''
        result = self.vxlapi.xlOpenDriver()
        return result

    def __get_appl_config(self):
        ''' Get application configuration information for specified can channel'''
        result = self.vxlapi.xlGetApplConfig(self.app_name, 0, self.hw_type,
                                             self.hw_index, self.hw_channel,
                                             XL_BUS_TYPE_CAN)
        return result

    def __get_channel_mask(self):
        ''' Get channel mask'''
        self.channel_mask = ctypes.c_ulonglong(
            self.vxlapi.xlGetChannelMask(self.hw_type.contents,
                                         self.hw_index.contents,
                                         self.hw_channel.contents))

    def __open_port(self):
        ''' Open port for port_handle'''
        self.permission_mask.contents = self.channel_mask
        self.vxlapi.xlOpenPort.argtypes = [
            ctypes.POINTER(can_types.XLporthandle), ctypes.c_char_p,
            can_types.XLACCESS,
            ctypes.POINTER(can_types.XLACCESS), ctypes.c_uint, ctypes.c_uint,
            ctypes.c_uint
        ]
        result = self.vxlapi.xlOpenPort(
            self.port_handle, self.app_name, self.channel_mask,
            self.permission_mask, 256, XL_INTERFACE_VERSION, XL_BUS_TYPE_CAN)
        return result

    def __activate_channel(self):
        ''' Activate can channel '''
        result = self.vxlapi.xlActivateChannel(
            self.port_handle, self.channel_mask, XL_BUS_TYPE_CAN,
            XL_ACTIVATE_NONE)
        return result

    def __set_notification(self):
        ''' Set notification handle '''
        result = self.vxlapi.xlSetNotification(self.port_handle, self.handle,
                                               1)
        return result

    def set_start_frame(self, frame_number):
        ''' Set start frame '''
        self.start_frame = frame_number

    def set_stop_frame(self, frame_number):
        ''' Set stop frame '''
        self.stop_frame = frame_number

    def set_output_file(self, output_file):
        self.output_file = output_file

    def __store_can_synch(self, data):
        self.frame_number = self.get_data(4, data, 0)
        time_stamp = self.get_data(2, data, 4) / 10000.0
        estimated_delay = self.get_data(2, data, 6) / 10000.0
        # Only log between given frames
        if self.start_frame <= self.frame_number <= self.stop_frame or self.stop_frame == -1:
            self.json_data[self.frame_number] = {}
            self.json_data[self.frame_number]['TimeStamp'] = time_stamp
            self.json_data[self.frame_number][
                'EstimatedDelay'] = estimated_delay

    def __store_can_user_time_stamp(self, data):
        user_time_stamp = self.get_data(8, data, 0)
        self.json_data[self.frame_number]['UserTimeStamp'] = user_time_stamp

    def __store_can_head_position(self, data):
        head_position_x = self.get_data_signed(2, data, 0) / 10000.0
        head_position_y = self.get_data_signed(2, data, 2) / 10000.0
        head_position_z = self.get_data_signed(2, data, 4) / 10000.0
        head_position_q = self.get_data_signed(2, data, 6) / 10000.0
        self.json_data[self.frame_number]['HeadPosition'] = {
            'x': head_position_x,
            'y': head_position_y,
            'z': head_position_z
        }
        self.json_data[self.frame_number]['HeadPositionQ'] = head_position_q

    def __store_can_head_rotation(self, data):
        head_rotation_x = self.get_data_signed(2, data, 0) / 10000.0
        head_rotation_y = self.get_data_signed(2, data, 2) / 10000.0
        head_rotation_z = self.get_data_signed(2, data, 4) / 10000.0
        head_rotation_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number]['HeadRotationRodrigues'] = {
            'x': head_rotation_x,
            'y': head_rotation_y,
            'z': head_rotation_z
        }
        self.json_data[self.frame_number]['HeadRotationQ'] = head_rotation_q

    def __store_can_gaze_origin(self, data):
        gaze_origin_x = self.get_data_signed(2, data, 0) / 10000.0
        gaze_origin_y = self.get_data_signed(2, data, 2) / 10000.0
        gaze_origin_z = self.get_data_signed(2, data, 4) / 10000.0
        gaze_origin_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number]['GazeOrigin'] = {
            'x': gaze_origin_x,
            'y': gaze_origin_y,
            'z': gaze_origin_z
        }
        self.json_data[self.frame_number]['GazeOriginQ'] = gaze_origin_q

    def __store_can_gaze_direction(self, data):
        gaze_direction_x = self.get_data_signed(2, data, 0) / 10000.0
        gaze_direction_y = self.get_data_signed(2, data, 2) / 10000.0
        gaze_direction_z = self.get_data_signed(2, data, 4) / 10000.0
        gaze_direction_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number]['GazeDirection'] = {
            'x': gaze_direction_x,
            'y': gaze_direction_y,
            'z': gaze_direction_z
        }
        self.json_data[self.frame_number]['GazeDirectionQ'] = gaze_direction_q

    def __store_can_eye_closure(self, data):
        eyelid_opening = self.get_data_signed(2, data, 0) / 10000.0
        eyelid_opening_q = self.get_data(2, data, 2) / 10000.0
        self.json_data[self.frame_number]['EyelidOpening'] = eyelid_opening
        self.json_data[self.frame_number]['EyelidOpeningQ'] = eyelid_opening_q

    def __store_can_both_eye_closures(self, data):
        left_eyelid_opening = self.get_data_signed(2, data, 0) / 10000.0
        left_eyelid_opening_q = self.get_data(2, data, 2) / 10000.0
        right_eyelid_opening = self.get_data_signed(2, data, 4) / 10000.0
        right_eyelid_opening_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number][
            'LeftEyelidOpening'] = left_eyelid_opening
        self.json_data[self.frame_number][
            'LeftEyelidOpeningQ'] = left_eyelid_opening_q
        self.json_data[self.frame_number][
            'RightEyelidOpening'] = right_eyelid_opening
        self.json_data[self.frame_number][
            'RightEyelidOpeningQ'] = right_eyelid_opening_q

    def __store_can_pupil_diameter(self, data):
        pupil_diameter = self.get_data_signed(2, data, 0) / 10000.0
        pupil_diameter_q = self.get_data(2, data, 2) / 10000.0
        self.json_data[self.frame_number]['PupilDiameter'] = pupil_diameter
        self.json_data[self.frame_number]['PupilDiameterQ'] = pupil_diameter_q

    def __store_can_both_pupil_diameters(self, data):
        left_pupil_diameter = self.get_data_signed(2, data, 0) / 10000.0
        left_pupil_diameter_q = self.get_data(2, data, 2) / 10000.0
        right_pupil_diameter = self.get_data_signed(2, data, 4) / 10000.0
        right_pupil_diameter_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number][
            'LeftPupilDiameter'] = left_pupil_diameter
        self.json_data[self.frame_number][
            'LeftPupilDiameterQ'] = left_pupil_diameter_q
        self.json_data[self.frame_number][
            'RightPupilDiameter'] = right_pupil_diameter
        self.json_data[self.frame_number][
            'RightPupilDiameterQ'] = right_pupil_diameter_q

    def __store_can_ascii_key(self, data):
        assci_keyboard_state = self.get_data(1, data, 0)
        self.json_data[self.frame_number][
            'ASCIIKeyboardState'] = assci_keyboard_state

    def __store_can_world_intersection(self, data):
        zone_id = self.get_data(2, data, 0)
        object_point_x = self.get_data_signed(2, data, 2)
        object_point_y = self.get_data_signed(2, data, 4)
        object_point_z = self.get_data_signed(2, data, 6)
        self.json_data[self.frame_number]['WorldIntersection'] = {
            'x': object_point_x,
            'y': object_point_y,
            'z': object_point_z,
            'id': zone_id
        }

    def __store_can_filtered_gaze_direction(self, data):
        filtered_gaze_direction_x = self.get_data_signed(2, data, 0) / 10000.0
        filtered_gaze_direction_y = self.get_data_signed(2, data, 2) / 10000.0
        filtered_gaze_direction_z = self.get_data_signed(2, data, 4) / 10000.0
        filtered_gaze_direction_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number]['FilteredGazeDirection'] = {
            'x': filtered_gaze_direction_x,
            'y': filtered_gaze_direction_y,
            'z': filtered_gaze_direction_z
        }
        self.json_data[self.frame_number]['FilteredGazeDirectionQ'] = \
            filtered_gaze_direction_q

    def __store_can_filtered_left_gaze_direction(self, data):
        filtered_left_gaze_direction_x = self.get_data_signed(2, data,
                                                              0) / 10000.0
        filtered_left_gaze_direction_y = self.get_data_signed(2, data,
                                                              2) / 10000.0
        filtered_left_gaze_direction_z = self.get_data_signed(2, data,
                                                              4) / 10000.0
        filtered_left_gaze_direction_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number]['FilteredLeftGazeDirection'] = {
            'x': filtered_left_gaze_direction_x,
            'y': filtered_left_gaze_direction_y,
            'z': filtered_left_gaze_direction_z
        }
        self.json_data[self.frame_number]['FilteredLeftGazeDirectionQ'] = \
            filtered_left_gaze_direction_q

    def __store_can_filtered_right_gaze_direction(self, data):
        filtered_right_gaze_direction_x = self.get_data_signed(2, data,
                                                               0) / 10000.0
        filtered_right_gaze_direction_y = self.get_data_signed(2, data,
                                                               2) / 10000.0
        filtered_right_gaze_direction_z = self.get_data_signed(2, data,
                                                               4) / 10000.0
        filtered_right_gaze_direction_q = self.get_data(2, data, 6) / 10000.0
        self.json_data[self.frame_number]['FilteredRightGazeDirection'] = {
            'x': filtered_right_gaze_direction_x,
            'y': filtered_right_gaze_direction_y,
            'z': filtered_right_gaze_direction_z
        }
        self.json_data[self.frame_number]['FilteredRightGazeDirectionQ'] = \
            filtered_right_gaze_direction_q

    def __store_can_synch_non_realtime(self, data):
        self.frame_number = self.get_data(4, data, 0)
        time_stamp = self.get_data(2, data, 4) / 10000.0
        estimated_delay = self.get_data(2, data, 6) / 10000.0
        # Only log between given frames
        if self.start_frame <= self.frame_number:
            if self.frame_number not in self.json_data:
                self.json_data[self.frame_number] = {}
            self.json_data[self.frame_number]['TimeStampNonReal'] = time_stamp
            self.json_data[self.frame_number][
                'EstimatedDelayNonReal'] = estimated_delay

    def __store_can_user_time_stamp_non_real_time(self, data):
        user_time_stamp = self.get_data(8, data, 0)
        self.json_data[self.frame_number][
            'UserTimeStampNonRealTime'] = user_time_stamp

    def __store_can_blink(self, data):
        blink = self.get_data(4, data, 0)
        self.json_data[self.frame_number]['Blink'] = blink

    def __store_can_saccade(self, data):
        saccade = self.get_data(4, data, 0)
        self.json_data[self.frame_number]['Saccade'] = saccade

    def __store_can_left_blink_closing_mid_time(self, data):
        left_blink_closing_mid_time = self.get_data(8, data, 0)
        self.json_data[self.frame_number]['LeftBlinkClosingMidTime'] = \
            left_blink_closing_mid_time

    def __store_can_left_blink_closing_amplitude(self, data):
        left_blink_closing_amplitude = self.get_data_signed(2, data,
                                                            0) / 10000.0
        self.json_data[self.frame_number]['LeftBlinkClosingAmplitude'] = \
            left_blink_closing_amplitude

    def __store_can_left_blink_closing_speed(self, data):
        left_blink_closing_speed = self.get_data_signed(2, data, 0) / 10000.0
        self.json_data[self.frame_number]['LeftBlinkClosingSpeed'] = \
            left_blink_closing_speed

    def __store_can_left_blink_opening_mid_time(self, data):
        left_blink_opening_mid_time = self.get_data(8, data, 0)
        self.json_data[self.frame_number]['LeftBlinkOpeningMidTime'] = \
            left_blink_opening_mid_time

    def __store_can_left_blink_opening_amplitude(self, data):
        left_blink_opening_amplitude = self.get_data_signed(2, data,
                                                            0) / 10000.0
        self.json_data[self.frame_number]['LeftBlinkOpeningAmplitude'] = \
            left_blink_opening_amplitude

    def __store_can_left_blink_opening_speed(self, data):
        left_blink_opening_speed = self.get_data(2, data, 0) / 10000.0
        self.json_data[self.frame_number]['LeftBlinkOpeningSpeed'] = \
            left_blink_opening_speed

    def __store_can_right_blink_closing_mid_time(self, data):
        right_blink_closing_mid_time = self.get_data(8, data, 0)
        self.json_data[self.frame_number]['RightBlinkClosingMidTime'] = \
            right_blink_closing_mid_time

    def __store_can_right_blink_closing_amplitude(self, data):
        right_blink_closing_amplitude = self.get_data_signed(2, data,
                                                             0) / 10000.0
        self.json_data[self.frame_number]['RightBlinkClosingAmplitude'] = \
            right_blink_closing_amplitude

    def __store_can_right_blink_closing_speed(self, data):
        right_blink_closing_speed = self.get_data_signed(2, data, 0) / 10000.0
        self.json_data[self.frame_number]['RightBlinkClosingSpeed'] = \
            right_blink_closing_speed

    def __store_can_right_blink_opening_mid_time(self, data):
        right_blink_opening_mid_time = self.get_data(8, data, 0)
        self.json_data[self.frame_number]['RightBlinkOpeningMidTime'] = \
            right_blink_opening_mid_time

    def __store_can_right_blink_opening_amplitude(self, data):
        right_blink_opening_amplitude = self.get_data_signed(2, data,
                                                             0) / 10000.0
        self.json_data[self.frame_number]['RightBlinkOpeningAmplitude'] = \
            right_blink_opening_amplitude

    def __store_can_right_blink_opening_speed(self, data):
        right_blink_opening_speed = self.get_data_signed(2, data, 0) / 10000.0
        self.json_data[self.frame_number]['RightBlinkOpeningSpeed'] \
            = right_blink_opening_speed

    def __store_received_data(self, msg_id, data):  #pylint: disable=R0915,R0912
        ''' Store can message depending on msg_id '''
        if msg_id == 1:
            self.__store_can_synch(data)
        if msg_id == 16:
            self.__store_can_synch_non_realtime(data)
        # Only log between given frames
        if self.start_frame <= self.frame_number <= self.stop_frame or self.stop_frame == -1:
            if msg_id == 2:
                self.__store_can_user_time_stamp(data)
            if msg_id == 3:
                self.__store_can_head_position(data)
            if msg_id == 4:
                self.__store_can_head_rotation(data)
            if msg_id == 5:
                self.__store_can_gaze_origin(data)
            if msg_id == 6:
                self.__store_can_gaze_direction(data)
            if msg_id == 7:
                self.__store_can_eye_closure(data)
            if msg_id == 8:
                self.__store_can_both_eye_closures(data)
            if msg_id == 9:
                self.__store_can_pupil_diameter(data)
            if msg_id == 10:
                self.__store_can_both_pupil_diameters(data)
            if msg_id == 11:
                self.__store_can_ascii_key(data)
            if msg_id == 12:
                self.__store_can_world_intersection(data)
            if msg_id == 13:
                self.__store_can_filtered_gaze_direction(data)
            if msg_id == 14:
                self.__store_can_filtered_left_gaze_direction(data)
            if msg_id == 15:
                self.__store_can_filtered_right_gaze_direction(data)
            if msg_id == 17:
                self.__store_can_user_time_stamp_non_real_time(data)
            if msg_id == 18:
                self.__store_can_blink(data)
            if msg_id == 19:
                self.__store_can_saccade(data)
            if msg_id == 20:
                self.__store_can_left_blink_closing_mid_time(data)
            if msg_id == 21:
                self.__store_can_left_blink_closing_amplitude(data)
            if msg_id == 22:
                self.__store_can_left_blink_closing_speed(data)
            if msg_id == 23:
                self.__store_can_left_blink_opening_mid_time(data)
            if msg_id == 24:
                self.__store_can_left_blink_opening_amplitude(data)
            if msg_id == 25:
                self.__store_can_left_blink_opening_speed(data)
            if msg_id == 26:
                self.__store_can_right_blink_closing_mid_time(data)
            if msg_id == 27:
                self.__store_can_right_blink_closing_amplitude(data)
            if msg_id == 28:
                self.__store_can_right_blink_closing_speed(data)
            if msg_id == 29:
                self.__store_can_right_blink_opening_mid_time(data)
            if msg_id == 30:
                self.__store_can_right_blink_opening_amplitude(data)
            if msg_id == 31:
                self.__store_can_right_blink_opening_speed(data)
            if msg_id > 31:
                print("Unknown message with id: %s received" % msg_id)

    def receive(self):
        ''' Start receive the can messages '''
        print("Please note that this example assumes SE_CAN_SYNCH is logged.")
        print("Receiving can data...\n")
        try:
            while self.frame_number < self.stop_frame or self.stop_frame == -1:
                result = XL_SUCCESS
                while not result:
                    self.msgsrx.contents = ctypes.c_long(RECEIVE_EVENT_SIZE)
                    result = self.vxlapi.xlReceive(self.port_handle,
                                                   self.msgsrx, self.xl_event)
                    if result != XL_ERR_QUEUE_IS_EMPTY:
                        if self.xl_event.contents.tag == XL_RECEIVE_MSG:
                            msg_id = self.xl_event.contents.tagData.msg.id - 0x400
                            data = self.xl_event.contents.tagData.msg.data
                            self.__store_received_data(msg_id, data)
            self.__write_to_file()
        except KeyboardInterrupt:
            self.__write_to_file()

    def __write_to_file(self):
        ''' Write json_data to file'''
        print('Writing can data to: {}'.format(self.output_file))
        with open(self.output_file, 'w') as log_file:
            log_file.write(
                json.dumps(self.json_data, indent=2, sort_keys=True))

    def print_json_data(self):
        ''' Print json data '''
        print(json.dumps(self.json_data))
