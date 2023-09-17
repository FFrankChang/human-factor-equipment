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

#if __STDC__ || __cplusplus
    //In c/c++ the namespace and public should not be included
#else
using System;
namespace SE
{
  [Serializable]
  public
    
#endif
    // IMPORTANT NOTE
    // These ids defines the output data from the Smart Eye system
    // Do not alter any of these ids
  enum SEOutputDataIds
  {
    //Frame Information
  SEFrameNumber = 0x0001,
  SEEstimatedDelay = 0x0002,
  SETimeStamp = 0x0003,
  SEUserTimeStamp = 0x0004,
  SEFrameRate = 0x0005,
  SECameraPositions = 0x0006,
  SECameraRotations = 0x0007,
  SEUserDefinedData = 0x0008,
  SERealTimeClock = 0x0009,
  SEKeyboardState = 0x0056,
  SEASCIIKeyboardState = 0x00a4,
  SEUserMarker = 0x03a0,
  SECameraClocks = 0x03a1,

    //Head Position
  SEHeadPosition = 0x0010,
  SEHeadPositionQ = 0x0011,
  SEHeadRotationRodrigues = 0x0012,
  SEHeadRotationQuaternion = 0x001d,
  SEHeadLeftEarDirection = 0x0015,
  SEHeadUpDirection = 0x0014,
  SEHeadNoseDirection = 0x0013,
  SEHeadHeading = 0x0016,
  SEHeadPitch = 0x0017,
  SEHeadRoll = 0x0018,
  SEHeadRotationQ = 0x0019,

    //Raw Gaze
  SEGazeOrigin = 0x001a,
  SELeftGazeOrigin = 0x001b,
  SERightGazeOrigin = 0x001c,
  SEEyePosition = 0x0020,
  SEGazeDirection = 0x0021,
  SEGazeDirectionQ = 0x0022,
  SELeftEyePosition = 0x0023,
  SELeftGazeDirection = 0x0024,
  SELeftGazeDirectionQ = 0x0025,
  SERightEyePosition = 0x0026,
  SERightGazeDirection = 0x0027,
  SERightGazeDirectionQ = 0x0028,
  SEGazeHeading = 0x0029,
  SEGazePitch = 0x002a,
  SELeftGazeHeading = 0x002b,
  SELeftGazePitch = 0x002c,
  SERightGazeHeading = 0x002d,
  SERightGazePitch = 0x002e,

    //Filtered Gaze
  SEFilteredGazeDirection = 0x0030,
  SEFilteredGazeDirectionQ = 0x0031,
  SEFilteredLeftGazeDirection = 0x0032,
  SEFilteredLeftGazeDirectionQ = 0x0033,
  SEFilteredRightGazeDirection = 0x0034,
  SEFilteredRightGazeDirectionQ = 0x0035,
  SEFilteredGazeHeading = 0x0036,
  SEFilteredGazePitch = 0x0037,
  SEFilteredLeftGazeHeading = 0x0038,
  SEFilteredLeftGazePitch = 0x0039,
  SEFilteredRightGazeHeading = 0x003a,
  SEFilteredRightGazePitch = 0x003b,

    //Analysis (non-real-time)
  SESaccade = 0x003d,
  SEFixation = 0x003e,
  SEBlink = 0x003f,
  SELeftBlinkClosingMidTime = 0x00e0,
  SELeftBlinkOpeningMidTime = 0x00e1,
  SELeftBlinkClosingAmplitude = 0x00e2,
  SELeftBlinkOpeningAmplitude = 0x00e3,
  SELeftBlinkClosingSpeed = 0x00e4,
  SELeftBlinkOpeningSpeed = 0x00e5,
  SERightBlinkClosingMidTime = 0x00e6,
  SERightBlinkOpeningMidTime = 0x00e7,
  SERightBlinkClosingAmplitude = 0x00e8,
  SERightBlinkOpeningAmplitude = 0x00e9,
  SERightBlinkClosingSpeed = 0x00ea,
  SERightBlinkOpeningSpeed = 0x00eb,

