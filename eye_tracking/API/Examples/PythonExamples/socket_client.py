# Copyright (C) Smart Eye AB 2002-2018
# THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
''' Module containing functionality regarding getting logs from TCP/UDP connection

    Intended to receive the data output from SmartEyePro application and
    log it in a JSON structured logfile.

    Example on how to use it:
    client = socket_client.SocketClient()

    client.init("127.0.0.1", 5002, "TCP")
    client.set_start_frame(start_frame)
    client.set_stop_frame(stop_frame)
    client.connect()
    client.receive()
'''
from __future__ import absolute_import
from __future__ import print_function

import socket
import ctypes
import json
import collections
import os
import socket_types

# Header size definitions
HEADER_SIZE = 8
SUBHEADER_SIZE = 4

# This is the mapping between the types from
# output data file(data_output.json) and the internal
# types that are used to store received data.
SETYPE_TO_INTERNAL_TYPE_MAPPING = {
    'SEType_u8': ctypes.c_uint8(),
    'SEType_u16': ctypes.c_uint16(),
    'SEType_u32': ctypes.c_uint32(),
    'SEType_s32': ctypes.c_int32(),
    'SEType_u64': ctypes.c_uint64(),
    'SEType_f32': ctypes.c_float(),
    'SEType_f64': ctypes.c_double(),
    'SEType_Point2D': socket_types.SETypePoint2D(),
    'SEType_Vect2D': socket_types.SETypeVect2D(),
    'SEType_Point3D': socket_types.SETypePoint3D(),
    'SEType_Vect3D': socket_types.SETypeVect3D(),
    'SEType_Quaternion': socket_types.SETypeQuaternion(),
    'SEType_String': socket_types.SETypeString(),
    'SEType_UserMarker': socket_types.SETypeUserMarker(),
    'SEType_PupilMatchPointAnalysis': 'SEType_PupilMatchPointAnalysis',
    'SEType_WorldIntersection': socket_types.SETypeWorldIntersection(),
    # Handled exactly the same as a single WorldIntersection
    'SEType_WorldIntersections': socket_types.SETypeWorldIntersection(),
    # Just indicates that it is a vector, will be handled
    # according to the vector element types.
    'SEType_Vector': 'Vector',
    'SEType_Struct': 'SEType_Struct',
    'SEType_PacketHeader': socket_types.SEPacketHeader(),
    'SEType_SubPacketHeader': socket_types.SESubPacketHeader(),
    # No output of these types, but they are here since they
    # exists in data_types.json
    'SEType_Matrix3x3': "SEType_Matrix3x3",
    'SEType_Matrix2x2': "SEType_Matrix2x2"
}

# Deprecated data types
SETYPE_DEPRECATED = ['SEType_float']


