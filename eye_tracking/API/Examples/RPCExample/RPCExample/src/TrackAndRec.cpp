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

#include "TrackAndRec.h"
#include "RpcHandle.h"
#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <filesystem>

namespace
{
void notificationCB(const char* notificationName, const char*, void*)
{
  std::cout << "Executing callback for notification " << notificationName << std::endl;
}

static void checkResponseOk(const SEJsonRpcRequestResult res, const std::string& rpcCommandName)
{
  if (res.requestStatus != SEJsonRpcRequestStatus::OK)
  {
    std::cerr << rpcCommandName << " failed: " << res.requestError << std::endl;
    std::exit(-1);
  }
  else if (seParseSEErrorId(&res) != 0)
  {
    std::cout << rpcCommandName << " failed: " << res.jsonResponse << std::endl;
    std::exit(-1);
  }
  else
  {
    std::cout << rpcCommandName << " OK: " << res.jsonResponse << std::endl;
  }
}
} // namespace
int TrackAndRec::run()
{
  SEJsonRpcRequestResult res;

  // Initialize connection to Smart Eye Pro JSON-RPC. Note that the
  // RpcHandle class automatically calls seFree once out of scope.
  RpcHandle handle("127.0.0.1", 8100);

  const std::filesystem::path tmpDir = std::filesystem::temp_directory_path();
  const std::string recordPath = (tmpDir / "se_trackandrec_rec").string();
  const std::string logPath = (tmpDir / "se_trackandrec_log.log").string();

  std::cout << "recPath = \"" << recordPath << "\"" << std::endl;
  std::cout << "logPath = \"" << logPath << "\"" << std::endl;

  std::vector<std::string> notifications = {"recordingStarted",
                                            "recordingStopped",
                                            "recordingError",
                                            "trackingStarted",
                                            "trackingStopped"};
  const std::chrono::seconds recordTime = std::chrono::seconds(3);

  res = handle.initError();
  if (res.requestStatus != SEJsonRpcRequestStatus::OK)
  {
    std::cerr << "seInitialize failed: " << res.requestError << std::endl;
    return -1;
  }
  std::cout << "seInitialize OK." << std::endl;

  SEJsonRpcHandle h = handle.get();

  res = seSetRecordingFile(h, recordPath.c_str());
  checkResponseOk(res, "seSetRecordingFile");

  res = seSetLogFile(h, logPath.c_str());
  checkResponseOk(res, "seSetLogFile");

  for (auto notification : notifications)
  {
    res = seSubscribeToNotification(h, notification.c_str(), notificationCB);
    checkResponseOk(res, "seSubscribeToNotification");
  }

  // Define compression rate
  // 0 = uncompressed, 2 = compressed
  const int compressionRate = 0;
  res = seStartRecordingCompression(h, compressionRate);
  checkResponseOk(res, "seStartRecordingCompression");

  res = seStartTracking(h);
  checkResponseOk(res, "seStartTracking");

  res = seStartLogging(h);
  checkResponseOk(res, "seStartLogging");

  std::cout << "Recording for " << recordTime.count() << " seconds." << std::endl;
  std::this_thread::sleep_for(recordTime);

  res = seStopRecording(h);
  checkResponseOk(res, "seStopRecording");

  res = seStopLogging(h);
  checkResponseOk(res, "seStopLogging");

  res = seStopTracking(h);
  checkResponseOk(res, "seStopTracking");

  return 0;
}
