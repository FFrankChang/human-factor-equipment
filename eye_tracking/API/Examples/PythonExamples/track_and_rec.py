'''Sample code used to demo simultaneous tracking and recording.
'''
import argparse
import time

from Cli import external_interfaces


class TrackAndRecHelper:
    receive_timeout = 31556926

    def __init__(self, ip, port, record_path, log_path):
        self.ip_addr = ip
        self.port = port
        self.record_path = record_path
        self.log_path = log_path

        self.si = external_interfaces.ExternalInterface()

    def connect(self):
        print("Connecting to SEP.")
        self.si.connect(self.ip_addr, self.port)

        print("Setting recording file.")
        res = self.si.set_recording_file(self.record_path)
        if res != None:
            return False
        print("Setting log file.")
        res = self.si.set_log_file(self.log_path)
        if res != None:
            return False

        notifications = [
            'recordingStarted', 'recordingStopped', 'recordingError',
            'trackingStarted', 'trackingStopped'
        ]
        cbMap = {'recordingError': self.recording_error_cb}
        for notification in notifications:
            res = None
            if notification in cbMap:
                callback = cbMap[notification]
                print(
                    f"Subscribing to notification {notification} with callback {callback.__name__}."
                )
                res = self.si.subscribe_to_notificationCB(
                    notification, callback)
            else:
                print(f"Subscribing to notification {notification}.")
                res = self.si.subscribe_to_notification(notification)
            if res != None:
                return False

        return True

    def recording_error_cb(self):
        # Add actions to take on recording errors.
        print("recording_error_cb executed!")

    def start_tracking(self):
        print("Starting tracking.")
        self.si.start_tracking()
        self.si.start_log()

    def start_recording(self):
        print("Starting recording.")
        self.si.start_recording()
        self.si.get_recording_state()

    def stop_tracking(self):
        print("Stopping tracking.")
        self.si.stop_log()
        self.si.stop_tracking()

    def stop_recording(self):
        print("Stopping recording")
        self.si.stop_recording()
        self.si.get_recording_state()

    def disconnect(self):
        self.si.disconnect()


def main():
    parser = argparse.ArgumentParser(
        description='Track and Record feature demo.')
    parser.add_argument(
        '--record-time',
        '-t',
        dest='record_time',
        default=10,
        help='Time to record before stopping.',
        type=int)
    parser.add_argument(
        '--record-path',
        '-r',
        dest='rec_path',
        required=True,
        help='Recording storage path.',
        type=str)
    parser.add_argument(
        '--log-path',
        '-l',
        dest='log_path',
        required=True,
        help='Log storage path.',
        type=str)
    parser.add_argument(
        '--ip',
        dest='ip',
        default="127.0.0.1",
        help="RPC server ip address.",
        type=str)
    parser.add_argument(
        '--port',
        dest='port',
        default="8100",
        help="RPC server port.",
        type=str)
    args = parser.parse_args()

    helper = TrackAndRecHelper(args.ip, args.port, args.rec_path,
                               args.log_path)

    if not helper.connect():
        return

    helper.start_recording()
    helper.start_tracking()

    time.sleep(args.record_time)

    helper.stop_recording()
    helper.stop_tracking()

    helper.disconnect()


if __name__ == "__main__":
    main()
