// Copyright (C) Smart Eye AB 2002-2018
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

#ifdef BUILDING_TIMESERVICE
#define TIMESERVICE_API __declspec(dllexport)
#else
#define TIMESERVICE_API __declspec(dllimport)
#endif

#if defined(__cplusplus)
extern "C"
{
#endif

  // types
  // -----

  // opaque handle to the time service
  // it may be used to identify a client and/or refer to private data structures
  typedef void* TTimeServiceHandle;

  // user time is stored in a 64 bit opaque data structure
  typedef unsigned __int64 TOpaqueUserTime;

  // functions
  // ---------
  // all functions return 1 on success, 0 on failure

  // start and possibly synchronize the time service, allocate any resources needed
  // this function is called exactly once (per client) before any other calls are made from that client
  TIMESERVICE_API int startTimeService(TTimeServiceHandle* handle); // [out] time service handle

  // stop time service and release resources
  // this function is called exactly once (per client) after all other calls have been made
  TIMESERVICE_API int stopTimeService(TTimeServiceHandle handle); // [in] time service handle

  // get the current time in user format
  // to the result should be added a time offset in order to get the actual time of a past or future event
  // this function might be called from time-critical sections of the code,
  // and should avoid potentially blocking calls and return as soon as possible
  TIMESERVICE_API int getCurrentTime(
      TTimeServiceHandle handle,     // [in] time service handle
      signed __int64 offset,         // [in] offset in 100 ns units
      TOpaqueUserTime* currentTime); // [out] current time in user format, adjusted by offset

  // convert a user format timestamp to a human readable text format
  // the text format is intended for presentation and not data logging, so a one-to-one mapping is not required
  TIMESERVICE_API int timeToString(
      TTimeServiceHandle handle,   // [in] time service handle
      TOpaqueUserTime currentTime, // [in] time in user format
      unsigned long*
          bufferSize, // [in/out] size of text buffer in bytes incl null termination (in = max, out = actual)
      char* textBuffer); // [out] time in text format (null terminated)

#if defined(__cplusplus)
} // extern "C"
#endif
