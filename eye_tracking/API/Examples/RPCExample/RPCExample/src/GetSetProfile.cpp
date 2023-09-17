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

#include "GetSetProfile.h"
#include "RpcHandle.h"
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <vector>
#include <filesystem>
#include <json.hpp>
using json = nlohmann::json;

namespace
{

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

std::string parseProfileResult(const std::string& rpcResponse)
{
  const json responseJson = json::parse(rpcResponse);
  const json resultJson = responseJson["result"];
  return resultJson.value("profile", "");
}

} // namespace
int GetSetProfile::run()
{
  SEJsonRpcRequestResult res;

  // Initialize connection to Smart Eye Pro JSON-RPC. Note that the
  // RpcHandle class automatically calls seFree once out of scope.
  RpcHandle handle("127.0.0.1", 8100);

  const std::filesystem::path tmpDir = std::filesystem::temp_directory_path();
  const std::string profilePath = (tmpDir / "se_getsetprofile.txt").string();

  std::cout << "profilePath = \"" << profilePath << "\"" << std::endl;

  const std::chrono::seconds trackTime = std::chrono::seconds(2);

  res = handle.initError();
  if (res.requestStatus != SEJsonRpcRequestStatus::OK)
  {
    std::cerr << "seInitialize failed: " << res.requestError << std::endl;
    return -1;
  }
  std::cout << "seInitialize OK." << std::endl;

  SEJsonRpcHandle h = handle.get();

  // Start tracking to get an interesting profile
  res = seStartTracking(h);
  checkResponseOk(res, "seStartTracking");

  std::cout << "Tracking for " << trackTime.count() << " seconds." << std::endl;
  std::this_thread::sleep_for(trackTime);

  res = seStopTracking(h);
  checkResponseOk(res, "seStopTracking");

  res = seGetProfile(h);
  checkResponseOk(res, "seGetProfile");

  const std::string profileResponse = res.jsonResponse;

  // Parse json response from RPC to get the profile string
  const std::string profileToSave = parseProfileResult(profileResponse);

  // Save profile
  std::ofstream saveFile(profilePath);
  if (saveFile.is_open())
  {
    saveFile << profileToSave;
    saveFile.close();
  }

  // Clear profile
  res = seClearProfile(h);
  checkResponseOk(res, "seClearProfile");

  // Load profile
  std::ifstream ifs(profilePath);
  const std::string inProfile((std::istreambuf_iterator<char>(ifs)),
                              (std::istreambuf_iterator<char>()));

  // Set profile in SEP again
  res = seSetProfile(h, inProfile.c_str());
  checkResponseOk(res, "seSetProfile");

  return 0;
}
