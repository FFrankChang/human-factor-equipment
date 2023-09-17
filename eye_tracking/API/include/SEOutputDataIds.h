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


#pragma once

#include "SEDataTypes.h"
#include "SEOutputData.h"

using namespace output;

static SEOutputData OutputDataList[] = {

  //Frame Information
    {SEFrameNumber, "FrameNumber", SEType_u32},
    {SEEstimatedDelay, "EstimatedDelay", SEType_u32},
    {SETimeStamp, "TimeStamp", SEType_u64},
    {SEUserTimeStamp, "UserTimeStamp", SEType_u64},
    {SEFrameRate, "FrameRate", SEType_f64},
    {SECameraPositions, "CameraPositions", SEType_Vector},
    {SECameraRotations, "CameraRotations", SEType_Vector},
    {SEUserDefinedData, "UserDefinedData", SEType_u64},
    {SERealTimeClock, "RealTimeClock", SEType_u64},
    {SEKeyboardState, "KeyboardState", SEType_String},
    {SEASCIIKeyboardState, "ASCIIKeyboardState", SEType_u16},
    {SEUserMarker, "UserMarker", SEType_UserMarker},
    {SECameraClocks, "CameraClocks", SEType_Vector},

  //Head Position
    {SEHeadPosition, "HeadPosition", SEType_Point3D},
    {SEHeadPositionQ, "HeadPositionQ", SEType_f64},
    {SEHeadRotationRodrigues, "HeadRotationRodrigues", SEType_Vect3D},
    {SEHeadRotationQuaternion, "HeadRotationQuaternion", SEType_Quaternion},
    {SEHeadLeftEarDirection, "HeadLeftEarDirection", SEType_Vect3D},
    {SEHeadUpDirection, "HeadUpDirection", SEType_Vect3D},
    {SEHeadNoseDirection, "HeadNoseDirection", SEType_Vect3D},
    {SEHeadHeading, "HeadHeading", SEType_f64},
    {SEHeadPitch, "HeadPitch", SEType_f64},
    {SEHeadRoll, "HeadRoll", SEType_f64},
    {SEHeadRotationQ, "HeadRotationQ", SEType_f64},

  //Raw Gaze
    {SEGazeOrigin, "GazeOrigin", SEType_Point3D},
    {SELeftGazeOrigin, "LeftGazeOrigin", SEType_Point3D},
    {SERightGazeOrigin, "RightGazeOrigin", SEType_Point3D},
    {SEEyePosition, "EyePosition", SEType_Point3D},
    {SEGazeDirection, "GazeDirection", SEType_Vect3D},
    {SEGazeDirectionQ, "GazeDirectionQ", SEType_f64},
    {SELeftEyePosition, "LeftEyePosition", SEType_Point3D},
    {SELeftGazeDirection, "LeftGazeDirection", SEType_Vect3D},
    {SELeftGazeDirectionQ, "LeftGazeDirectionQ", SEType_f64},
    {SERightEyePosition, "RightEyePosition", SEType_Point3D},
    {SERightGazeDirection, "RightGazeDirection", SEType_Vect3D},
    {SERightGazeDirectionQ, "RightGazeDirectionQ", SEType_f64},
    {SEGazeHeading, "GazeHeading", SEType_f64},
    {SEGazePitch, "GazePitch", SEType_f64},
    {SELeftGazeHeading, "LeftGazeHeading", SEType_f64},
    {SELeftGazePitch, "LeftGazePitch", SEType_f64},
    {SERightGazeHeading, "RightGazeHeading", SEType_f64},
    {SERightGazePitch, "RightGazePitch", SEType_f64},

  //Filtered Gaze
    {SEFilteredGazeDirection, "FilteredGazeDirection", SEType_Vect3D},
    {SEFilteredGazeDirectionQ, "FilteredGazeDirectionQ", SEType_f64},
    {SEFilteredLeftGazeDirection, "FilteredLeftGazeDirection", SEType_Vect3D},
    {SEFilteredLeftGazeDirectionQ, "FilteredLeftGazeDirectionQ", SEType_f64},
    {SEFilteredRightGazeDirection, "FilteredRightGazeDirection", SEType_Vect3D},
    {SEFilteredRightGazeDirectionQ, "FilteredRightGazeDirectionQ", SEType_f64},
    {SEFilteredGazeHeading, "FilteredGazeHeading", SEType_f64},
    {SEFilteredGazePitch, "FilteredGazePitch", SEType_f64},
    {SEFilteredLeftGazeHeading, "FilteredLeftGazeHeading", SEType_f64},
    {SEFilteredLeftGazePitch, "FilteredLeftGazePitch", SEType_f64},
    {SEFilteredRightGazeHeading, "FilteredRightGazeHeading", SEType_f64},
    {SEFilteredRightGazePitch, "FilteredRightGazePitch", SEType_f64},

  //Analysis (non-real-time)
    {SESaccade, "Saccade", SEType_u32},
    {SEFixation, "Fixation", SEType_u32},
    {SEBlink, "Blink", SEType_u32},
    {SELeftBlinkClosingMidTime, "LeftBlinkClosingMidTime", SEType_u64},
    {SELeftBlinkOpeningMidTime, "LeftBlinkOpeningMidTime", SEType_u64},
    {SELeftBlinkClosingAmplitude, "LeftBlinkClosingAmplitude", SEType_f64},
    {SELeftBlinkOpeningAmplitude, "LeftBlinkOpeningAmplitude", SEType_f64},
    {SELeftBlinkClosingSpeed, "LeftBlinkClosingSpeed", SEType_f64},
    {SELeftBlinkOpeningSpeed, "LeftBlinkOpeningSpeed", SEType_f64},
    {SERightBlinkClosingMidTime, "RightBlinkClosingMidTime", SEType_u64},
    {SERightBlinkOpeningMidTime, "RightBlinkOpeningMidTime", SEType_u64},
    {SERightBlinkClosingAmplitude, "RightBlinkClosingAmplitude", SEType_f64},
    {SERightBlinkOpeningAmplitude, "RightBlinkOpeningAmplitude", SEType_f64},
    {SERightBlinkClosingSpeed, "RightBlinkClosingSpeed", SEType_f64},
    {SERightBlinkOpeningSpeed, "RightBlinkOpeningSpeed", SEType_f64},

  //Intersections
    {SEClosestWorldIntersection, "ClosestWorldIntersection", SEType_WorldIntersection},
    {SEFilteredClosestWorldIntersection, "FilteredClosestWorldIntersection", SEType_WorldIntersection},
    {SEAllWorldIntersections, "AllWorldIntersections", SEType_WorldIntersections},
    {SEFilteredAllWorldIntersections, "FilteredAllWorldIntersections", SEType_WorldIntersections},
    {SEZoneId, "NumericalClosestWorldIntersection", SEType_u16},
    {SEEstimatedClosestWorldIntersection, "EstimatedClosestWorldIntersection", SEType_WorldIntersection},
    {SEEstimatedAllWorldIntersections, "EstimatedAllWorldIntersections", SEType_WorldIntersections},
    {SEHeadClosestWorldIntersection, "HeadClosestWorldIntersection", SEType_WorldIntersection},
    {SEHeadAllWorldIntersections, "HeadAllWorldIntersections", SEType_WorldIntersections},
    {SECalibrationGazeIntersection, "CalibrationGazeIntersection", SEType_WorldIntersection},
    {SETaggedGazeIntersection, "TaggedGazeIntersection", SEType_WorldIntersection},
    {SELeftClosestWorldIntersection, "LeftClosestWorldIntersection", SEType_WorldIntersection},
    {SELeftAllWorldIntersections, "LeftAllWorldIntersections", SEType_WorldIntersections},
    {SERightClosestWorldIntersection, "RightClosestWorldIntersection", SEType_WorldIntersection},
    {SERightAllWorldIntersections, "RightAllWorldIntersections", SEType_WorldIntersections},
    {SEFilteredLeftClosestWorldIntersection, "FilteredLeftClosestWorldIntersection", SEType_WorldIntersection},
    {SEFilteredLeftAllWorldIntersections, "FilteredLeftAllWorldIntersections", SEType_WorldIntersections},
    {SEFilteredRightClosestWorldIntersection, "FilteredRightClosestWorldIntersection", SEType_WorldIntersection},
    {SEFilteredRightAllWorldIntersections, "FilteredRightAllWorldIntersections", SEType_WorldIntersections},
    {SEEstimatedLeftClosestWorldIntersection, "EstimatedLeftClosestWorldIntersection", SEType_WorldIntersection},
    {SEEstimatedLeftAllWorldIntersections, "EstimatedLeftAllWorldIntersections", SEType_WorldIntersections},
    {SEEstimatedRightClosestWorldIntersection, "EstimatedRightClosestWorldIntersection", SEType_WorldIntersection},
    {SEEstimatedRightAllWorldIntersections, "EstimatedRightAllWorldIntersections", SEType_WorldIntersections},
    {SEFilteredEstimatedClosestWorldIntersection, "FilteredEstimatedClosestWorldIntersection", SEType_WorldIntersection},
    {SEFilteredEstimatedAllWorldIntersections, "FilteredEstimatedAllWorldIntersections", SEType_WorldIntersections},
    {SEFilteredEstimatedLeftClosestWorldIntersection, "FilteredEstimatedLeftClosestWorldIntersection", SEType_WorldIntersection},
    {SEFilteredEstimatedLeftAllWorldIntersections, "FilteredEstimatedLeftAllWorldIntersections", SEType_WorldIntersections},
    {SEFilteredEstimatedRightClosestWorldIntersection, "FilteredEstimatedRightClosestWorldIntersection", SEType_WorldIntersection},
    {SEFilteredEstimatedRightAllWorldIntersections, "FilteredEstimatedRightAllWorldIntersections", SEType_WorldIntersections},

  //Eyelid
    {SEEyelidOpening, "EyelidOpening", SEType_f64},
    {SEEyelidOpeningQ, "EyelidOpeningQ", SEType_f64},
    {SELeftEyelidOpening, "LeftEyelidOpening", SEType_f64},
    {SELeftEyelidOpeningQ, "LeftEyelidOpeningQ", SEType_f64},
    {SERightEyelidOpening, "RightEyelidOpening", SEType_f64},
    {SERightEyelidOpeningQ, "RightEyelidOpeningQ", SEType_f64},
    {SELeftLowerEyelidExtremePointDEPRECATED, "LeftLowerEyelidExtremePoint", SEType_Point3D},
    {SELeftUpperEyelidExtremePointDEPRECATED, "LeftUpperEyelidExtremePoint", SEType_Point3D},
    {SERightLowerEyelidExtremePointDEPRECATED, "RightLowerEyelidExtremePoint", SEType_Point3D},
    {SERightUpperEyelidExtremePointDEPRECATED, "RightUpperEyelidExtremePoint", SEType_Point3D},
    {SELeftEyelidState, "LeftEyelidState", SEType_u8},
    {SERightEyelidState, "RightEyelidState", SEType_u8},

  //Pupilometry
    {SEPupilDiameter, "PupilDiameter", SEType_f64},
    {SEPupilDiameterQ, "PupilDiameterQ", SEType_f64},
    {SELeftPupilDiameter, "LeftPupilDiameter", SEType_f64},
    {SELeftPupilDiameterQ, "LeftPupilDiameterQ", SEType_f64},
    {SERightPupilDiameter, "RightPupilDiameter", SEType_f64},
    {SERightPupilDiameterQ, "RightPupilDiameterQ", SEType_f64},
    {SEFilteredPupilDiameter, "FilteredPupilDiameter", SEType_f64},
    {SEFilteredPupilDiameterQ, "FilteredPupilDiameterQ", SEType_f64},
    {SEFilteredLeftPupilDiameter, "FilteredLeftPupilDiameter", SEType_f64},
    {SEFilteredLeftPupilDiameterQ, "FilteredLeftPupilDiameterQ", SEType_f64},
    {SEFilteredRightPupilDiameter, "FilteredRightPupilDiameter", SEType_f64},
    {SEFilteredRightPupilDiameterQ, "FilteredRightPupilDiameterQ", SEType_f64},

  //GPS Information
    {SEGPSPosition, "GPSPosition", SEType_Point2D},
    {SEGPSGroundSpeed, "GPSGroundSpeed", SEType_f64},
    {SEGPSCourse, "GPSCourse", SEType_f64},
    {SEGPSTime, "GPSTime", SEType_u64},

  //Raw Estimated Gaze
    {SEEstimatedGazeOrigin, "EstimatedGazeOrigin", SEType_Point3D},
    {SEEstimatedLeftGazeOrigin, "EstimatedLeftGazeOrigin", SEType_Point3D},
    {SEEstimatedRightGazeOrigin, "EstimatedRightGazeOrigin", SEType_Point3D},
    {SEEstimatedEyePosition, "EstimatedEyePosition", SEType_Point3D},
    {SEEstimatedGazeDirection, "EstimatedGazeDirection", SEType_Vect3D},
    {SEEstimatedGazeDirectionQ, "EstimatedGazeDirectionQ", SEType_f64},
    {SEEstimatedGazeHeading, "EstimatedGazeHeading", SEType_f64},
    {SEEstimatedGazePitch, "EstimatedGazePitch", SEType_f64},
    {SEEstimatedLeftEyePosition, "EstimatedLeftEyePosition", SEType_Point3D},
    {SEEstimatedLeftGazeDirection, "EstimatedLeftGazeDirection", SEType_Vect3D},
    {SEEstimatedLeftGazeDirectionQ, "EstimatedLeftGazeDirectionQ", SEType_f64},
    {SEEstimatedLeftGazeHeading, "EstimatedLeftGazeHeading", SEType_f64},
    {SEEstimatedLeftGazePitch, "EstimatedLeftGazePitch", SEType_f64},
    {SEEstimatedRightEyePosition, "EstimatedRightEyePosition", SEType_Point3D},
    {SEEstimatedRightGazeDirection, "EstimatedRightGazeDirection", SEType_Vect3D},
    {SEEstimatedRightGazeDirectionQ, "EstimatedRightGazeDirectionQ", SEType_f64},
    {SEEstimatedRightGazeHeading, "EstimatedRightGazeHeading", SEType_f64},
    {SEEstimatedRightGazePitch, "EstimatedRightGazePitch", SEType_f64},

  //Filtered Estimated Gaze
    {SEFilteredEstimatedGazeDirection, "FilteredEstimatedGazeDirection", SEType_Vect3D},
    {SEFilteredEstimatedGazeDirectionQ, "FilteredEstimatedGazeDirectionQ", SEType_f64},
    {SEFilteredEstimatedGazeHeading, "FilteredEstimatedGazeHeading", SEType_f64},
    {SEFilteredEstimatedGazePitch, "FilteredEstimatedGazePitch", SEType_f64},
    {SEFilteredEstimatedLeftGazeDirection, "FilteredEstimatedLeftGazeDirection", SEType_Vect3D},
    {SEFilteredEstimatedLeftGazeDirectionQ, "FilteredEstimatedLeftGazeDirectionQ", SEType_f64},
    {SEFilteredEstimatedLeftGazeHeading, "FilteredEstimatedLeftGazeHeading", SEType_f64},
    {SEFilteredEstimatedLeftGazePitch, "FilteredEstimatedLeftGazePitch", SEType_f64},
    {SEFilteredEstimatedRightGazeDirection, "FilteredEstimatedRightGazeDirection", SEType_Vect3D},
    {SEFilteredEstimatedRightGazeDirectionQ, "FilteredEstimatedRightGazeDirectionQ", SEType_f64},
    {SEFilteredEstimatedRightGazeHeading, "FilteredEstimatedRightGazeHeading", SEType_f64},
    {SEFilteredEstimatedRightGazePitch, "FilteredEstimatedRightGazePitch", SEType_f64},

  //Status
    {SETrackingState, "TrackingState", SEType_u8},
    {SEEyeglassesStatus, "EyeglassesStatus", SEType_u8},
    {SEReflexReductionStateDEPRECATED, "ReflexReductionStateDEPRECATED", SEType_u8},

  //Facial Feature Positions
    {SELeftEyeOuterCorner3D, "LeftEyeOuterCorner3D", SEType_Point3D},
    {SELeftEyeInnerCorner3D, "LeftEyeInnerCorner3D", SEType_Point3D},
    {SERightEyeInnerCorner3D, "RightEyeInnerCorner3D", SEType_Point3D},
    {SERightEyeOuterCorner3D, "RightEyeOuterCorner3D", SEType_Point3D},
    {SELeftNostril3D, "LeftNostril3D", SEType_Point3D},
    {SERightNostril3D, "RightNostril3D", SEType_Point3D},
    {SELeftMouthCorner3D, "LeftMouthCorner3D", SEType_Point3D},
    {SERightMouthCorner3D, "RightMouthCorner3D", SEType_Point3D},
    {SELeftEar3D, "LeftEar3D", SEType_Point3D},
    {SERightEar3D, "RightEar3D", SEType_Point3D},
    {SENoseTip3D, "NoseTip3D", SEType_Point3D},
    {SELeftEyeOuterCorner2D, "LeftEyeOuterCorner2D", SEType_Vector},
    {SELeftEyeInnerCorner2D, "LeftEyeInnerCorner2D", SEType_Vector},
    {SERightEyeInnerCorner2D, "RightEyeInnerCorner2D", SEType_Vector},
    {SERightEyeOuterCorner2D, "RightEyeOuterCorner2D", SEType_Vector},
    {SELeftNostril2D, "LeftNostril2D", SEType_Vector},
    {SERightNostril2D, "RightNostril2D", SEType_Vector},
    {SELeftMouthCorner2D, "LeftMouthCorner2D", SEType_Vector},
    {SERightMouthCorner2D, "RightMouthCorner2D", SEType_Vector},
    {SELeftEar2D, "LeftEar2D", SEType_Vector},
    {SERightEar2D, "RightEar2D", SEType_Vector},
    {SENoseTip2D, "NoseTip2D", SEType_Vector},
    {SEMouthShapePoints2D, "MouthShapePoints2D", SEType_Vector},
    {SELeftEarShapePoints2D, "LeftEarShapePoints2D", SEType_Vector},
    {SERightEarShapePoints2D, "RightEarShapePoints2D", SEType_Vector},
    {SENoseShapePoints2D, "NoseShapePoints2D", SEType_Vector},
    {SELeftEyeShapePoints2D, "LeftEyeShapePoints2D", SEType_Vector},
    {SERightEyeShapePoints2D, "RightEyeShapePoints2D", SEType_Vector},

  //Emotion
    {SEEmotionJoy, "Joy", SEType_f64},
    {SEEmotionFear, "Fear", SEType_f64},
    {SEEmotionDisgust, "Disgust", SEType_f64},
    {SEEmotionSadness, "Sadness", SEType_f64},
    {SEEmotionSurprise, "Surprise", SEType_f64},
    {SEEmotionValence, "Valence", SEType_f64},
    {SEEmotionEngagement, "Engagement", SEType_f64},
    {SEEmotionSentimentality, "Sentimentality", SEType_f64},
    {SEEmotionConfusion, "Confusion", SEType_f64},
    {SEEmotionNeutral, "Neutral", SEType_f64},
    {SEEmotionQ, "EmotionQ", SEType_f64},

  //Expression
    {SEExpressionSmile, "Smile", SEType_f64},
    {SEExpressionInnerBrowRaise, "InnerBrowRaise", SEType_f64},
    {SEExpressionBrowRaise, "BrowRaise", SEType_f64},
    {SEExpressionBrowFurrow, "BrowFurrow", SEType_f64},
    {SEExpressionNoseWrinkle, "NoseWrinkle", SEType_f64},
    {SEExpressionUpperLipRaise, "UpperLipRaise", SEType_f64},
    {SEExpressionLipCornerDepressor, "LipCornerDepressor", SEType_f64},
    {SEExpressionChinRaise, "ChinRaise", SEType_f64},
    {SEExpressionLipPucker, "LipPucker", SEType_f64},
    {SEExpressionLipPress, "LipPress", SEType_f64},
    {SEExpressionLipSuck, "LipSuck", SEType_f64},
    {SEExpressionMouthOpen, "MouthOpen", SEType_f64},
    {SEExpressionSmirk, "Smirk", SEType_f64},
    {SEExpressionAttention, "Attention", SEType_f64},
    {SEExpressionEyeWiden, "EyeWiden", SEType_f64},
    {SEExpressionCheekRaise, "CheekRaise", SEType_f64},
    {SEExpressionLidTighten, "LidTighten", SEType_f64},
    {SEExpressionDimpler, "Dimpler", SEType_f64},
    {SEExpressionLipStretch, "LipStretch", SEType_f64},
    {SEExpressionJawDrop, "JawDrop", SEType_f64},
    {SEExpressionQ, "ExpressionQ", SEType_f64},

  //Activity
    {SESpeaking, "Speaking", SEType_u8},
    {SESpeakingQ, "SpeakingQ", SEType_f64},

    {0, 0, SEType(0)}};
