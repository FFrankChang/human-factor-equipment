/*
 * Copyright (c) Smart Eye AB, Sweden. All Rights Reserved.
 *
 * This information is supplied under the terms of a license agreement
 * or nondisclosure agreement with Smart Eye AB and may not be copied
 * or disclosed except in accordance with the terms of that agreement.
 *
 */

#ifndef _SERPC_
#define _SERPC_

#ifdef SERPC_EXPORTS
#define SERPC_API __declspec(dllexport)
#else
#define SERPC_API __declspec(dllimport)
#endif

#include <cstdlib>

extern "C"
{
  typedef void* SEJsonRpcHandle;

  // Request status
  typedef enum
  {
    OK = 0,
    FAILED = 1,
    PENDING = 2
  } SEJsonRpcRequestStatus;

  // Connection status
  typedef enum
  {
    CONNECTED = 0,
    TRY_CONNECT = 1,
    NOT_CONNECTED = 2
  } SEJsonRpcConnectionStatus;

  // Request result
  struct SEJsonRpcRequestResult
  {
    // The request id.
    int requestId;

    // The status of the request, see SEJsonRpcRequestStatus.
    SEJsonRpcRequestStatus requestStatus;

    // Description of the error that occurred, is null if no error exists.
    //
    // NOTE: The memory pointed to by requestError is owned by the SEJsonRpc
    // instance. The memory is valid only until the next RPC request call, or
    // until seFree is called, whichever happens first.
    char* requestError;

    // The returned response from the application, this json string needs to be
    // parsed for application errors and returned data. This field may be null.
    //
    // NOTE: The memory pointed to by jsonResponse is owned by the SEJsonRpc
    // instance. The memory is valid only until the next RPC request call, or
    // until seFree is called, whichever happens first.
    char* jsonResponse;
  };

  // Callback type definitions
  typedef void (*seCallback)(SEJsonRpcRequestStatus status, void* context);
  typedef void (*seFunctionCallback)(int id, SEJsonRpcRequestResult* result, void* context);
  typedef void (*seNotificationCallback)(const char* notificationName,
                                         const char* notificationParams,
                                         void* context);

  // Response parsing helper
  SERPC_API int seParseSEErrorId(const SEJsonRpcRequestResult* result);

  // Initialize and Free
  SERPC_API SEJsonRpcRequestResult seInitialize(SEJsonRpcHandle* handle,
                                                const char* hostname = "127.0.0.1",
                                                int port = 8100,
                                                seCallback disconnectedCallback = NULL,
                                                void* disconnectContext = NULL,
                                                seCallback connectCallback = NULL,
                                                void* connectContext = NULL);
  SERPC_API void seFree(SEJsonRpcHandle handle);

  // Connection status
  SERPC_API SEJsonRpcConnectionStatus seGetConnectionStatus(SEJsonRpcHandle handle);

  // Requests
  SERPC_API SEJsonRpcRequestResult seGetRealTimeClock(SEJsonRpcHandle handle,
                                                      seFunctionCallback cb = NULL,
                                                      void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetRPCVersion(SEJsonRpcHandle handle,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetState(SEJsonRpcHandle handle,
                                              seFunctionCallback cb = NULL,
                                              void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetRecordingState(SEJsonRpcHandle handle,
                                                       seFunctionCallback cb = NULL,
                                                       void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetProductName(SEJsonRpcHandle handle,
                                                    seFunctionCallback cb = NULL,
                                                    void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetProductVersion(SEJsonRpcHandle handle,
                                                       seFunctionCallback cb = NULL,
                                                       void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetCameraType(SEJsonRpcHandle handle,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetFirmwareVersions(SEJsonRpcHandle handle,
                                                         seFunctionCallback cb = NULL,
                                                         void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seSetLogSpecification(SEJsonRpcHandle handle,
                                                         const char* spec,
                                                         seFunctionCallback cb = NULL,
                                                         void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seSetLogFile(SEJsonRpcHandle handle,
                                                const char* filename,
                                                seFunctionCallback cb = NULL,
                                                void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seLoadProfile(SEJsonRpcHandle handle,
                                                 const char* filename,
                                                 seFunctionCallback cb = NULL,
                                                 void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seSaveProfile(SEJsonRpcHandle handle,
                                                 const char* filename,
                                                 seFunctionCallback cb = NULL,
                                                 void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seGetProfile(SEJsonRpcHandle handle,
                                                seFunctionCallback cb = NULL,
                                                void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seSetProfile(SEJsonRpcHandle handle,
                                                const char* profileData,
                                                seFunctionCallback cb = NULL,
                                                void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seClearProfile(SEJsonRpcHandle handle,
                                                  seFunctionCallback cb = NULL,
                                                  void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seStartLogging(SEJsonRpcHandle handle,
                                                  seFunctionCallback cb = NULL,
                                                  void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStopLogging(SEJsonRpcHandle handle,
                                                 seFunctionCallback cb = NULL,
                                                 void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seStartTracking(SEJsonRpcHandle handle,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStopTracking(SEJsonRpcHandle handle,
                                                  seFunctionCallback cb = NULL,
                                                  void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seSetRecordingFile(SEJsonRpcHandle handle,
                                                      const char* filename,
                                                      seFunctionCallback cb = NULL,
                                                      void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStartRecording(SEJsonRpcHandle handle,
                                                    seFunctionCallback cb = NULL,
                                                    void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStartRecordingCompression(SEJsonRpcHandle handle,
                                                               int compressionRate,
                                                               seFunctionCallback cb = NULL,
                                                               void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStopRecording(SEJsonRpcHandle handle,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seSetImageSourceRecording(SEJsonRpcHandle handle,
                                                             const char* filename,
                                                             seFunctionCallback cb = NULL,
                                                             void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seSetImageSourceCameras(SEJsonRpcHandle handle,
                                                           seFunctionCallback cb = NULL,
                                                           void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seKeyDown(SEJsonRpcHandle handle,
                                             const char* key,
                                             seFunctionCallback cb = NULL,
                                             void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seKeyUp(SEJsonRpcHandle handle,
                                           const char* key,
                                           seFunctionCallback cb = NULL,
                                           void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seStartCollectSamplesWCS(SEJsonRpcHandle handle,
                                                            int targetId,
                                                            double x,
                                                            double y,
                                                            double z,
                                                            int timeout,
                                                            seFunctionCallback cb = NULL,
                                                            void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStartCollectSamplesByTargetName(SEJsonRpcHandle handle,
                                                                     int targetId,
                                                                     const char* targetName,
                                                                     int timeout,
                                                                     seFunctionCallback cb = NULL,
                                                                     void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStartCollectSamplesObject(SEJsonRpcHandle handle,
                                                               int targetId,
                                                               const char* objectName,
                                                               double x,
                                                               double y,
                                                               double z,
                                                               int timeout,
                                                               seFunctionCallback cb = NULL,
                                                               void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStopCollectSamples(SEJsonRpcHandle handle,
                                                        seFunctionCallback cb = NULL,
                                                        void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seCalibrateGaze(SEJsonRpcHandle handle,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seApplyGazeCalibration(SEJsonRpcHandle handle,
                                                          seFunctionCallback cb = NULL,
                                                          void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seClearGazeCalibration(SEJsonRpcHandle handle,
                                                          seFunctionCallback cb = NULL,
                                                          void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seStartCollectPointSamplesAutomatic(SEJsonRpcHandle handle,
                                                                       seFunctionCallback cb = NULL,
                                                                       void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seStopCollectPointSamplesAutomatic(SEJsonRpcHandle handle,
                                                                      seFunctionCallback cb = NULL,
                                                                      void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seRetrieveTargetStatistics(SEJsonRpcHandle handle,
                                                              int targetId,
                                                              seFunctionCallback cb = NULL,
                                                              void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult
  seRetrieveTargetStatisticsWithGazeOrigin(SEJsonRpcHandle handle,
                                           int targetId,
                                           seFunctionCallback cb = NULL,
                                           void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seRetrieveCalibrationResults(SEJsonRpcHandle handle,
                                                                seFunctionCallback cb = NULL,
                                                                void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seClearTargetSamples(SEJsonRpcHandle handle,
                                                        int targetId,
                                                        seFunctionCallback cb = NULL,
                                                        void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seClearAllTargetSamples(SEJsonRpcHandle handle,
                                                           seFunctionCallback cb = NULL,
                                                           void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seOpenDataStreamUDP(SEJsonRpcHandle handle,
                                                       int port = 5100,
                                                       const char* spec = "",
                                                       const char* clientAddress = "",
                                                       seFunctionCallback cb = NULL,
                                                       void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seCloseDataStreamUDP(SEJsonRpcHandle handle,
                                                        int port = 5100,
                                                        const char* clientAddress = "",
                                                        seFunctionCallback cb = NULL,
                                                        void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seOpenDataStreamTCP(SEJsonRpcHandle handle,
                                                       int port = 5200,
                                                       const char* spec = "",
                                                       seFunctionCallback cb = NULL,
                                                       void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seCloseDataStreamTCP(SEJsonRpcHandle handle,
                                                        int port = 5200,
                                                        seFunctionCallback cb = NULL,
                                                        void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seSubscribeToNotification(SEJsonRpcHandle handle,
                                                             const char* notificationName,
                                                             seNotificationCallback cb,
                                                             void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seUnsubscribeToNotification(SEJsonRpcHandle handle,
                                                               const char* notificationName);
  SERPC_API SEJsonRpcRequestResult seSendNotification(SEJsonRpcHandle handle,
                                                      const char* notificationName,
                                                      const char* notificationParams = "");

  SERPC_API SEJsonRpcRequestResult seGetWorldModel(SEJsonRpcHandle handle,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seSetWorldModel(SEJsonRpcHandle handle,
                                                   const char* worldModel,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seLoadWorldModel(SEJsonRpcHandle handle,
                                                    const char* worldModelFile = NULL,
                                                    seFunctionCallback cb = NULL,
                                                    void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seShutdown(SEJsonRpcHandle handle,
                                              seFunctionCallback cb = NULL,
                                              void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seGetCameraImage(SEJsonRpcHandle handle,
                                                    int index,
                                                    float scale,
                                                    seFunctionCallback cb = NULL,
                                                    void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seSetReflexReductionMode(SEJsonRpcHandle handle,
                                                            int rrMode,
                                                            seFunctionCallback cb = NULL,
                                                            void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seGetSubjectCategory(SEJsonRpcHandle handle,
                                                        seFunctionCallback cb = NULL,
                                                        void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seSetSubjectCategory(SEJsonRpcHandle handle,
                                                        int subjectCategory,
                                                        seFunctionCallback cb = NULL,
                                                        void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seGetActiveEyes(SEJsonRpcHandle handle,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);
  SERPC_API SEJsonRpcRequestResult seSetActiveEyes(SEJsonRpcHandle handle,
                                                   bool left,
                                                   bool right,
                                                   seFunctionCallback cb = NULL,
                                                   void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seGetIlluminationMode(SEJsonRpcHandle handle,
                                                         seFunctionCallback cb = NULL,
                                                         void* userContext = NULL);

  SERPC_API SEJsonRpcRequestResult seSetIlluminationMode(SEJsonRpcHandle handle,
                                                         int mode,
                                                         seFunctionCallback cb = NULL,
                                                         void* userContext = NULL);
};

#endif //_SERPC_
