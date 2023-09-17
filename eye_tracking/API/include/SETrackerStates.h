// Copyright (C) Smart Eye AB 2002-2023
// THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
// ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
// THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
// OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
// OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
//----------------------------------------------------------------------------//
// Smart Eye AB
// Första långgatan 28 B,
// 413 27 Göteborg, Sweden
// Contact: support@smarteye.se
//
// You are free to modify and use this code together with
// your purchased Smart Eye system.
//
// You MAY NOT distribute this code (modified or unmodified)
// without prior written consent from Smart Eye AB.
//----------------------------------------------------------------------------//

#if !defined(SE_TRACKING_STATES_INCLUDED_)
#define SE_TRACKING_STATES_INCLUDED_

#ifdef __cplusplus
namespace se {
namespace states {
#endif

typedef enum {
  Idling                  = 0x0000, // The system is idle, ready to go into any other state.
  Tracking                = 0x0010, // The system is tracking
  ChessboardTracker       = 0x0015, // The system is currently tracking a chessboard
  CalibratingCameras      = 0x0020, // The system is currently performing camera calibration
  VerifyingCalibration    = 0x0021, // The system is verifying the camera calibration
  CheckingFocus           = 0x0030, // The system is adjusting focus and aperture
  DefiningWCS             = 0x0040, // The system is performing manual WCS definition
  DefiningAutomaticWCS    = 0x0041, // The system is in an defining WCS automatically using a chessboard
  DefiningCameraTiedWCS   = 0x0042, // The system is defining wcs manually, but using cameras for position and rotation
  GazeCalibrating         = 0x0050, // The system is performing gaze calibration
  GazeVerifying           = 0x0051, // The system is verifying gaze calibration
  RecordingProfile        = 0x0060, // The system is collecting snapshots for manual profile creation
  PlacingMarkers          = 0x0061, // The system is placing markers in manual profile creation
  ProfileSelectingPoses   = 0x0062, // The system is selecting/reviewing/removing poses in manual profile creation
  ProfileReselectingPoses = 0x0063, // The system is reselecting poses in manual profile creation
  RecordingToFile         = 0x0070, // [OBSOLETE] The system is recording to disk
  ScriptedRecordingToFile = 0x0071, // [OBSOLETE] The system is recording to disk (without open UI dialog)
  DefiningExpectedPose    = 0x0080, // The system is defining expected pose
  WorldMeasurement        = 0x0090, // [OBSOLETE] The system is measuring/building a world model
  AutoDetectLens          = 0x00A0, // The system is detecting lenses
} TrackerState;

typedef enum {
  NotRecording = 0x1000, // The system is not currently recording.
  Recording    = 0x1010, // The system is currently recording.
} RecordState;

#ifdef __cplusplus
} // namespace states
} // namespace se
#endif

#endif // SE_TRACKING_STATES_INCLUDED_
