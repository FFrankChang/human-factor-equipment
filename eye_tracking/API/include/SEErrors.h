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


#if !defined(SE_ERROR__INCLUDED_)
#define SE_ERROR__INCLUDED_

#ifdef __cplusplus
namespace se {
namespace errors {
#endif

typedef enum {

  // 0x0000.. Success
  Success                                             = 0x00000000,

  // 0xffff.. Undefined
  UndefinedError                                      = 0xffffffff,

  // 0xffff.. JsonRpc
  JsonRpcDefaultError                                 = 0xffff8300,
  JsonRpcParsingError                                 = 0xffff8044,
  JsonRpcInvalidRequest                               = 0xffff80a8,
  JsonRpcMethodNotFound                               = 0xffff80a7,
  JsonRpcInvalidParams                                = 0xffff80a6,
  JsonRpcInternalError                                = 0xffff80a5,
  JsonRpcCallFailed                                   = 0xffff82ff,
  JsonRpcWrongVersion                                 = 0xffff82fe,
  JsonRpcServerNotInitialized                         = 0xffff82fd,
  JsonRpcTooFewParams                                 = 0xffff82fc,

  // 0x0000.. System
  SystemDefaultError                                  = 0x00002000,
  SystemBusy                                          = 0x00002001,
  SystemNotImplemented                                = 0x00002002,
  SystemNotInTrackingState                            = 0x00002003,
  SystemNotInIdleState                                = 0x00002004,
  SystemOperationTimeout                              = 0x00002005,

  // 0x0000.. GazeCalibration
  GazeCalibrationDefaultError                         = 0x00003000,
  GazeCalibrationNotInitialized                       = 0x00003001,
  GazeCalibrationCollecting                           = 0x00003002,
  GazeCalibrationCalibrationPointNotFoundInWorldModel = 0x00003003,
  GazeCalibrationCollectionDoesNotExist               = 0x00003004,
  GazeCalibrationCollectingAutomatic                  = 0x00003005,
  GazeCalibrationNotEnoughCalibrationData             = 0x00003011,
  GazeCalibrationNoFixationInCollection               = 0x00003012,
  GazeCalibrationCalibrationCouldNotBeSolved          = 0x00003013,
  GazeCalibrationCanceled                             = 0x00003014,
  GazeCalibrationCalibrationError                     = 0x00003015,

  // 0x0000.. Logging
  LoggingDefaultError                                 = 0x00004000,
  LoggingSetFileNotFound                              = 0x00004001,
  LoggingSetFileEmpty                                 = 0x00004002,
  LoggingSetSpecificationNoLogFound                   = 0x00004003,
  LoggingStartNoLogfileDefined                        = 0x00004021,
  LoggingStopNotStarted                               = 0x00004041,
  LoggingDirectoryNotValid                            = 0x00004042,
  LoggingStartLogInProgress                           = 0x00004043,

  // 0x0000.. Profile
  ProfileDefaultError                                 = 0x00005000,
  ProfileLoadFileNotFound                             = 0x00005001,
  ProfileSaveEmptyFilename                            = 0x00005002,
  ProfileFailedToReadFile                             = 0x00005003,
  ProfileOnlyGazeCalibration                          = 0x00005004,
  ProfileFailedToWriteFile                            = 0x00005005,
  ProfileLoadTracking                                 = 0x00005006,
  ProfileDirectoryNotValid                            = 0x00005007,
  ProfileRefinderMissing                              = 0x00005008,
  ProfileAlreadyInitialized                           = 0x00005009,
  ProfileFailedToParse                                = 0x00005010,
  ProfileTrackingTypeNotSupported                     = 0x00005011,

  // 0x0000.. Tracking
  TrackingDefaultError                                = 0x00006000,
  TrackingStartFailed                                 = 0x00006001,
  TrackingStopFailed                                  = 0x00006021,
  TrackingStartAlreadyTracking                        = 0x00006022,
  TrackingStopNoOngoingTracking                       = 0x00006023,

  // 0x0000.. ImageSource
  ImageSourceDefaultError                             = 0x00007000,
  ImageSourceSetRecordingFailed                       = 0x00007001,
  ImageSourceSetCamerasFailed                         = 0x00007002,
  ImageSourceGetCameraImageIndexOutOfBounds           = 0x00007003,
  ImageSourceSetFileEmpty                             = 0x00007004,
  ImageSourceCamerasNotAvailable                      = 0x00007005,
  ImageSourceSetRecordingCouldNotFindRecording        = 0x00007006,

  // 0x0000.. Recording
  RecordingDefaultError                               = 0x00008000,
  RecordingSetFileFailed                              = 0x00008001,
  RecordingStartNoFileSet                             = 0x00008002,
  RecordingStartAlreadyRecording                      = 0x00008003,
  RecordingStopNotRecording                           = 0x00008004,
  RecordingDirectoryNotValid                          = 0x00008005,
  RecordingNotSupported                               = 0x00008006,
  RecordingUnknownCompressionType                     = 0x00008007,
  RecordingFileSizeLimitReached                       = 0x00008008,
  RecordingNotSupportedByLicense                      = 0x00008009,
  RecordingInvalidSetup                               = 0x0000800a,

  // 0x0000.. DataStream
  DataStreamDefaultError                              = 0x0000a000,
  DataStreamUDPOpenFailed                             = 0x0000a001,
  DataStreamUDPCloseFailed                            = 0x0000a002,
  DataStreamTCPOpenFailed                             = 0x0000a003,
  DataStreamTCPCloseFailed                            = 0x0000a004,
  DataStreamTCPAlreadyOpen                            = 0x0000a005,
  DataStreamTCPDoesNotExist                           = 0x0000a006,
  DataStreamUDPAlreadyOpen                            = 0x0000a007,
  DataStreamUDPDoesNotExist                           = 0x0000a008,

  // 0x0000.. WorldModel
  WorldModelDefaultError                              = 0x0000b000,
  WorldModelGetFailed                                 = 0x0000b001,
  WorldModelSetFailed                                 = 0x0000b002,
  WorldModelLoadFailed                                = 0x0000b003,
  WorldModelInvalid                                   = 0x0000b004,

  // 0x0000.. Chessboard
  ChessboardDefaultError                              = 0x0000c000,
  ChessboardNoLicense                                 = 0x0000c001,
  ChessboardTrackingNotActive                         = 0x0000c002,

  // 0x0000.. Key
  KeyDefaultError                                     = 0x0000e000,
  KeyAlreadyReleased                                  = 0x0000e001,
  KeyAlreadyPressed                                   = 0x0000e002,

  // 0x0000.. Playback
  PlaybackDefaultError                                = 0x0000f000,
  PlaybackPauseFailed                                 = 0x0000f001,
  PlaybackResumeFailed                                = 0x0000f002,
  PlaybackSetPositionFailed                           = 0x0000f003,
  PlaybackSetStartStopPositionFailed                  = 0x0000f004,

  // 0x0001.. Notification
  NotificationDefaultError                            = 0x00010000,
  NotificationSubscribeAlreadySubscribing             = 0x00010001,
  NotificationUnsubscribeNotSubscribing               = 0x00010002,

  // 0x0003.. Usb
  UsbSpeedInvalidCameraType                           = 0x00030000,
  UsbSpeedInvalidCameraId                             = 0x00030001,
  UsbTypeNotSupported                                 = 0x00030002,
  UsbCameraFirmwareNotSupported                       = 0x00030003,
  UsbCameraFirmwareVersionNotAvailable                = 0x00030004,

  // 0x0004.. UserMarker
  UserMarkerDefaultError                              = 0x00040000,
  UserMarkerInvalidTimestamp                          = 0x00040001,
  UserMarkerDataOutOfRange                            = 0x00040002,
  UserMarker2PositiveEdgeInRow                        = 0x00040003,
  UserMarker2NegativeEdgeInRow                        = 0x00040004,
  UserMarkerFirmwareNotSupported                      = 0x00040005,
  UserMarkerMissedEdgeDetected                        = 0x00040006,

  // 0x0005.. ReflexReduction
  ReflexReductionSetFailed                            = 0x00050000,
  ReflexReductionNotSupported                         = 0x00050001,

  // 0x0006.. HeadTracking
  HeadTrackingSetFailed                               = 0x00060000,

  // 0x0007.. SubjectCategory
  SubjectCategoryNotSupportedByLicense                = 0x00070000,

  // 0x0008.. IlluminationMode
  IlluminationModeNotSupported                        = 0x00080000

} SEErrorId;

#ifdef __cplusplus
} // namespace errors
} // namespace se
#endif

#endif //  SE_ERROR__INCLUDED_