    //Intersections
  SEClosestWorldIntersection = 0x0040,
  SEFilteredClosestWorldIntersection = 0x0041,
  SEAllWorldIntersections = 0x0042,
  SEFilteredAllWorldIntersections = 0x0043,
  SEZoneId = 0x0044,
  SEEstimatedClosestWorldIntersection = 0x0045,
  SEEstimatedAllWorldIntersections = 0x0046,
  SEHeadClosestWorldIntersection = 0x0049,
  SEHeadAllWorldIntersections = 0x004a,
  SECalibrationGazeIntersection = 0x00b0,
  SETaggedGazeIntersection = 0x00b1,
  SELeftClosestWorldIntersection = 0x00b2,
  SELeftAllWorldIntersections = 0x00b3,
  SERightClosestWorldIntersection = 0x00b4,
  SERightAllWorldIntersections = 0x00b5,
  SEFilteredLeftClosestWorldIntersection = 0x00b6,
  SEFilteredLeftAllWorldIntersections = 0x00b7,
  SEFilteredRightClosestWorldIntersection = 0x00b8,
  SEFilteredRightAllWorldIntersections = 0x00b9,
  SEEstimatedLeftClosestWorldIntersection = 0x00ba,
  SEEstimatedLeftAllWorldIntersections = 0x00bb,
  SEEstimatedRightClosestWorldIntersection = 0x00bc,
  SEEstimatedRightAllWorldIntersections = 0x00bd,
  SEFilteredEstimatedClosestWorldIntersection = 0x0141,
  SEFilteredEstimatedAllWorldIntersections = 0x0143,
  SEFilteredEstimatedLeftClosestWorldIntersection = 0x01b6,
  SEFilteredEstimatedLeftAllWorldIntersections = 0x01b7,
  SEFilteredEstimatedRightClosestWorldIntersection = 0x01b8,
  SEFilteredEstimatedRightAllWorldIntersections = 0x01b9,

    //Eyelid
  SEEyelidOpening = 0x0050,
  SEEyelidOpeningQ = 0x0051,
  SELeftEyelidOpening = 0x0052,
  SELeftEyelidOpeningQ = 0x0053,
  SERightEyelidOpening = 0x0054,
  SERightEyelidOpeningQ = 0x0055,
  SELeftLowerEyelidExtremePointDEPRECATED = 0x0058,
  SELeftUpperEyelidExtremePointDEPRECATED = 0x0059,
  SERightLowerEyelidExtremePointDEPRECATED = 0x005a,
  SERightUpperEyelidExtremePointDEPRECATED = 0x005b,
  SELeftEyelidState = 0x0390,
  SERightEyelidState = 0x0391,

    //Pupilometry
  SEPupilDiameter = 0x0060,
  SEPupilDiameterQ = 0x0061,
  SELeftPupilDiameter = 0x0062,
  SELeftPupilDiameterQ = 0x0063,
  SERightPupilDiameter = 0x0064,
  SERightPupilDiameterQ = 0x0065,
  SEFilteredPupilDiameter = 0x0066,
  SEFilteredPupilDiameterQ = 0x0067,
  SEFilteredLeftPupilDiameter = 0x0068,
  SEFilteredLeftPupilDiameterQ = 0x0069,
  SEFilteredRightPupilDiameter = 0x006a,
  SEFilteredRightPupilDiameterQ = 0x006b,

    //GPS Information
  SEGPSPosition = 0x0070,
  SEGPSGroundSpeed = 0x0071,
  SEGPSCourse = 0x0072,
  SEGPSTime = 0x0073,

    //Raw Estimated Gaze
  SEEstimatedGazeOrigin = 0x007a,
  SEEstimatedLeftGazeOrigin = 0x007b,
  SEEstimatedRightGazeOrigin = 0x007c,
  SEEstimatedEyePosition = 0x0080,
  SEEstimatedGazeDirection = 0x0081,
  SEEstimatedGazeDirectionQ = 0x0082,
  SEEstimatedGazeHeading = 0x0083,
  SEEstimatedGazePitch = 0x0084,
  SEEstimatedLeftEyePosition = 0x0085,
  SEEstimatedLeftGazeDirection = 0x0086,
  SEEstimatedLeftGazeDirectionQ = 0x0087,
  SEEstimatedLeftGazeHeading = 0x0088,
  SEEstimatedLeftGazePitch = 0x0089,
  SEEstimatedRightEyePosition = 0x008a,
  SEEstimatedRightGazeDirection = 0x008b,
  SEEstimatedRightGazeDirectionQ = 0x008c,
  SEEstimatedRightGazeHeading = 0x008d,
  SEEstimatedRightGazePitch = 0x008e,

