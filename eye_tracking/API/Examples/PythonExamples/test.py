# Copyright (C) Smart Eye AB 2002-2018
# THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
''' Module containing examples on how to use socket_client.py and can_client.py
'''
from __future__ import absolute_import
from __future__ import print_function

import json
import collections
import can_client
import socket_client
import argparse
import os
import sys
import socket as sockets
import time
import datetime
def validate_file_path(file):
    """'Type' for argparse - checks that file exists."""
    if not os.path.exists(file):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: path does not exist
        raise argparse.ArgumentTypeError("The path {0} does not"
                                         " exist.".format(file))
    return file


def receive_socket_data(mode, start_frame, stop_frame, output_data_file,
                        data_types_file, out_dir):
    client = socket_client.SocketClient()
    client.set_output_data_file(output_data_file)
    client.set_data_types_file(data_types_file)
    client.set_output_file(os.path.join(out_dir, 'socket_log.json'))
    result = False
    if mode == "tcp":
        result = client.init("127.0.0.1", 5002, mode)
    elif mode == "udp":
        result = client.init("127.0.0.1", 5001, mode)
    if result:
        client.set_start_frame(start_frame)
        client.set_stop_frame(stop_frame)
        if client.connect():
            client.receive()


def receive_can_data(start_frame, stop_frame, vxlapi_path, out_dir):
    client = can_client.CanClient()
    client.set_vxlapi_path(vxlapi_path)
    client.set_start_frame(start_frame)
    client.set_stop_frame(stop_frame)
    client.set_output_file(os.path.join(out_dir, 'can_log.json'))
    if client.init():
        client.receive()
        client.print_json_data()


def print_logs(out_dir):
    print("Printing logs...\n")
    try:
        can_log = os.path.join(out_dir, 'can_log.json')
        with open(can_log, 'r') as can_file:
            parsed_can_file = json.load(
                can_file, object_pairs_hook=collections.OrderedDict)
        print("Printing can log:\n")
        print_log(parsed_can_file)
    except IOError:
        print("No can log found!\n")
        pass

    try:
        socket_log = os.path.join(out_dir, 'socket_log.json')
        with open(socket_log, 'r') as socket_file:
            parsed_socket_file = json.load(
                socket_file, object_pairs_hook=collections.OrderedDict)
        print("Printing socket log:\n")
        print_log(parsed_socket_file)
    except IOError:
        print("No socket log found!\n")
        pass


def print_log(log):
    for frame_number in log:
        print("FrameNumber: %s" % frame_number)
        for message in log[frame_number]:
            print("Message: %s Value: %s" % (message,
                                             log[frame_number][message]))


def main():
    is_64bits = sys.maxsize > 2**32
    parser = argparse.ArgumentParser(
        description='Example of how to receive output over TCP/UDP and CAN.')
    parser.add_argument(
        '--data-output-file',
        dest='data_output_file',
        default='E:\projects\API\include\data_output.json',
        type=validate_file_path,
        help='Path to data types file(.json). Required for tcp/udp.')
    parser.add_argument(
        '--data-types-file',
        dest='data_types_file',
        default='E:\projects\API\include\data_types.json',
        type=validate_file_path,
        help='Path to data types file(.json). Required for tcp/udp.')
    parser.add_argument(
        '--vxlapi-path',
        dest='vxlapi_path',
        default='vxlapi64.dll' if is_64bits else 'vxlapi.dll',
        help='Path to data vxlapi.dll. Required for can.')
    parser.add_argument(
        '--mode',
        dest='mode',
        choices=['tcp', 'udp', 'can'],
        default='udp',
        # required=True,
        help="Receive tcp/udp/can data.")
    parser.add_argument(
        '--print-logs',
        dest='print_logs',
        action="store_true",
        help="Print logged ouput to command line.")
    parser.add_argument(
        '--start-frame',
        dest='start_frame',
        type=int,
        default=-1,
        help=
        "Start logging from this framenumber. If not specified all frames are logged"
    )
    parser.add_argument(
        '--stop-frame',
        dest='stop_frame',
        type=int,
        default=-1,
        help=
        "Stop logging at this framenumber. If not specified all frames are logged"
    )
    parser.add_argument(
        '--out-dir',
        dest='out_dir',
        type=validate_file_path,
        default=os.path.expanduser("~/Documents/Smart Eye/log"),
        help="Save collected logs to this directory.")

    print("\n*** Welcome to the Smart Eye Pro client Python example ***")
    print(
        "*** Please note that this example requires 'FrameNumber' to be selected in the Smart Eye Pro log specification. ***\n"
    )

    args = parser.parse_args()

    # receive_socket_data(args.mode, args.start_frame, args.stop_frame,
    #                         args.data_output_file, args.data_types_file,
    #                         args.out_dir)
    client = socket_client.SocketClient()
    client.set_output_data_file('E:\projects\API\include\data_output.json')
    client.set_data_types_file('E:\projects\API\include\data_types.json')
    client.set_output_file(os.path.join("E:\projects\API\log", 'socket_log.json'))
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y%m%d_%H%M%S")
    eye_data_file_path = f'E:\projects\log\eye_data_{formatted_time}.json'
    result = client.init("127.0.0.1", 1999, 'udp')
    eye_data=[]
    if result:
        client.set_start_frame(-1)
        client.set_stop_frame(-1)
        client.connect()
        with open(eye_data_file_path, 'a') as file: 
            while(1):
                client.receive()
                eye_data=client.json_data[list(client.json_data)[-1]]
                # 'a' mode to append data
                json.dump(eye_data, file)
                file.write('\n') 

if __name__ == "__main__":
    main()
