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

#include <SEDataTypes.h>
#include <SEOutputDataIds.h>
#pragma warning(push)
#pragma warning(disable : 4505) // C4505: unreferenced local function has been removed.
#include <SEPacketAPI.h>
#pragma warning(pop)

#pragma comment(lib, "Ws2_32.lib")
#include <winsock2.h>
#include <ws2tcpip.h>
#include <algorithm>
#include <iostream>
#include <ctype.h>

//----------------------------------------------------------------------------//

// Look below for the main function

const int defaultPortUDP = 5001; /// This is the port number you choose in Smart Eye Pro
const int defaultPortTCP = 5002; /// This is the port number you choose in Smart Eye Pro
const char defaultHost[] =
    "127.0.0.1"; /// Modify this to IP-address of server if not same as client

/// This is an example function of different ways to handle packet data
/// Modify this function or write your own handler that is called from main function
///
/// pPacket    - Pointer to beginning of the packet buffer.
/// packetType - Type of packet found in the packet header.
void userPacketHandler(char* pPacket, const SEu16& packetType)
{
  // This function only cares about packets of type 4
  if (packetType != 4)
    return;

  std::cout << "User packet handler function...\n";

  // Example 1:
  // Look up subpacket of id = SEHeadPosition
  SEPoint3D headPosition;
  if (findDataInPacket(SEHeadPosition, pPacket, headPosition))
    std::cout << "Headposition [" << headPosition.x << ", " << headPosition.y << ", "
              << headPosition.z << "]\n";
  else
    std::cout << "Did not find SEHeadPosition in data, check packet contents in Smart Eye Pro\n";

  // Example 2:
  // Look up subpacket of id = SEEyelidOpening
  SEf64 eyelidOpening;
  if (findDataInPacket(SEEyelidOpening, pPacket, eyelidOpening))
    std::cout << "Eyelid opening : " << eyelidOpening << "\n";
  else
    std::cout << "Did not find SEEyelidOpening in data, check packet contents in Smart Eye Pro\n";

  // Example 3:
  // Get closest intersection point
  SEWorldIntersectionStruct worldIntersection;
  if (findDataInPacket(SEClosestWorldIntersection, pPacket, worldIntersection))
  {
    if (strcmp(worldIntersection.objectName.ptr, "Screen.Surface") != -1)
    {
      double x = worldIntersection.objectPoint.x;
      double y = worldIntersection.objectPoint.y;
      std::cout << "Screen.Surface intersected at [" << x << ", " << y << "]\n";
    }
  }

  // Example 4:
  // Get all closest intersection point
  SEWorldIntersectionStruct my_worldIntersection[10];
  SEu16 numberOfIntersections;
  if (findDataInPacket(
          SEAllWorldIntersections, pPacket, my_worldIntersection, numberOfIntersections))
  {
    numberOfIntersections = numberOfIntersections < 10 ? numberOfIntersections : 10;
    for (int i = 0; i < numberOfIntersections; i++)
    {
      std::cout << "Intersection " << i << " ";
      std::cout << my_worldIntersection[i].objectName.ptr;
      double x = worldIntersection.objectPoint.x;
      double y = worldIntersection.objectPoint.y;
      double z = worldIntersection.objectPoint.z;
      std::cout << " intersected at [" << x << ", " << y << ", " << z << "]\n";
    }
  }

  std::cout << "\n\n";
}