    //Filtered Estimated Gaze
  SEFilteredEstimatedGazeDirection = 0x0091,
  SEFilteredEstimatedGazeDirectionQ = 0x0092,
  SEFilteredEstimatedGazeHeading = 0x0093,
  SEFilteredEstimatedGazePitch = 0x0094,
  SEFilteredEstimatedLeftGazeDirection = 0x0096,
  SEFilteredEstimatedLeftGazeDirectionQ = 0x0097,
  SEFilteredEstimatedLeftGazeHeading = 0x0098,
  SEFilteredEstimatedLeftGazePitch = 0x0099,
  SEFilteredEstimatedRightGazeDirection = 0x009b,
  SEFilteredEstimatedRightGazeDirectionQ = 0x009c,
  SEFilteredEstimatedRightGazeHeading = 0x009d,
  SEFilteredEstimatedRightGazePitch = 0x009e,

    //Status
  SETrackingState = 0x00c0,
  SEEyeglassesStatus = 0x00c1,
  SEReflexReductionStateDEPRECATED = 0x00c2,

    //Facial Feature Positions
  SELeftEyeOuterCorner3D = 0x0300,
  SELeftEyeInnerCorner3D = 0x0301,
  SERightEyeInnerCorner3D = 0x0302,
  SERightEyeOuterCorner3D = 0x0303,
  SELeftNostril3D = 0x0304,
  SERightNostril3D = 0x0305,
  SELeftMouthCorner3D = 0x0306,
  SERightMouthCorner3D = 0x0307,
  SELeftEar3D = 0x0308,
  SERightEar3D = 0x0309,
  SENoseTip3D = 0x0360,
  SELeftEyeOuterCorner2D = 0x0310,
  SELeftEyeInnerCorner2D = 0x0311,
  SERightEyeInnerCorner2D = 0x0312,
  SERightEyeOuterCorner2D = 0x0313,
  SELeftNostril2D = 0x0314,
  SERightNostril2D = 0x0315,
  SELeftMouthCorner2D = 0x0316,
  SERightMouthCorner2D = 0x0317,
  SELeftEar2D = 0x0318,
  SERightEar2D = 0x0319,
  SENoseTip2D = 0x0370,
  SEMouthShapePoints2D = 0x0320,
  SELeftEarShapePoints2D = 0x0321,
  SERightEarShapePoints2D = 0x0322,
  SENoseShapePoints2D = 0x0323,
  SELeftEyeShapePoints2D = 0x0324,
  SERightEyeShapePoints2D = 0x0325,

    //Emotion
  SEEmotionJoy = 0x03b0,
  SEEmotionFear = 0x03b1,
  SEEmotionDisgust = 0x03b2,
  SEEmotionSadness = 0x03b3,
  SEEmotionSurprise = 0x03b5,
  SEEmotionValence = 0x03b7,
  SEEmotionEngagement = 0x03b8,
  SEEmotionSentimentality = 0x03b9,
  SEEmotionConfusion = 0x03ba,
  SEEmotionNeutral = 0x03bb,
  SEEmotionQ = 0x03bc,

    //Expression
  SEExpressionSmile = 0x03c0,
  SEExpressionInnerBrowRaise = 0x03c1,
  SEExpressionBrowRaise = 0x03c2,
  SEExpressionBrowFurrow = 0x03c3,
  SEExpressionNoseWrinkle = 0x03c4,
  SEExpressionUpperLipRaise = 0x03c5,
  SEExpressionLipCornerDepressor = 0x03c6,
  SEExpressionChinRaise = 0x03c7,
  SEExpressionLipPucker = 0x03c8,
  SEExpressionLipPress = 0x03c9,
  SEExpressionLipSuck = 0x03ca,
  SEExpressionMouthOpen = 0x03cb,
  SEExpressionSmirk = 0x03d0,
  SEExpressionAttention = 0x03d3,
  SEExpressionEyeWiden = 0x03d4,
  SEExpressionCheekRaise = 0x03d5,
  SEExpressionLidTighten = 0x03d6,
  SEExpressionDimpler = 0x03d7,
  SEExpressionLipStretch = 0x03d8,
  SEExpressionJawDrop = 0x03d9,
  SEExpressionQ = 0x03e0,

    //Activity
  SESpeaking = 0x03f0,
  SESpeakingQ = 0x03f1,
      //0x0200 - 0x0202 cannot be used
    
  };
#if __STDC__ || __cplusplus
    //In c/c++ the namespace and public should not be included
#else
}
#endif