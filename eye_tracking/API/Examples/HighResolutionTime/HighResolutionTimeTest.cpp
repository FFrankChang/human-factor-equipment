// Copyright (C) Smart Eye AB 2002-2021
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
//
// time service function declarations
#include "../../include/TimeService.h"

#include <cstdlib>
#include <cstdio>
#include <iostream>

// Typedefs
typedef __int64 s64;

// UDP
#include <winsock2.h>
#define getsockerror() WSAGetLastError()
#define sockLibInit() initWinSock()
#define sockLibCleanup() WSACleanup()
int initWinSock(void)
{
  // Initialize the Windows socket library
  WSADATA info;
  if (WSAStartup(0x0002, &info) == SOCKET_ERROR)
  {
    std::cerr << "Could not initialize socket library!\n";
    exit(1);
  }
  return 0;
}

const int defaultPortNo = 5003;

typedef struct
{
  TOpaqueUserTime t1;
  TOpaqueUserTime t2;
  TOpaqueUserTime t3;
  TOpaqueUserTime t4;
} SyncTimes;

void clearTime(SyncTimes& times)
{
  times.t1 = 0;
  times.t2 = 0;
  times.t3 = 0;
  times.t4 = 0;
}

int main(int argc, char* argv[])
{
  // check command line arguments
  if (argc != 5)
  {
    printf(
        "Usage: %s <DLLFileName> <offset> <remoteHost> <clientType>\n"
        "where remoteHost is the ip address to the host\n"
        "and clienttype is either a or b (one client should be a and one b)\n",
        argv[0]);
    return 1;
  }
  char client = argv[4][0];
  if (!(client == 'a' || client == 'b'))
  {
    printf("Unkown client type!\n");
    return 1;
  }
  printf("HighResolutionTimeTest:\n");

  // read offset from command line
  s64 offset = _atoi64(argv[2]);

  int stat;

  // Get a handle to the DLL module
  HINSTANCE hinstLib = LoadLibrary(argv[1]);
  if (!hinstLib)
  {
    printf("Error: %s failed to load DLL '%s'\n", argv[0], argv[1]);
    return 1;
  }

  // acquire function pointers

  auto* fptr_startTimeService =
      (int (*)(TTimeServiceHandle))GetProcAddress(hinstLib, "startTimeService");
  if (!fptr_startTimeService)
  {
    std::cerr << "Failed to load function \"startTimeService()\"\n";
    return 1;
  }

  auto* fptr_stopTimeService =
      (int (*)(TTimeServiceHandle))GetProcAddress(hinstLib, "stopTimeService");
  if (!fptr_stopTimeService)
  {
    std::cerr << "Failed to load function \"stopTimeService()\"\n";
    return 1;
  }

  auto* fptr_getCurrentTime =
      (int (*)(TTimeServiceHandle, signed __int64, TOpaqueUserTime*))GetProcAddress(
          hinstLib, "getCurrentTime");
  if (!fptr_getCurrentTime)
  {
    std::cerr << "Failed to load function \"getCurrentTime()\"\n";
    return 1;
  }

  auto* fptr_timeToString =
      (int (*)(TTimeServiceHandle, TOpaqueUserTime, unsigned long*, char*))GetProcAddress(
          hinstLib, "timeToString");
  if (!fptr_timeToString)
  {
    std::cerr << "Failed to load function \"timeToString()\"\n";
    return 1;
  }

  // start the time service
  TTimeServiceHandle hts = 0;
  stat = fptr_startTimeService(&hts);
  printf("* startTimeService returned %d\n", stat);

  // Read remote host from command line
  char* remoteHost = argv[3];

  // Initialize socket library
  sockLibInit();

  // Resolve remote host
  struct hostent* remote_hp = gethostbyname(remoteHost);
  if (!remote_hp)
  {
    printf("Error: %s could not resolve host name \"%s\"!\n", argv[0], remoteHost);
    sockLibCleanup();
    return 1;
  }

  // set default port number depending on client
  int recPortNo = defaultPortNo;
  int sendPortNo = defaultPortNo + 1;
  if (client == 'b')
  {
    recPortNo = defaultPortNo + 1;
    sendPortNo = defaultPortNo;
  }

  // Setup remote sockaddr_in
  struct sockaddr_in remote;
  memset(&remote, 0, sizeof(remote));
  memcpy((char*)&remote.sin_addr, remote_hp->h_addr, remote_hp->h_length);
  remote.sin_family = remote_hp->h_addrtype;
  remote.sin_port = htons((u_short)sendPortNo);

  // Setup local sockaddr_in
  struct sockaddr_in local;
  memset(&local, 0, sizeof(remote));
  local.sin_family = remote_hp->h_addrtype;
  local.sin_port = htons((u_short)recPortNo);

  // Create socket
  SOCKET socketConnection = socket(remote_hp->h_addrtype, SOCK_DGRAM, 0);
  if (socketConnection == SOCKET_ERROR)
  {
    printf("Error: %s could not create socket with error %d!\n", argv[0], getsockerror());
    sockLibCleanup();
    return 1;
  }

  // Try to bind to the specified socket
  stat = bind(socketConnection, (struct sockaddr*)&local, sizeof(local));
  if (stat == SOCKET_ERROR)
  {
    printf("Error: %s could not bind to socket with error %d!\n", argv[0], getsockerror());
    closesocket(socketConnection);
    sockLibCleanup();
    return 1;
  }

  printf("* remote host is %s\n", remoteHost);

  SyncTimes timeData1;
  SyncTimes timeData2;

  s64 diffMax = 0;
  s64 diffMin = _I64_MAX;

  s64 diffMeanMax = 0;
  s64 diffMeanMin = 0;
  s64 diffNum = 0;

  // setup console for character mode
  HANDLE hConsoleIn = GetStdHandle(STD_INPUT_HANDLE);
  SetConsoleMode(hConsoleIn, ENABLE_PROCESSED_INPUT);

  while (true)
  {
    clearTime(timeData1);
    clearTime(timeData2);

    s64 currentDiff1 = 0;
    s64 currentDiff2 = 0;
    s64 currentWindowSize = 0;

    if (client == 'a')
    {
      // wait for keypress
      printf("-- press a key to read time, or Q to quit --\n");
      char buf;
      DWORD nChars;
      ReadConsole(hConsoleIn, &buf, 1, &nChars, NULL);
      if (buf == 'q' || buf == 'Q')
      {
        break;
      }

      // t1a0
      stat = fptr_getCurrentTime(hts, offset, &timeData1.t1);
      stat = sendto(socketConnection,
                    (const char*)&timeData1,
                    sizeof(SyncTimes),
                    0,
                    (struct sockaddr*)&remote,
                    sizeof(remote));
      if (stat == SOCKET_ERROR)
      {
        printf("Error: %s failed to send with error %d!\n", argv[0], getsockerror());
        break;
      }

      // t1a1
      stat = fptr_getCurrentTime(hts, offset, &timeData1.t2);
      stat = recv(socketConnection, (char*)&timeData2, sizeof(SyncTimes), 0);
      if (stat == SOCKET_ERROR)
      {
        printf("Error: %s failed to recieve with error %d!\n", argv[0], getsockerror());
        break;
      }

      // t3a0
      stat = fptr_getCurrentTime(hts, offset, &timeData1.t4);
      if (timeData2.t1 != timeData1.t1)
      {
        printf("Error: %s recieved faulty data!\n", argv[0]);
        continue;
      }

      timeData1.t3 = timeData2.t2;

      stat = sendto(socketConnection,
                    (const char*)&timeData1,
                    sizeof(SyncTimes),
                    0,
                    (struct sockaddr*)&remote,
                    sizeof(remote));
      if (stat == SOCKET_ERROR)
      {
        printf("Error: %s failed to send with error %d!\n", argv[0], getsockerror());
        break;
      }

      // Calculate diffs
      currentWindowSize = timeData1.t4 - timeData1.t1;
      currentDiff1 = timeData1.t3 - timeData1.t1 - currentWindowSize / 2;
      currentDiff2 = timeData1.t4 - timeData1.t3 - currentWindowSize / 2;
    }
    else if (client == 'b')
    {
      stat = recv(socketConnection, (char*)&timeData2, sizeof(SyncTimes), 0);
      if (stat == SOCKET_ERROR)
      {
        printf("Error: %s failed to recieve with error %d!\n", argv[0], getsockerror());
        break;
      }

      timeData1.t1 = timeData2.t1;

      // t2b0
      stat = fptr_getCurrentTime(hts, offset, &timeData1.t2);
      stat = sendto(socketConnection,
                    (const char*)&timeData1,
                    sizeof(SyncTimes),
                    0,
                    (struct sockaddr*)&remote,
                    sizeof(remote));
      if (stat == SOCKET_ERROR)
      {
        printf("Error: %s failed to send with error %d!\n", argv[0], getsockerror());
        break;
      }

      // t2b1
      stat = fptr_getCurrentTime(hts, offset, &timeData1.t3);

      stat = recv(socketConnection, (char*)&timeData2, sizeof(SyncTimes), 0);
      if (stat == SOCKET_ERROR)
      {
        printf("Error: %s failed to recieve with error %d!\n", argv[0], getsockerror());
        break;
      }

      // Check recieved data
      if (timeData2.t1 != timeData1.t1)
      {
        printf("Error: %s recieved faulty data!\n", argv[0]);
        continue;
      }

      // t4b0
      stat = fptr_getCurrentTime(hts, offset, &timeData1.t4);

      // Calculate diffs
      currentWindowSize = timeData1.t4 - timeData1.t2;
      currentDiff1 = timeData2.t4 - timeData1.t2 - currentWindowSize / 2;
      currentDiff2 = timeData1.t4 - timeData2.t4 - currentWindowSize / 2;
    }

    // Update max/min
    const s64 absDiff1 = _abs64(currentDiff1);
    const s64 absDiff2 = _abs64(currentDiff2);
    if ((absDiff1 >= absDiff2) && (absDiff1 > diffMax))
    {
      diffMax = absDiff1;
    }
    else if ((absDiff2 > absDiff1) && (absDiff2 > diffMax))
    {
      diffMax = absDiff2;
    }
    if ((absDiff1 <= absDiff2) && (absDiff1 < diffMin))
    {
      diffMin = absDiff1;
    }
    else if ((absDiff2 < absDiff1) && (absDiff2 < diffMin))
    {
      diffMin = absDiff2;
    }

    // Calculate mean
    if (currentWindowSize < 10000)
    {
      if (currentDiff1 < currentDiff2)
      {
        diffMeanMin += currentDiff1;
        diffMeanMax += currentDiff2;
      }
      else
      {
        diffMeanMax += currentDiff1;
        diffMeanMin += currentDiff2;
      }

      diffNum++;
    }

    // Print results
    const unsigned long MAXBUFSIZE = 128;
    char textBuffer[MAXBUFSIZE];

    unsigned long bufferSize = MAXBUFSIZE;
    stat = fptr_timeToString(hts, timeData1.t1, &bufferSize, textBuffer);
    printf("* timeToString returned %d\n", stat);
    printf("*  time1 as text = \"%s\"\n", textBuffer);
    printf("*  opaque time1  = %016I64X\n", timeData1.t1);

    bufferSize = MAXBUFSIZE;
    stat = fptr_timeToString(hts, timeData1.t2, &bufferSize, textBuffer);
    printf("* timeToString returned %d\n", stat);
    printf("*  time2 as text = \"%s\"\n", textBuffer);
    printf("*  opaque time2  = %016I64X\n", timeData1.t2);

    bufferSize = MAXBUFSIZE;
    stat = fptr_timeToString(hts, timeData1.t3, &bufferSize, textBuffer);
    printf("* timeToString returned %d\n", stat);
    printf("*  time3 as text = \"%s\"\n", textBuffer);
    printf("*  opaque time3  = %016I64X\n", timeData1.t3);

    bufferSize = MAXBUFSIZE;
    stat = fptr_timeToString(hts, timeData1.t4, &bufferSize, textBuffer);
    printf("* timeToString returned %d\n", stat);
    printf("*  time4 as text = \"%s\"\n", textBuffer);
    printf("*  opaque time4  = %016I64X\n", timeData1.t4);

    printf("* Current difference #1 = %f ms\n", (double)currentDiff1 / 10000.0);
    printf("* Current difference #2 = %f ms\n", (double)currentDiff2 / 10000.0);
    printf("* Current window size = %f ms\n", (double)currentWindowSize / 10000.0);
    printf("* Maximum absolute difference = %f ms\n", (double)diffMax / 10000.0);
    printf("* Minimum absolute difference = %f ms\n", (double)diffMin / 10000.0);
    printf("* Maximum difference mean = %f ms\n", (double)diffMeanMax / (double)diffNum / 10000.0);
    printf("* Minimum difference mean = %f ms\n", (double)diffMeanMin / (double)diffNum / 10000.0);
  }

  // Close socket
  stat = closesocket(socketConnection);
  printf("* closesocket returned %d\n", stat);
  if (stat)
  {
    printf("Warning: %s failed to close socket!\n", argv[0]);
  }
  sockLibCleanup();

  // stop the time service
  stat = fptr_stopTimeService(hts);
  printf("* stopTimeService returned %d\n", stat);

  // Free the DLL module.
  if (!FreeLibrary(hinstLib))
  {
    printf("Warning: %s failed to unload DLL!\n", argv[0]);
  }

  // done
  return 0;
}