SOCKET connectToSocket(const char* hostname, unsigned short portnum)
{
  int err;
  addrinfo* addrResult;
  addrinfo addrHints{0};
  addrHints.ai_family = AF_INET;
  addrHints.ai_socktype = SOCK_STREAM;

  // Lookup address by hostname.
  int sockFamily = AF_UNSPEC;
  sockaddr_in sockAddr{0};
  bool sockAddrOk = false;

  err = getaddrinfo(hostname, NULL, &addrHints, &addrResult);
  if (err != 0)
  {
    std::cerr << "connectToSocket: Error getaddrinfo() = " << err << std::endl;
    return INVALID_SOCKET;
  }

  for (addrinfo* p = addrResult; p != nullptr; p = p->ai_next)
  {
    if (p->ai_family == AF_INET && p->ai_socktype == SOCK_STREAM)
    {
      sockFamily = p->ai_family;
      sockAddr = *((sockaddr_in*)p->ai_addr);
      sockAddrOk = true;
      break;
    }
  }
  freeaddrinfo(addrResult);

  if (!sockAddrOk)
  {
    std::cerr << "connectToSocket: Error could not translate hostname to address." << std::endl;
    return INVALID_SOCKET;
  }

  // Create socket
  SOCKET s = socket(sockFamily, SOCK_STREAM, 0);
  if (s == INVALID_SOCKET)
  {
    err = WSAGetLastError();
    std::cerr << "connectToSocket: Error socket() = " << err << std::endl;
    return INVALID_SOCKET;
  }

  // Try to connect to the specified socket
  sockAddr.sin_port = htons((u_short)portnum);
  int result = connect(s, (struct sockaddr*)&sockAddr, sizeof sockAddr);
  if (result == SOCKET_ERROR)
  {
    err = WSAGetLastError();
    std::cerr << "connectToSocket: Error connect() = " << err << std::endl;
    closesocket(s);
    return INVALID_SOCKET;
  }
  return s;
}

/// This function initialized a socket connection with the given
/// host and port
SOCKET bindToSocket(unsigned short portnum)
{
  // Prepare socket address
  struct sockaddr_in sockAddr;
  memset(&sockAddr, 0, sizeof(sockAddr));
  sockAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  sockAddr.sin_family = AF_INET;
  sockAddr.sin_port = htons((u_short)portnum);

  // Create socket
  SOCKET s = socket(AF_INET, SOCK_DGRAM, 0);
  if (s == INVALID_SOCKET)
  {
    int err = WSAGetLastError();
    std::cerr << "bindToSocket: Error socket() = " << err << std::endl;
    return INVALID_SOCKET;
  }

  // Try to bind to the specified socket
  int result = bind(s, (struct sockaddr*)&sockAddr, sizeof sockAddr);
  if (result == SOCKET_ERROR)
  {
    int err = WSAGetLastError();
    std::cerr << "bindToSocket: Error bind() = " << err << std::endl;
    closesocket(s);
    return INVALID_SOCKET;
  }
  return s;
}

void printUsage()
{
  std::cout << "\nSocketClient\n(C) Copyright 2009 Smart Eye AB\n\n";
  std::cout << "Usage: SocketClient UDP|TCP <port> <hostname>\n\n";

  std::cout << "UDP or TCP has to be specified.\n";
  std::cout << "Default port for UDP is 5001 and default port for TCP is 5002\n";
  std::cout << "Default host is 127.0.0.1\n";
}

#if defined(_WIN32)
#define sockLibInit() initWinSock()
#define sockLibCleanup() WSACleanup()
#else
#define sockLibInit()
#define sockLibCleanup()
#endif

#if defined(_WIN32)
int initWinSock(void)
{
  // Initialize the Windows socket library
  WSADATA info;
  if (WSAStartup(0x0002, &info) == SOCKET_ERROR)
  {
    std::cerr << "Could not initialize socket library.\n";
    exit(1);
  }
  return 0;
}
#endif

static int recvPacketUDP(SOCKET conn, char* buf, int len)
{
  // We expect to get the full SEPacket in a single UDP datagram.
  return recv(conn, buf, len, 0);
}

static int recvPacketTCP(SOCKET conn, char* buf, int len)
{
  // TCP is stream based so we cannot assume that a single recv will read the
  // full SEPacket.
  int bytesReceived = 0;
  int n = 0;
  while (bytesReceived < len)
  {
    n = recv(conn, buf + bytesReceived, len - bytesReceived, 0);
    if (n == SOCKET_ERROR)
    {
      return SOCKET_ERROR;
    }
    else if (n == 0)
    {
      // Connection was closed.
      break;
    }
    bytesReceived += n;
  }
  return bytesReceived;
}