class SocketClient(object):
    '''
    SocketClient class for connection to SEP and handle the TCP/UDP packets.
    '''
    host = "127.0.0.1"
    tcp_port = 5002
    udp_port = 5001

    use_udp = False
    connection = None

    # Holds received data that will be written to
    # json log file
    json_data = {}

    # Internally keep track of which frame number
    # we are currently logging
    frame_number = 0

    # Specifies which frames to log between
    start_frame = -1
    stop_frame = -1

    # Store parsed data of output data file(data_output.json)
    output_id_to_internal_type = {}
    # Store parsed data from data_types.json
    type_id_to_internal_type = {}
    # Store json files containing output data
    output_data_file = ''
    # Store json files containing output types
    data_types_file = ''
    output_file = "socket_log.json"

    def init(self, host, port, connection_type):
        ''' Initialize socket connection '''
        self.connection_type = connection_type.lower()
        self.host = host
        if connection_type == "udp":
            self.udp_port = port
            self.use_udp = True
        elif connection_type == "tcp":
            self.tcp_port = port
            self.use_udp = False
        else:
            print("Connection type not recognize. Use either TCP or UDP")
        data_output_parsed = self.__parse_data_output_json()
        data_types_parsed = self.__parse_data_types_json()
        return data_output_parsed and data_types_parsed

    def set_output_data_file(self, output_data_file):
        self.output_data_file = output_data_file

    def set_data_types_file(self, data_types_file):
        self.data_types_file = data_types_file

    def set_output_file(self, output_file):
        self.output_file = output_file

    def __parse_data_output_json(self):
        ''' Parses output data file(data_output.json) and store information
            in internal mapping to be able to handle each output type
            correctly.
        '''
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, self.output_data_file)
        try:
            with open(filename, 'r') as data_output_file:
                raw_str = data_output_file.read()
        except IOError as error:
            print("Unable to get output id specification. Error: %s" % error)
            return False

        json_object = json.loads(
            raw_str, object_pairs_hook=collections.OrderedDict)
        for items in json_object:
            data_type = SETYPE_TO_INTERNAL_TYPE_MAPPING[items['DataType']]
            name = items['Name']
            self.output_id_to_internal_type[int(items['EnumNumber'], 16)] = {
                'type': data_type,
                'name': name
            }
        return True

    def __parse_data_types_json(self):
        ''' Parse data_types.json and create map between type and id
        '''
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, self.data_types_file)
        try:
            with open(filename, 'r') as data_types_file:
                raw_str = data_types_file.read()
        except IOError as error:
            print("Unable to get data type specification. Error: %s" % error)
            return False

        json_object = json.loads(
            raw_str, object_pairs_hook=collections.OrderedDict)
        map_id = 0
        for items in json_object:
            if items['DataType'] in SETYPE_DEPRECATED:
                continue
            data_type = SETYPE_TO_INTERNAL_TYPE_MAPPING[items['DataType']]
            self.type_id_to_internal_type[map_id] = data_type
            map_id += 1
        return True

    def set_start_frame(self, frame_number):
        ''' Set start frame'''
        self.start_frame = frame_number

    def set_stop_frame(self, frame_number):
        ''' Set stop frame'''
        self.stop_frame = frame_number

    def connect(self):
        ''' Connect to SmartEyePro application '''
        print("Init socket connection...\n")
        if self.use_udp:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.connection.bind((self.host, self.udp_port))
        else:  # TCP
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.connection.connect((self.host, self.tcp_port))
            except socket.error as error:
                print(error)
                return False
        print("Connection established\n")
        return True

    def __get_packet_size(self):
        ''' Get size of received packet '''
        packet_header = socket_types.SEPacketHeader()
        # Not really sure why, but with TCP the receive
        # timed out inside try statement.
        if self.use_udp is False:
            self.connection.recv_into(packet_header, HEADER_SIZE, 2)
        else:
            try:
                self.connection.recv_into(packet_header, HEADER_SIZE, 2)
            except socket.error as error:
                # packet_header is smaller than the whole packet,
                # but thats okay
                if error.args[0] == 10040:
                    pass
                else:
                    print(error)
        packet_size = self.__shift_byte_order(packet_header.length,
                                              ctypes.c_uint16())
        packet_size.value += ctypes.sizeof(socket_types.SEPacketHeader())
        return packet_size

    def __get_packet(self, packet_size):
        ''' Receive packet '''
        packet = ctypes.create_string_buffer(packet_size.value)
        self.connection.recv_into(packet, packet_size.value, 0)
        return packet

    def __get_sub_packet_header_info(self, packet, bytes_read):
        ''' Get id and size of sub packet'''
        sub_packet_header = ctypes.pointer(socket_types.SESubPacketHeader())
        ctypes.memmove(sub_packet_header, ctypes.byref(packet, bytes_read),
                       SUBHEADER_SIZE)
        sub_packet_length = self.__shift_byte_order(
            sub_packet_header.contents.length, ctypes.c_uint16())
        sub_packet_id = self.__shift_byte_order(sub_packet_header.contents.id,
                                                ctypes.c_uint16())
        return sub_packet_length, sub_packet_id

    def __store_received_data(self, packet, sub_packet_id, bytes_read):
        ''' Store received sub packet data '''
        # Some special handling for receiving frameNr
        if sub_packet_id.value == 1:
            sub_packet_type = self.output_id_to_internal_type[
                sub_packet_id.value]['type']
            sub_packet = self.__get_base_type_data(sub_packet_type, packet,
                                                   bytes_read)
            self.frame_number = sub_packet.contents.value
            if self.start_frame <= self.frame_number or self.stop_frame == -1:
                self.json_data[self.frame_number] = {}
        else:  # Receiving any other subpacket
            if self.start_frame <= self.frame_number or self.stop_frame == -1:
                if sub_packet_id.value not in self.output_id_to_internal_type:
                    print("Unsupported type %s added, " \
                        "add it to output_id_to_internal_type dictionary!" \
                            % sub_packet_id.value)
                    return
                sub_packet_type = self.output_id_to_internal_type[
                    sub_packet_id.value]['type']

                self.__store_sub_packet(sub_packet_type, packet, bytes_read,
                                        sub_packet_id)

    def __store_sub_packet(self, sub_packet_type, packet, bytes_read,
                           sub_packet_id):
        ''' Handles reading and storing of sub packet depending on sub packet type
        '''
        if sub_packet_type == "Vector":
            self.__store_vector_sub_packet(packet, bytes_read, sub_packet_id)
        elif isinstance(sub_packet_type,
                        (ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                         ctypes.c_int32, ctypes.c_uint64, ctypes.c_double)):
            sub_packet = self.__get_base_type_data(sub_packet_type, packet,
                                                   bytes_read)
            self.__save_to_log(sub_packet, sub_packet_type, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypePoint2D):
            sub_packet = self.__get_2d_point_data(packet, bytes_read)
            self.__save_to_log(sub_packet, sub_packet_type, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypeVect2D):
            sub_packet = self.__get_2d_point_data(packet, bytes_read)
            self.__save_to_log(sub_packet, sub_packet_type, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypePoint3D):
            sub_packet = self.__get_3d_point_data(packet, bytes_read)
            self.__save_to_log(sub_packet, sub_packet_type, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypeVect3D):
            sub_packet = self.__get_3d_point_data(packet, bytes_read)
            self.__save_to_log(sub_packet, sub_packet_type, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypeString):
            sub_packet = self.__get_string_data(packet, bytes_read)
            self.__save_to_log(sub_packet[0], sub_packet_type, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypeWorldIntersection):
            self.__store_world_intersection_sub_packet(
                sub_packet_type, packet, bytes_read, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypeQuaternion):
            sub_packet = self.__get_quaternion_data(packet, bytes_read)
            self.__save_to_log(sub_packet, sub_packet_type, sub_packet_id)
        elif isinstance(sub_packet_type, socket_types.SETypeUserMarker):
            self.__get_usermarker_data_and_save(packet, bytes_read,
                                                sub_packet_id)
        else:
            print("Unknown sub packet type received")

    def __store_world_intersection_sub_packet(self, sub_packet_type, packet,
                                              bytes_read, sub_packet_id):
        read_at = bytes_read

        nr_of_intersections = ctypes.pointer(ctypes.c_uint16())
        nr_of_intersections_size = ctypes.sizeof(ctypes.c_uint16())
        ctypes.memmove(nr_of_intersections, ctypes.byref(packet, read_at),
                       nr_of_intersections_size)
        nr_of_intersections.contents = self.__shift_byte_order(
            nr_of_intersections.contents.value, ctypes.c_uint16())
        read_at += nr_of_intersections_size
        nr_of_intersections_count = 0
        while nr_of_intersections_count < nr_of_intersections.contents.value:
            world_point, object_point, object_name, byte_count = \
                self.__get_world_intersection_data(packet, read_at)
            sub_packet = (world_point, object_point, object_name)
            self.__save_to_log(sub_packet, sub_packet_type, sub_packet_id)
            read_at += byte_count
            nr_of_intersections_count += 1

    def __store_vector_sub_packet(self, packet, bytes_read, sub_packet_id):
        # Keep track of which position to read from packet
        read_at = bytes_read
        # Get size of vector
        vector_size = ctypes.pointer(ctypes.c_uint16())
        read_size = ctypes.sizeof(ctypes.c_uint16())
        ctypes.memmove(vector_size, ctypes.byref(packet, read_at), read_size)
        vector_size.contents = self.__shift_byte_order(
            vector_size.contents.value, ctypes.c_uint16())
        read_at += read_size

        vector_size_count = 0
        while vector_size_count < vector_size.contents.value:
            # Get TypeId of the elements in the vector
            type_id = ctypes.pointer(ctypes.c_uint16())
            read_size = ctypes.sizeof(ctypes.c_uint16())
            ctypes.memmove(type_id, ctypes.byref(packet, read_at), read_size)
            type_id.contents = self.__shift_byte_order(type_id.contents.value,
                                                       ctypes.c_uint16())
            read_at += read_size

            vector_sub_type = self.type_id_to_internal_type[
                type_id.contents.value]
            # We do not currently support vectors containing SEType_Struct
            # If we encounter any we will ignore them and notify user
            if vector_sub_type == "SEType_Struct":
                print("Ignoring vector of type {}.".format(vector_sub_type))
                return
            vector_sub_type_size = ctypes.sizeof(vector_sub_type)
            self.__store_sub_packet(vector_sub_type, packet, read_at,
                                    sub_packet_id)

            read_at += vector_sub_type_size
            vector_size_count += 1

    def __get_base_type_data(self, sub_packet_type, packet, bytes_read):
        ''' Gets the data content of base type subpackets'''
        sub_packet_size = ctypes.sizeof(sub_packet_type)
        sub_packet = ctypes.pointer(sub_packet_type)
        ctypes.memmove(sub_packet, ctypes.byref(packet, bytes_read),
                       sub_packet_size)
        sub_packet.contents = self.__shift_byte_order(
            sub_packet.contents.value, sub_packet_type)
        return sub_packet

    def __get_quaternion_data(self, packet, bytes_read):
        ''' Gets the data content of quaternion
            type subpackets
        '''
        sub_packet_size = ctypes.sizeof(socket_types.SETypeQuaternion())
        sub_packet = ctypes.pointer(socket_types.SETypeQuaternion())

        ctypes.memmove(sub_packet, ctypes.byref(packet, bytes_read),
                       sub_packet_size)
        sub_packet.contents.w = self.__shift_byte_order(
            sub_packet.contents.w, ctypes.c_double())
        sub_packet.contents.x = self.__shift_byte_order(
            sub_packet.contents.x, ctypes.c_double())
        sub_packet.contents.y = self.__shift_byte_order(
            sub_packet.contents.y, ctypes.c_double())
        sub_packet.contents.z = self.__shift_byte_order(
            sub_packet.contents.z, ctypes.c_double())
        return sub_packet

    def __get_usermarker_data_and_save(self, packet, bytes_read,
                                       sub_packet_id):
        ''' Gets the data content of user marker
            type subpackets
        '''
        read_at = bytes_read

        marker_exist = ctypes.pointer(ctypes.c_uint16())
        marker_exist_size = ctypes.sizeof(ctypes.c_uint16())
        ctypes.memmove(marker_exist, ctypes.byref(packet, read_at),
                       marker_exist_size)

        marker_exist.contents = self.__shift_byte_order(
            marker_exist.contents.value, ctypes.c_uint16())

        read_at += marker_exist_size

        if (marker_exist.contents.value):
            sub_packet_size = ctypes.sizeof(socket_types.SETypeUserMarker())
            sub_packet = ctypes.pointer(socket_types.SETypeUserMarker())

            ctypes.memmove(sub_packet, ctypes.byref(packet, read_at),
                           sub_packet_size)
            sub_packet.contents.error = self.__shift_byte_order(
                sub_packet.contents.error, ctypes.c_int32())
            sub_packet.contents.cameraClock = self.__shift_byte_order(
                sub_packet.contents.cameraClock, ctypes.c_uint64())
            sub_packet.contents.cameraIdx = self.__shift_byte_order(
                sub_packet.contents.cameraIdx, ctypes.c_uint8())
            sub_packet.contents.data = self.__shift_byte_order(
                sub_packet.contents.data, ctypes.c_uint64())
            self.__save_to_log(sub_packet, socket_types.SETypeUserMarker(),
                               sub_packet_id)
        return 0

    # Point and Vect has same handling
    def __get_3d_point_data(self, packet, bytes_read):
        ''' Gets the data content of 3D point/vector
            type subpackets
        '''
        sub_packet_size = ctypes.sizeof(socket_types.SETypePoint3D())
        sub_packet = ctypes.pointer(socket_types.SETypePoint3D())

        ctypes.memmove(sub_packet, ctypes.byref(packet, bytes_read),
                       sub_packet_size)
        sub_packet.contents.x = self.__shift_byte_order(
            sub_packet.contents.x, ctypes.c_double())
        sub_packet.contents.y = self.__shift_byte_order(
            sub_packet.contents.y, ctypes.c_double())
        sub_packet.contents.z = self.__shift_byte_order(
            sub_packet.contents.z, ctypes.c_double())
        return sub_packet

    # Point and Vect has same handling
    def __get_2d_point_data(self, packet, bytes_read):
        ''' Gets the data content of 2D point/vector
            type subpackets
        '''
        sub_packet_size = ctypes.sizeof(socket_types.SETypePoint2D())
        sub_packet = ctypes.pointer(socket_types.SETypePoint2D())

        ctypes.memmove(sub_packet, ctypes.byref(packet, bytes_read),
                       sub_packet_size)
        sub_packet.contents.x = self.__shift_byte_order(
            sub_packet.contents.x, ctypes.c_double())
        sub_packet.contents.y = self.__shift_byte_order(
            sub_packet.contents.y, ctypes.c_double())
        return sub_packet

    def __get_world_intersection_data(self, packet, bytes_read):
        ''' Gets the data content of world intersections
            type subpackets
        '''
        byte_count = 0
        # Get world point (socket_types.SETypePoint3D)
        world_point = self.__get_3d_point_data(packet, bytes_read)
        byte_count += ctypes.sizeof(socket_types.SETypePoint3D)
        # Get Object point (socket_types.SETypePoint3D)
        object_point = self.__get_3d_point_data(packet,
                                                bytes_read + byte_count)
        byte_count += ctypes.sizeof(socket_types.SETypePoint3D)
        # Get object_name (socket_types.SETypeString
        object_name, string_byte_count = self.__get_string_data(
            packet, byte_count + bytes_read)
        byte_count += string_byte_count

        return world_point, object_point, object_name, byte_count

    def __get_string_data(self, packet, bytes_read):
        ''' Gets the data content of string type subpackets'''
        byte_count = 0
        # Get size of object_name
        object_name_size = ctypes.pointer(ctypes.c_uint16())
        read_size = ctypes.sizeof(ctypes.c_uint16())
        ctypes.memmove(object_name_size, ctypes.byref(packet, bytes_read),
                       read_size)
        object_name_size.contents = self.__shift_byte_order(
            object_name_size.contents.value, ctypes.c_uint16())
        byte_count += read_size
        # Get actual object_name
        object_name = ctypes.create_string_buffer(1024)
        if object_name_size.contents.value <= 1024:
            ctypes.memmove(object_name,
                           ctypes.byref(packet, bytes_read + read_size),
                           object_name_size.contents.value)
        byte_count += object_name_size.contents.value
        return object_name, byte_count

    def __save_3d_point_to_log(self, data_to_save, sub_packet_name):
        if sub_packet_name in self.json_data[self.frame_number]:
            json_data_item = self.json_data[self.frame_number][sub_packet_name]
            if isinstance(json_data_item, dict):
                json_data_item = [
                    json_data_item, {
                        'x': data_to_save.contents.x,
                        'y': data_to_save.contents.y,
                        'z': data_to_save.contents.z
                    }
                ]
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
            elif isinstance(json_data_item, list):
                json_data_item.append({
                    'x': data_to_save.contents.x,
                    'y': data_to_save.contents.y,
                    'z': data_to_save.contents.z
                })
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
        else:
            self.json_data[self.frame_number][sub_packet_name] = {
                'x': data_to_save.contents.x,
                'y': data_to_save.contents.y,
                'z': data_to_save.contents.z
            }

    def __save_quaternion_to_log(self, data_to_save, sub_packet_name):
        if sub_packet_name in self.json_data[self.frame_number]:
            json_data_item = self.json_data[self.frame_number][sub_packet_name]
            if isinstance(json_data_item, dict):
                json_data_item = [
                    json_data_item, {
                        'w': data_to_save.contents.w,
                        'x': data_to_save.contents.x,
                        'y': data_to_save.contents.y,
                        'z': data_to_save.contents.z
                    }
                ]
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
            elif isinstance(json_data_item, list):
                json_data_item.append({
                    'w': data_to_save.contents.w,
                    'x': data_to_save.contents.x,
                    'y': data_to_save.contents.y,
                    'z': data_to_save.contents.z
                })
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
        else:
            self.json_data[self.frame_number][sub_packet_name] = {
                'w': data_to_save.contents.w,
                'x': data_to_save.contents.x,
                'y': data_to_save.contents.y,
                'z': data_to_save.contents.z
            }

    def __save_usermarker_to_log(self, data_to_save, sub_packet_name):
        if sub_packet_name in self.json_data[self.frame_number]:
            json_data_item = self.json_data[self.frame_number][sub_packet_name]
            if isinstance(json_data_item, dict):
                json_data_item = [
                    json_data_item, {
                        'error': data_to_save.contents.error,
                        'cameraClock': data_to_save.contents.cameraClock,
                        'cameraIdx': data_to_save.contents.cameraIdx,
                        'data': data_to_save.contents.data
                    }
                ]
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
            elif isinstance(json_data_item, list):
                json_data_item.append({
                    'error':
                    data_to_save.contents.error,
                    'cameraClock':
                    data_to_save.contents.cameraClock,
                    'cameraIdx':
                    data_to_save.contents.cameraIdx,
                    'data':
                    data_to_save.contents.data
                })
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
        else:
            self.json_data[self.frame_number][sub_packet_name] = {
                'error': data_to_save.contents.error,
                'cameraClock': data_to_save.contents.cameraClock,
                'cameraIdx': data_to_save.contents.cameraIdx,
                'data': data_to_save.contents.data
            }

    def __save_2d_point_to_log(self, data_to_save, sub_packet_name):
        if sub_packet_name in self.json_data[self.frame_number]:
            json_data_item = \
                self.json_data[self.frame_number][sub_packet_name]
            if isinstance(json_data_item, dict):
                json_data_item = [
                    json_data_item, {
                        'x': data_to_save.contents.x,
                        'y': data_to_save.contents.y
                    }
                ]
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
            elif isinstance(json_data_item, list):
                json_data_item.append({
                    'x': data_to_save.contents.x,
                    'y': data_to_save.contents.y
                })
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
        else:
            self.json_data[self.frame_number][sub_packet_name] = {
                'x': data_to_save.contents.x,
                'y': data_to_save.contents.y
            }

    def __save_world_intersection_to_log(self, data_to_save, sub_packet_name):
        if sub_packet_name in self.json_data[self.frame_number]:
            json_data_item = \
                self.json_data[self.frame_number][sub_packet_name]
            if isinstance(json_data_item, dict):
                json_data_item = [
                    json_data_item, {
                        'WorldPoint': {
                            'x': data_to_save[0].contents.x,
                            'y': data_to_save[0].contents.y,
                            'z': data_to_save[0].contents.z
                        },
                        'ObjectPoint': {
                            'x': data_to_save[1].contents.x,
                            'y': data_to_save[1].contents.y,
                            'z': data_to_save[1].contents.z
                        },
                        'ObjectName': data_to_save[2].value.decode('utf-8')
                    }
                ]
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
            elif isinstance(json_data_item, list):
                json_data_item.append({
                    'WorldPoint': {
                        'x': data_to_save[0].contents.x,
                        'y': data_to_save[0].contents.y,
                        'z': data_to_save[0].contents.z
                    },
                    'ObjectPoint': {
                        'x': data_to_save[1].contents.x,
                        'y': data_to_save[1].contents.y,
                        'z': data_to_save[1].contents.z
                    },
                    'ObjectName':
                    data_to_save[2].value.decode('utf-8')
                })
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
        else:
            self.json_data[self.frame_number][sub_packet_name] = {
                'WorldPoint': {
                    'x': data_to_save[0].contents.x,
                    'y': data_to_save[0].contents.y,
                    'z': data_to_save[0].contents.z
                },
                'ObjectPoint': {
                    'x': data_to_save[1].contents.x,
                    'y': data_to_save[1].contents.y,
                    'z': data_to_save[1].contents.z
                },
                'ObjectName': data_to_save[2].value.decode('utf-8')
            }

    def __save_string_to_log(self, data_to_save, sub_packet_name):
        self.json_data[self.frame_number][sub_packet_name] = \
            data_to_save.value.decode('utf-8')

    def __save_base_type_to_log(self, data_to_save, sub_packet_name):
        if sub_packet_name in self.json_data[self.frame_number]:
            json_data_item = \
                self.json_data[self.frame_number][sub_packet_name]
            if isinstance(json_data_item, list):
                json_data_item.append(data_to_save.contents.value)
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
            else:
                json_data_item = [json_data_item, data_to_save.contents.value]
                self.json_data[self.frame_number][sub_packet_name] = \
                    json_data_item
        else:
            self.json_data[self.frame_number][sub_packet_name] = \
                data_to_save.contents.value

    def __save_to_log(self, data_to_save, data_type, sub_packet_id):
        ''' Save received sub packet data in json_data '''
        sub_packet_name = self.output_id_to_internal_type[sub_packet_id.value][
            'name']
        if isinstance(data_type,
                      (socket_types.SETypePoint3D, socket_types.SETypeVect3D)):
            self.__save_3d_point_to_log(data_to_save, sub_packet_name)
        elif isinstance(
                data_type,
            (socket_types.SETypePoint2D, socket_types.SETypeVect2D)):
            self.__save_2d_point_to_log(data_to_save, sub_packet_name)
        elif isinstance(data_type, socket_types.SETypeWorldIntersection):
            self.__save_world_intersection_to_log(data_to_save,
                                                  sub_packet_name)
        elif isinstance(data_type, socket_types.SETypeString):
            self.__save_string_to_log(data_to_save, sub_packet_name)
        elif isinstance(data_type, socket_types.SETypeQuaternion):
            self.__save_quaternion_to_log(data_to_save, sub_packet_name)
        elif isinstance(data_type, socket_types.SETypeUserMarker):
            self.__save_usermarker_to_log(data_to_save, sub_packet_name)
        else:
            self.__save_base_type_to_log(data_to_save, sub_packet_name)

    def receive(self):
        ''' Main loop for receiving packets '''
        print("Receiving socket data...\n")
        try:
            # Stop listening to packets when reached specified stop_frame
            while self.frame_number < self.stop_frame or self.stop_frame == -1:
                try:
                    # Get Packet size
                    packet_size = self.__get_packet_size()
                    # Retrieve packet with size from header
                    packet = self.__get_packet(packet_size)
                    # Start reading subPackets after packet_header
                    bytes_read = ctypes.sizeof(socket_types.SEPacketHeader())
                    while bytes_read < packet_size.value:
                        # Read out sub_packet size and id
                        sub_packet_length, sub_packet_id = \
                            self.__get_sub_packet_header_info(
                                packet, bytes_read)
                        bytes_read += SUBHEADER_SIZE
                        # Store packet data
                        self.__store_received_data(packet, sub_packet_id,
                                                   bytes_read)
                        bytes_read += sub_packet_length.value
                except socket.error as error:
                    print("Socket error: %s" % error)
                    return
            self.__write_to_file()
        except KeyboardInterrupt:
            self.__write_to_file()

    def __write_to_file(self):
        ''' Write json_data to json logfile'''
        print('Writing socket data to: {}'.format(self.output_file))
        with open(self.output_file, 'w') as log_file:
            log_file.write(
                json.dumps(self.json_data, indent=2, sort_keys=True))

    def print_json_data(self):
        ''' Print out json_data '''
        print(json.dumps(self.json_data))

    @staticmethod
    def __shift_byte_order(data, data_type):
        ''' Shift byte order '''
        nr_of_bytes = ctypes.sizeof(data_type)
        if isinstance(data_type, ctypes.c_uint8):
            temp_input = ctypes.c_uint8(data)
            temp_output = ctypes.c_uint8()
        elif isinstance(data_type, ctypes.c_uint16):
            temp_input = ctypes.c_uint16(data)
            temp_output = ctypes.c_uint16()
        elif isinstance(data_type, ctypes.c_uint32):
            temp_input = ctypes.c_uint32(data)
            temp_output = ctypes.c_uint32()
        elif isinstance(data_type, ctypes.c_int32):
            temp_input = ctypes.c_int32(data)
            temp_output = ctypes.c_int32()
        elif isinstance(data_type, ctypes.c_uint64):
            temp_input = ctypes.c_uint64(data)
            temp_output = ctypes.c_uint64()
        elif isinstance(data_type, ctypes.c_double):
            temp_input = ctypes.c_double(data)
            temp_output = ctypes.c_double()
        else:
            temp_output = data_type
        for the_bytes in range(0, nr_of_bytes):
            ctypes.memmove(
                ctypes.byref(temp_output, the_bytes),
                ctypes.byref(temp_input, nr_of_bytes - 1 - the_bytes), 1)
        return temp_output
