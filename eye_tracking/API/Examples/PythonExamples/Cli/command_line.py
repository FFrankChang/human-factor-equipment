# Copyright (C) Smart Eye AB 2002-2023
# THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
''' Command line interface to communicate with RPC server

    command_line.py parse the commands along with arguments
    from prompt and pass them to external_interfaces.py.

'''
from __future__ import print_function
from __future__ import absolute_import

import cmd
import external_interfaces


# pylint: disable=R0904,C0103,W0613
# Disabling R0904: Too many public methods since they have to be to be visible from command line
# Disabling C0103: Invalid method name to keep the purpose of the command clear
# Disabling W0613: Unused argument since we need to read command line input
class ExternalInterfacesCommands(cmd.Cmd):
    """ Commands processor """
    ext_interface = external_interfaces.ExternalInterface()

    def __init__(self):
        cmd.Cmd.__init__(self)

    # Introduction message
    intro = 'Welcome to the Smart Eye JSON-RPC ExternalInterface test shell.' \
            '\nType help or ? to list commands.\n'

    # Prompt
    prompt = ">>>> "

    def emptyline(self):
        pass

    # Commands
    def do_connect(self, line):
        """ Connect to the JSON_RPC server """
        args = line.split(' ')
        try:  # Cast to int will cause ValueError when unable to cast
            if len(args) > 1:
                self.ext_interface.connect(args[0], int(args[1]))
            else:
                print("Usage: connect IP PORT")
        except ValueError:
            print("Invalid PORT - Must be an integer value")

    def do_disconnect(self, line):
        """ Disconnect from JSON RPC"""
        self.ext_interface.disconnect()

    # Ping
    def do_ping(self, line):
        """ Sends a ping to the server which replies with a pong """
        self.ext_interface.send_ping()

    def do_get_real_time_clock(self, line):
        """ Gets the remote computer clock"""
        self.ext_interface.get_real_time_clock()

    # Get version
    def do_get_rpc_version(self, line):
        """ Gets the version of the SEP JSON-RPC interface"""
        self.ext_interface.get_rpc_version()

    # Get product name
    def do_get_product_name(self, line):
        """ Returns the product name """
        self.ext_interface.get_product_name()

    # Get product version
    def do_get_product_version(self, line):
        """ Returns the product version """
        self.ext_interface.get_product_version()

    # Get camera type
    def do_get_camera_type(self, line):
        """ Returns the live camera type """
        self.ext_interface.get_camera_type()

    def do_get_firmware_versions(self, line):
        """ Returns the firmware versions of the connected cameras"""
        self.ext_interface.get_firmware_versions()

    def do_get_illumination_mode(self, line):
        """ Returns the illumination mode of the system"""
        self.ext_interface.get_illumination_mode()

    def do_set_illumination_mode(self, line):
        """ Sets the illumination mode of the system"""
        if line:
            try:
                mode = int(line)
                self.ext_interface.set_illumination_mode(mode)
            except ValueError:
                print("Invalid illumination mode - Must be an integer value")
        else:
            print("Usage: set_illumination_mode mode")

    # Tracker States
    def do_get_state(self, line):
        """ Gets the SEP state """
        self.ext_interface.get_state()

    # Tracking
    def do_start_tracking(self, line):
        """ Start tracking mode"""
        self.ext_interface.start_tracking()

    def do_stop_tracking(self, line):
        """ Stop tracking mode"""
        self.ext_interface.stop_tracking()

    # Logging
    def do_set_log_specification(self, line):
        """ Sets the output data specification for text logging
        (Defaults to log everything if left empty)"""
        if line:
            self.ext_interface.set_log_specification(line)
        else:
            self.ext_interface.set_log_specification("")

    def do_set_log_file(self, line):
        """ Sets the file path of the output log file"""
        if line:
            self.ext_interface.set_log_file(line)
        else:
            print("Usage: set_log_file filename")

    def do_start_log(self, line):
        """ Starts logging a text log.
        Note! This command assumes that the log path has already been set by
        the command set_log_file
        """
        self.ext_interface.start_log()

    def do_stop_log(self, line):
        """ Stops logging the active text log"""
        self.ext_interface.stop_log()

    # Recording
    def do_set_recording_file(self, line):
        """ Sets the output recording file path"""
        if line:
            self.ext_interface.set_recording_file(line)
        else:
            print("Usage: set_recording_file filename")

    def do_start_recording(self, line):
        """" Starts recording a movie.
        NOTE! This command assumes that the recording file path has already
        been set by the command set_recording_file
        """
        if line:
            # Optional compression parameter
            self.ext_interface.start_recording(line)
        else:
            self.ext_interface.start_recording()

    def do_stop_recording(self, line):
        """" Stops recording a movie"""
        self.ext_interface.stop_recording()

    def do_get_recording_state(self, line):
        """ Get recording state to see if SEP is recording or not """
        self.ext_interface.get_recording_state()

    # Subject Category
    def do_get_subject_category(self, line):
        """Returns the current subject category."""
        self.ext_interface.get_subject_category()

    def do_set_subject_category(self, line):
        """Sets the subject category."""
        if line:
            try:
                subjectCategory = int(line)
                self.ext_interface.set_subject_category(subjectCategory)
            except ValueError:
                print("Invalid subjectCategory - Must be an integer value")
        else:
            print("Usage: set_subject_category subjectCategory")

    # Image source
    def do_set_image_source_cameras(self, line):
        """ Sets the image source to live cameras """
        self.ext_interface.set_image_source_cameras()

    def do_set_image_source_recording(self, line):
        """ Sets the image source to recording """
        if line:
            self.ext_interface.set_image_source_recording(line)
        else:
            print("Usage: set_image_source_recording filename")

    # Profile
    def do_clear_profile(self, line):
        """ Clears the current profile"""
        self.ext_interface.clear_profile()

    def do_save_profile(self, line):
        """ Saves a Profile to the specified path"""
        if line:
            self.ext_interface.save_profile(line)
        else:
            print("Usage: save_profile filename")

    def do_load_profile(self, line):
        """ Load a Profile with the specified path"""
        if line:
            self.ext_interface.load_profile(line)
        else:
            print("Usage: load_profile filename")

    def do_get_profile(self, line):
        """ Returns profile data"""
        self.ext_interface.get_profile()

    def do_set_profile(self, line):
        """ Set profile with provided data"""
        if line:
            # This will replace double \\ with single \, as SEP expects
            if "\\n" in line:
                line = line.replace("\\n", "\n")
            self.ext_interface.set_profile(line)
        else:
            print("Usage: set_profile profile_data")

    def do_get_active_eyes(self, line):
        """ Gets the active eyes set in profile"""
        self.ext_interface.get_active_eyes()

    def do_set_active_eyes(self, line):
        """ Set active eyes in profile"""
        args = line.split(' ')
        if len(args) > 1:
            left = args[0].lower() == "true"
            right = args[1].lower() == "true"
            self.ext_interface.set_active_eyes(left, right)
        else:
            print("Usage: set_active_eyes left right")

    # World model
    def do_load_world_model(self, line):
        """Loads a World Model with the specified path"""
        if line:
            self.ext_interface.load_world_model(line)
        else:
            print("Usage: load_world_model filePath")

    def do_load_default_world_model(self, line):
        """Loads the default world model"""
        self.ext_interface.load_default_world_model()

    def do_get_world_model(self, line):
        """ Gets the World Model currently loaded in SEP"""
        self.ext_interface.get_world_model()

    def do_set_world_model(self, line):
        """ Sets the World Model in SEP"""
        if line:
            self.ext_interface.set_world_model(line)
        else:
            print("Usage: set_world_model worldModelObjectString")

    # Communication UDP/TCP
    def do_open_data_stream_udp(self, line):
        """ Orders SEP to open up a UDP data stream
        NOTE: If IP is left empty it defaults to connections IP
        NOTE: If LOG_SPEC is left empty it defaults to full specification
        """
        args = line.split(' ')
        try:
            if len(args) > 2:
                self.ext_interface.open_data_stream_udp(
                    [args[0], int(args[1]), args[2]])
            elif len(args) > 1:
                try:  # Try to see if IP + PORT was provided
                    self.ext_interface.open_data_stream_udp(
                        [args[0], int(args[1])])
                except ValueError:  # Otherwise it is PORT + Log_spec
                    self.ext_interface.open_data_stream_udp(
                        ["", int(args[0]), args[1]])
            elif line:
                self.ext_interface.open_data_stream_udp(["", int(line)])
            else:
                print("Usage: open_data_stream_udp IP PORT LOG_SPEC")
        except ValueError:
            print("Invalid PORT - Must be an integer value")

    def do_close_data_stream_udp(self, line):
        """ Orders SEP to close a specific UDP data stream
        NOTE: If IP is left empty it defaults to connections IP
        """
        args = line.split(' ')
        try:  # Cast to int will cause ValueError when unable to cast
            if len(args) > 1:
                self.ext_interface.close_data_stream_udp(
                    [args[0], int(args[1])])
            elif line:
                self.ext_interface.close_data_stream_udp(["", int(line)])
            else:
                print("Usage: close_data_stream_udp IP PORT")
        except ValueError:
            print("Invalid PORT - Must be an integer value")

    def do_open_data_stream_tcp(self, line):
        """ Orders SEP to open up a TCP data stream
        NOTE: If LOG_SPEC is left empty it defaults to full specification
        """
        args = line.split(' ')
        try:  # Cast to int will cause ValueError when unable to cast
            if len(args) > 1:
                self.ext_interface.open_data_stream_tcp(
                    [int(args[0]), args[1]])
            elif line:
                self.ext_interface.open_data_stream_tcp([int(line)])
            else:
                print("Usage: open_data_stream_tcp PORT LOG_SPEC")
        except ValueError:
            print("Invalid PORT - Must be an integer value")

    def do_close_data_stream_tcp(self, line):
        """ Orders SEP to close a specific TCP data stream"""
        try:  # Cast to int will cause ValueError when unable to cast
            if line:
                self.ext_interface.close_data_stream_tcp(int(line))
            else:
                print("Usage: close_data_stream_tcp PORT")
        except ValueError:
            print("Invalid PORT - Must be an integer value")

    # Gaze callibration
    def do_start_collect_samples_wcs(self, line):
        """ Orders SEP/AS to start collecting points for one 3D-point in
        space given by (x,y,z) position in the World Coordinate System (WCS)
        with specified timeout in ms"""
        args = line.split(' ')
        try:  # Cast to int/float will cause ValueError when unable to cast
            if len(args) > 4:
                self.ext_interface.start_collect_samples_wcs([
                    int(args[0]),
                    float(args[1]),
                    float(args[2]),
                    float(args[3]),
                    int(args[4])
                ])
            else:
                print(
                    "Usage: start_collect_samples_wcs targetId x y z timeout")
        except ValueError:
            print("Invalid input - Must be numerical value")

    def do_start_collect_samples_by_target_name(self, line):
        """ Orders SEP to start collecting points for a target point with a
        specific name that is also specified in the loaded World Model with
        specified timeout in ms"""
        args = line.split(' ')
        try:  # Cast to int/float will cause ValueError when unable to cast
            if len(args) > 2:
                self.ext_interface.start_collect_samples_by_target_name(
                    [int(args[0]), args[1],
                     int(args[2])])
            else:
                print(
                    "Usage: start_collect_camples_by_target_name targetId targetName timeout"
                )
        except ValueError:
            print("Invalid input - Must be numerical value")

    def do_start_collect_samples_object(self, line):
        """  Orders SEP/AS to start collecting points for a target point
        on the surface of a named object in the World Mode with specified
        timeout in ms"""
        args = line.split(' ')
        try:  # Cast to int/float will cause ValueError when unable to cast
            if len(args) > 5:
                self.ext_interface.start_collect_samples_object([
                    int(args[0]), args[1],
                    float(args[2]),
                    float(args[3]),
                    float(args[4]),
                    int(args[5])
                ])
            else:
                print(
                    "Usage: do_start_collect_samples_object targetId objectName x y z timeout"
                )
        except ValueError:
            print("Invalid input - Must be numerical value")

    def do_stop_collect_samples(self, line):
        """ Stops the samples collection. Useful when you want to stop
        collecting points before the specified timeout period."""
        self.ext_interface.stop_collect_samples()

    def do_clear_all_target_samples(self, line):
        """ Clears all the samples for all target points"""
        self.ext_interface.clear_all_target_samples()

    def do_clear_target_samples(self, line):
        """ Clears all samples for a single target point"""
        try:  # Cast to int/float will cause ValueError when unable to cast
            if line:
                self.ext_interface.clear_target_samples(int(line))
            else:
                print("Usage: do_clear_target_samples targetId")
        except ValueError:
            print("Invalid targetId - Must be integer value")

    def do_retrieve_target_statistics(self, line):
        """ Retrieves statistics for a single target. It is assumed that
        a sample collection has been performed on that target before retrieving
        the data.
        """
        try:  # Cast to int will cause ValueError when unable to cast
            if line:
                self.ext_interface.retrieve_target_statistics(int(line))
            else:
                print("Usage: do_retrieve_target_statistics targetId")
        except ValueError:
            print("Invalid targetId - Must be integer value")

    def do_calibrate_gaze(self, line):
        """ Performs gaze calibration calculations based upon the currently
        collected samples for all target points"""
        self.ext_interface.calibrate_gaze()

    def do_apply_gaze_calibration(self, line):
        """ Applies the calculated gaze calibration.
        The calibration will not be used until this method is called"""
        self.ext_interface.apply_gaze_calibration()

    def do_clear_gaze_calibration(self, line):
        """ Clears the current gaze calibration"""
        self.ext_interface.clear_gaze_calibration()

    # Application control
    def do_shut_down(self, line):
        """ Shuts SEP down"""
        self.ext_interface.shut_down()

    def do_key_down(self, line):
        """ Simulates pushing a key on the keyboard. It will continue to be
        pushed down until the key_up command is called"""
        if line:
            self.ext_interface.key_down(line)
        else:
            print("Usage: key_down key")

    def do_key_up(self, line):
        """ Simulates releasing a key on the keyboard"""
        if line:
            self.ext_interface.key_up(line)
        else:
            print("Usage: key_up key")

    # Notifications
    def do_subscribe_to_notification(self, line):
        """ Subscribes to a certain notification message. SEP/AS acts as a
        notification server"""
        if line:
            self.ext_interface.subscribe_to_notification(line)
        else:
            print("Usage: subscribe_to_notification notificationName")

    def do_unsubscribe_to_notification(self, line):
        """ Unsubscribes to a certain notification message"""
        if line:
            self.ext_interface.unsubscribe_to_notification(line)
        else:
            print("Usage: unsubscribe_to_notification notificationName")

    def do_send_notification(self, line):
        """ Sends a notification message to the server SEP.
        The server will then forward the notification message to all clients
        subscribing to the specific notification name. """
        args = line.split(' ')
        if line:
            self.ext_interface.send_notification(args)
        else:
            print(
                "Usage: send_notification notificationName optionalParameters")

    def do_prompt(self, line):
        """ Change the interactive prompt """
        self.prompt = line + ': '

    # Disabling these two lint warnings, exit can't be static and
    # need to take line as argument.
    def do_exit(self, line):  #pylint: disable=R0201,W0613
        """ Exit the command line"""
        # Clear notification subscriptions
        self.ext_interface.subscriptions = []
        return True

    # Calibration
    def do_retrieve_calibration_results(self, line):
        """ Retrieve calibration results"""
        self.ext_interface.retrieve_calibration_results()

    # Playback
    def do_set_playback_speed_to_max(self, line):
        """ Set playback speed to max """
        self.ext_interface.set_playback_speed_to_max()

    def do_set_playback_speed_to_real(self, line):
        """ Set playback speed to real time"""
        self.ext_interface.set_playback_speed_to_real_time()

    def do_set_playback_position(self, line):
        """ Set which frame the recording should play from"""
        try:  # Cast to int/float will cause ValueError when unable to cast
            if line:
                self.ext_interface.set_playback_position(int(line))
            else:
                print("Usage: set_playback_position position")
        except ValueError:
            print("Invalid input - Must be numerical value")

    def do_set_playback_start_stop_positions(self, line):
        """ Set which frames the recording should start and stop at"""
        args = line.split(' ')
        try:  # Cast to int/float will cause ValueError when unable to cast
            if len(args) > 1:
                self.ext_interface.set_playback_start_stop_positions(
                    [int(args[0]), int(args[1])])
            else:
                print(
                    "Usage: set_playback_start_stop_positions startPosition stopPosition"
                )
        except ValueError:
            print("Invalid input - Must be numerical value")

    def do_resume_playback(self, line):
        """ Resume Playback"""
        self.ext_interface.resume_playback()

    def do_pause_playback(self, line):
        """ Pause playback"""
        self.ext_interface.pause_playback()

    def do_set_playback_repeat_on(self, line):
        """ Set playback repeat on"""
        self.ext_interface.set_playback_repeat_on()

    def do_set_playback_repeat_off(self, line):
        """ Set playback repeat off"""
        self.ext_interface.set_playback_repeat_off()

    # Collect Point Samples
    def do_start_collect_point_samples_auto(self, line):
        """ Start collect point samples"""
        self.ext_interface.start_collect_point_samples_automatic()

    def do_stop_collect_point_samples_auto(self, line):
        """ Stop collect point samples"""
        self.ext_interface.stop_collect_point_samples_automatic()

    # Camera Image
    def do_get_camera_image(self, line):
        """ Get camera image"""
        args = line.split(' ')
        try:  # Cast to int/float will cause ValueError when unable to cast
            if len(args) > 1:
                self.ext_interface.get_camera_image(
                    [int(args[0]), float(args[1])])
            else:
                print("Usage: get_camera_image cameraIndex scale")
        except ValueError:
            print("Invalid input - Must be numerical value")

    # Chessboard Tracking
    def do_start_chessboard_tracking(self, line):
        """ Start chessboard tracking"""
        self.ext_interface.start_chessboard_tracking()

    def do_stop_chessboard_tracking(self, line):
        """ Stop chessboard tracking"""
        self.ext_interface.stop_chessboard_tracking()

    # Usb speed
    def do_is_camera_connected_to_usb3(self, line):
        """ Check if camera is connected to USB3 """
        try:  # Cast to int/float will cause ValueError when unable to cast
            if line:
                self.ext_interface.is_camera_connected_to_usb3(int(line))
            else:
                print("Usage: is_camera_connected_to_usb3 cameraId")
        except ValueError:
            print("Invalid input - Must be numerical value")

    #Reflex Reduction
    def do_set_reflex_reduction_mode(self, line):
        """ Set reflex reduction mode"""
        try:  # Cast to int/float will cause ValueError when unable to cast
            if line:
                self.ext_interface.set_reflex_reduction_mode(int(line))
            else:
                print("Usage: set_reflex_reduction_mode mode")
        except ValueError:
            print("Invalid input - Must be numerical value")


if __name__ == "__main__":

    ExternalInterfacesCommands().cmdloop()