/// The following is an example of connecting to a socket and receiving packets
/// Feel free to copy parts of this code into your own client or use this code
/// to build your client from.
int main(int argc, char* argv[])
{
  if (argc == 1)
  {
    printUsage();
    return 0;
  }

  int arg = 1;
  bool useUDP = true;
  // Check for UDP/TCP flag
  if (strncmp(argv[arg], "TCP", 3) == 0 || strncmp(argv[arg], "tcp", 3) == 0)
    useUDP = false;
  else if (strncmp(argv[arg], "UDP", 3) != 0 && strncmp(argv[arg], "udp", 3) != 0)
  {
    printUsage();
    return 0;
  }
  arg++;

  sockLibInit();

  // Get server name and port number, either default or from command prompt
  SOCKET socketConnection = INVALID_SOCKET;
  unsigned short portNo = 0;
  if (useUDP)
  {
    portNo = static_cast<unsigned short>(argc > arg ? atoi(argv[arg]) : defaultPortUDP);
    arg++;
    std::cout << "Listening for UDP data on port " << portNo << "\n";
    socketConnection = bindToSocket(portNo);
  }
  else
  {
    portNo = static_cast<unsigned short>(argc > arg ? atoi(argv[arg]) : defaultPortTCP);
    arg++;
    const char* Name =
        argc > arg
            ? argv[arg]
            : defaultHost; // optional command line parameter is tracker host name (default localhost)

    std::cout << "Trying to connect to " << Name << " on port " << portNo << "\n";
    socketConnection = connectToSocket(Name, portNo);
  }

  if (socketConnection == INVALID_SOCKET)
  {
    std::cerr << "Could not connect to server\n";
    sockLibCleanup();
    return 1;
  }

  // Infinite loop that handles packet
  // 1. Wait for packet
  // 2. Check for errors
  // 3. Check packet type
  // 4. Interpret contents of packet(print content and call user function)
  // 5. Free packet and return to waiting for packets
  while (true)
  {
    // Wait for packet arrival
    // Do this by peeking for packet of size packet header, which is the smallest packet that may arrive
    SEPacketHeader tempPacketHeader;

    int received =
        recv(socketConnection, (char*)&tempPacketHeader, sizeof(SEPacketHeader), MSG_PEEK);

    // Something did arrive, socket is blocking so it would not return until packet arrived
    // Check that packet at least is the size of a packet header

#if defined(_WIN32)
    if (received == -1)
    {
      int err = WSAGetLastError();
      if (err == 10040)
      {
        //winsock reports error when receive buffer is smaller than packet, but fills the full buffer
        received = sizeof(SEPacketHeader);
      }
    }
#endif
    if (received != (int)sizeof(SEPacketHeader))
    {
      if (received == 0)
        std::cerr << "Socket connection was closet by server\n";
      else
      {
        int err = WSAGetLastError();
        std::cerr << "Communication failure, error = " << err << "\n";
      }

      sockLibCleanup();
      closesocket(socketConnection);
      return 1;
    }

    // Interpret packet header
    // readValue function handles the reversed byte order and copies data into packet header
    int pos = 0;

    SEPacketHeader packetHeader;
    readValue(packetHeader, (char*)&tempPacketHeader, pos);
    int packetSize = sizeof(SEPacketHeader) +
                     packetHeader.length; // header.length does not include size of header

    // Allocate memory space for packet to be received
    char* pPacket = (char*)malloc(packetSize);

    // Receive the packet from stream
    if (useUDP)
    {
      received = recvPacketUDP(socketConnection, pPacket, packetSize);
    }
    else
    {
      received = recvPacketTCP(socketConnection, pPacket, packetSize);
    }
    if (received != packetSize)
    {
      int err;
      err = WSAGetLastError();
      std::cerr << "Communication failure, error = " << err << "\n";
      sockLibCleanup();
      return 1;
    }

    // Print some general packet information
    std::cout << "Packet type = " << packetHeader.packetType << ", Total size = " << packetSize
              << " (Header size = " << sizeof(SEPacketHeader)
              << " + Data size = " << packetHeader.length << ")\n";

    // Print packet contents
    printPacketContents(pPacket, packetHeader.packetType);

    // Call user handler function with new packet
    userPacketHandler(pPacket, packetHeader.packetType);

    // Add other handler functions here if you like

    // Free the memory allocated for the packet
    free(pPacket);

  } // One iteration of infinite loop ends here

  return 0;
}
