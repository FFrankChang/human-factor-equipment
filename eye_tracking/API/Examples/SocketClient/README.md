# SocketClient

SocketClient is a C++ example implementation of how to receive output data from
the Smart Eye system via a network socket. Parts of this code can be copied
into your own client or used as a starting point to build your client from.

A pre-built SocketClient.exe can be found in the `API\Examples\bin` directory
of the Smart Eye software installation.

The remainder of this file first provides an overview of the SocketClient
implementation, then documents how to setup and build the project.


## Implementation

This section will give a brief overview of the SocketClient implementation and
outline API headers used by the SocketClient that may be useful for
implementing your own socket receiver.

The SocketClient implementation uses an infinite loop that:

1. Waits for a packet to arrive.
2. Checks for errors.
3. Checks packet type.
4. Interprets contents of packet (print content and call user function).
5. Frees packet, and return to waiting for packets (i.e. step 1).


The SocketClient example uses a couple of important header files from the
`API\include` folder:

* `SEDataTypes.h` - Contains definitions of data types custom to the Smart
  Eye System.
* `SEOutputDataIds.h`, `SEOutputData.h` - Contains definitions of the different
  data items that the Smart Eye System may produce (for example
  *SEGazeDirection*, *SERealTimeClock* and *SEHeadPosition*), as well as a
  lookup table to look up data type and literal name based on the data id.
* `SEPacketApi.h` - Contains functions to read a packet and convert it to the
  types found in `SEDataTypes.h`.


**Note**: Data on the socket is sent in network byte order. I.e. on an Intel
based system the byte order needs to be reversed in order to interpret the
data correctly. The SocketClient also illustrates this.


## Build Instructions

This section first lists prerequisites for building the SocketClient project,
then provides a short guide for building the project solution via CMake.

### Build Prerequisites

* [CMake](https://cmake.org/) > 3.10
* Visual Studio 2019

### Setup and Building

Start by copying this project to a location on your computer where you
have both read and write permissions. Generally the Program Files
directory is only writeable by applications running as admin.

After copying the project you should have a folder structure that looks
like this:

```.
/
  - SocketClient/
    - src/
      - SocketClient.cpp
    - CMakeLists.txt
  - build.ps1
  - README.md (this file)
```

Next, update the `SocketClient_SEP_API_INCLUDE_DIR` CMake variable in
`SocketClient/CMakeLists.txt` so that it contains the path of the
`API\Examples\bin` directory of your Smart Eye Pro installation. If Smart Eye
Pro was installed in the default location this should only require replacing
`X.Y` with the actual Smart Eye Pro version.

It should now be possible to build the example project by running the
build.ps1 file from a PowerShell prompt:

```
> ./build.ps1
```

The build.ps1 script uses CMake to generate a Visual Studio Project in a new
directory `build`, then builds the project in Release.

The resulting
`SocketClient.exe` can be found in the `build\Release` directory.

The generated Visual Studio project is found in `build\SocketClient.sln` and
can now be opened, modified, and built with Visual Studio.
