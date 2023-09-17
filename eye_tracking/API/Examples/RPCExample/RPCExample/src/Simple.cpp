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

#include <iostream>
#include "RpcHandle.h"
#include "Simple.h"

int Simple::run()
{
  SEJsonRpcRequestResult res;

  // Initialize connection to Smart Eye Pro JSON-RPC. Note that the
  // RpcHandle class automatically calls seFree once out of scope.
  RpcHandle handle("127.0.0.1", 8100);
  res = handle.initError();
  if (res.requestStatus != SEJsonRpcRequestStatus::OK)
  {
    std::cerr << "seInitialize failed: " << res.requestError << std::endl;
    return -1;
  }
  std::cout << "seInitialize OK." << std::endl;

  // Perform getProductName remote call.
  res = seGetProductName(handle.get());

  // Check request was performed and response received.
  if (res.requestStatus != SEJsonRpcRequestStatus::OK)
  {
    std::cerr << "seGetProductName request failed: " << res.requestError << std::endl;
    return -1;
  }

  // Check for application level errors in response.
  if (seParseSEErrorId(&res) != 0)
  {
    std::cerr << "seGetProductName failed: " << res.jsonResponse << std::endl;
    return -1;
  }

  // Request successful, res.jsonResponse contains the JSON encoded application
  // level response.
  std::cout << "seGetProductName OK: " << res.jsonResponse << std::endl;

  return 0;
}
