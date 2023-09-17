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
// F�rsta l�nggatan 28 B,
// 413 27 G�teborg, Sweden
// Contact: support@smarteye.se
//
// You are free to modify and use this code together with
// your purchased Smart Eye system.
//
// You MAY NOT distribute this code (modified or unmodified)
// without prior written consent from Smart Eye AB.
//----------------------------------------------------------------------------//

#include "stdafx.h"
#include "../../include/TimeService.h"

#if defined(__cplusplus)
extern "C"
{
#endif

  BOOL APIENTRY DllMain(HANDLE /*hModule*/, DWORD ul_reason_for_call, LPVOID /*lpReserved*/)
  {
    switch (ul_reason_for_call)
    {
      case DLL_PROCESS_ATTACH:
      case DLL_THREAD_ATTACH:
      case DLL_THREAD_DETACH:
      case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
  }

  // magic signature used to validate private data block
  const long MAGIC_SIGNATURE = 0x7715ABBA;

  struct TPrivateData
  {
    long magic;
    TIME_ZONE_INFORMATION timeZoneInformation;
  };

  inline TPrivateData* checkHandle(TTimeServiceHandle handle)
  {
    TPrivateData* pPrivateData = (TPrivateData*)handle;
    if (pPrivateData && (MAGIC_SIGNATURE == pPrivateData->magic))
    {
      return pPrivateData;
    }
    else
    {
      return 0;
    }
  }

  static HANDLE syncThreadHandle;
  static DWORD syncThreadId;
  static HANDLE quitThreadEvent;
  static HANDLE doneThreadEvent;

  static LARGE_INTEGER counterFrequency;

  struct TCurrentTimeBase
  {
    ULARGE_INTEGER currentFileTime;
    LARGE_INTEGER counterBaseValue;
  };
  static struct TCurrentTimeBase currentTimeBase;

  // Ref: http://msdn.microsoft.com/en-us/magazine/cc163996.aspx
  DWORD WINAPI syncThread(LPVOID /*param*/)
  {
    struct TCurrentTimeBase timeBase;

    // Get current filetime
    FILETIME fileTime;
    GetSystemTimeAsFileTime(&fileTime);
    timeBase.currentFileTime.HighPart = fileTime.dwHighDateTime;
    timeBase.currentFileTime.LowPart = fileTime.dwLowDateTime;

    // Get current counter value
    QueryPerformanceCounter(&timeBase.counterBaseValue);

    // Update timebase
    currentTimeBase = timeBase;

    // Basetime for execution time
    LARGE_INTEGER executionBase = timeBase.counterBaseValue;
    BOOL firstRun = TRUE;

    // Main loop
    while (TRUE)
    {
      // Valid flank detection
      BOOL done = FALSE;

      LARGE_INTEGER prev_diff, p0, p1;
      prev_diff.QuadPart = 0;

      QueryPerformanceCounter(&p0);

      // Get current file time
      GetSystemTimeAsFileTime(&fileTime);
      timeBase.currentFileTime.HighPart = fileTime.dwHighDateTime;
      timeBase.currentFileTime.LowPart = fileTime.dwLowDateTime;

      // Synchronization loop
      while (TRUE)
      {
        // Get current file time
        GetSystemTimeAsFileTime(&fileTime);
        ULARGE_INTEGER currentFileTime;
        currentFileTime.HighPart = fileTime.dwHighDateTime;
        currentFileTime.LowPart = fileTime.dwLowDateTime;

        QueryPerformanceCounter(&p1);

        // Check for flank
        if (currentFileTime.QuadPart > timeBase.currentFileTime.QuadPart)
        {
          // Max one tick
          if (currentFileTime.QuadPart - timeBase.currentFileTime.QuadPart < 312500)
          {
            // Valid limit
            if (double(p1.QuadPart - p0.QuadPart + prev_diff.QuadPart) /
                    (double)counterFrequency.QuadPart <
                0.002)
            {
              // Get current counter value as base
              timeBase.counterBaseValue.QuadPart =
                  p1.QuadPart - (p1.QuadPart - p0.QuadPart + prev_diff.QuadPart) / 2;

              // Store the new filetime
              timeBase.currentFileTime = currentFileTime;

              // Update timebase
              currentTimeBase = timeBase;

              done = TRUE;
              break;
            }
            else
            {
              break;
            }
          }
          else
          {
            break;
          }
        }
        else
        {
          // Maximum execution time exceeded
          if (firstRun == FALSE &&
              double(p1.QuadPart - executionBase.QuadPart) / (double)counterFrequency.QuadPart >
                  0.001)
          {
            done = TRUE;
            break;
          }

          prev_diff.QuadPart = p1.QuadPart - p0.QuadPart;
          p0 = p1;
        }
      }

      // Check flank detection or exceeded execution time
      if (done == TRUE)
      {
        // Toggle first run
        if (firstRun == TRUE)
        {
          firstRun = FALSE;
        }

        // Wait for quit or timeout
        if (WaitForSingleObject(quitThreadEvent, 1000) == WAIT_OBJECT_0)
        {
          break;
        }

        // Get frequency for counter
        QueryPerformanceFrequency(&counterFrequency);

        // Basetime for execution time
        QueryPerformanceCounter(&executionBase);
      }
    }

    SetEvent(doneThreadEvent);

    return 1;
  }

  int startTimeService(TTimeServiceHandle* handle)
  {
    // default return value is empty handle
    *handle = 0;

    // allocate a block of memory from Win32
    TPrivateData* pPrivateData = (TPrivateData*)GlobalAlloc(GPTR, sizeof(TPrivateData));
    if (!pPrivateData)
    {
      // failure
      return 0;
    }

    // mark it with the magic signature
    pPrivateData->magic = MAGIC_SIGNATURE;

    // get timezone information
    DWORD stat = GetTimeZoneInformation(&pPrivateData->timeZoneInformation);
    if (stat == TIME_ZONE_ID_INVALID)
    {
      // failure
      GlobalFree(pPrivateData);
      return 0;
    }

    // Get frequency
    if (!QueryPerformanceFrequency(&counterFrequency))
    {
      // the installed hardware does not support a high-resolution performance counter
      return 0;
    }

    // Run synchronization thread
    quitThreadEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
    doneThreadEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
    syncThreadHandle = CreateThread(NULL, 0, &syncThread, 0, 0, &syncThreadId);

    // return handle
    *handle = pPrivateData;

    // success
    return 1;
  }

  int stopTimeService(TTimeServiceHandle handle)
  {
    // return memory block to Win32
    TPrivateData* verifiedHandle = checkHandle(handle);
    if (verifiedHandle)
    {
      verifiedHandle->magic = 0; // invalidate
      GlobalFree(handle);
    }

    // Stop synchronization thread
    SetEvent(quitThreadEvent);
    WaitForSingleObject(doneThreadEvent, INFINITE);

    // report success (whatever happened)
    return 1;
  }

  int getCurrentTime(TTimeServiceHandle handle, signed __int64 offset, TOpaqueUserTime* currentTime)
  {
    // dummy result;
    *currentTime = 0;

    TPrivateData* pPrivateData = checkHandle(handle);
    if (!pPrivateData || !currentTime)
    {
      // bad parameters, fail
      return 0;
    }

    // get current UTC time
    TCurrentTimeBase timeBase = currentTimeBase;

    // calculate diff
    LARGE_INTEGER counterValue;
    QueryPerformanceCounter(&counterValue);
    __int64 counterDiff = counterValue.QuadPart - timeBase.counterBaseValue.QuadPart;
    __int64 counterOffset =
        (__int64)((double)counterDiff / (double)counterFrequency.QuadPart * 10000000.0);

    // adjust for offsets
    *currentTime = timeBase.currentFileTime.QuadPart + counterOffset + offset;

    // success
    return 1;
  }

  int timeToString(TTimeServiceHandle handle,
                   TOpaqueUserTime currentTime,
                   unsigned long* bufferSize,
                   char* textBuffer)
  {
    if (!textBuffer || !bufferSize || !*bufferSize)
    {
      // bad parameters, fail
      return 0;
    }

    // default result = empty string
    const unsigned long bufferSizeIn = *bufferSize;
    *textBuffer = 0;
    *bufferSize = 1;

    TPrivateData* pPrivateData = checkHandle(handle);
    if (!pPrivateData)
    {
      // bad parameters, fail
      return 0;
    }

    // we treat 0 as a special case that just gets converted into an empty string
    if (currentTime == 0)
    {
      return 1;
    }

    // convert UTC time to local time
    const FILETIME utcFileTime = *(FILETIME*)(&currentTime);
    FILETIME localFileTime;
    BOOL stat = FileTimeToLocalFileTime(&utcFileTime, &localFileTime);
    if (stat == 0)
    {
      // failed conversion
      return 0;
    }

    // convert local time to local system time format
    SYSTEMTIME localSystemTime;
    stat = FileTimeToSystemTime(&localFileTime, &localSystemTime);
    if (stat == 0)
    {
      // failed conversion
      return 0;
    }

    // convert to text format YYYY-MM-DD hh:mm:ss.sss [TZID]
    unsigned int theoreticalSize =
        4 + 1 + 2 + 1 + 2 + 1 + 2 + 1 + 2 + 1 + 2 + 1 + 3 + 1 + 1 +
        static_cast<unsigned int>(wcslen(pPrivateData->timeZoneInformation.StandardName)) + 1 + 1;
    if (theoreticalSize > bufferSizeIn)
    {
      // not room enough for result
      return 0;
    }
    unsigned int actualSize = wsprintf(textBuffer,
                                       "%04d-%02d-%02d %02d:%02d:%02d.%03d [%ls]",
                                       localSystemTime.wYear,
                                       localSystemTime.wMonth,
                                       localSystemTime.wDay,
                                       localSystemTime.wHour,
                                       localSystemTime.wMinute,
                                       localSystemTime.wSecond,
                                       localSystemTime.wMilliseconds,
                                       pPrivateData->timeZoneInformation.StandardName) +
                              1;
    *bufferSize = actualSize;

    // success
    return 1;
  }

#if defined(__cplusplus)
} // extern "C"
#endif
