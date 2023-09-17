# RPCExample

RPCExample is an example project showing how to use the `SeJsonRpc.dll`
to communicate with the Smart Eye Pro JSON-RPC. A pre-built
RPCExample.exe can be found in the `API\Examples\bin` directory of the
Smart Eye Pro installation.

The RPCExample.exe contains multiple examples described below. Each example
can be run by supplying the example name as an argument to RPCExample.exe.

The **Simple** example does the following:
1. Tries to connect to the Smart Eye Pro JSON-RPC on localhost.
2. Calls the `GetProductName` RPC method and prints the *json encoded*
   response.
3. Disconnects.

The **TrackAndRecord** example does the following:
1. Tries to connect to the Smart Eye Pro JSON-RPC on localhost.
2. Sets which paths the log and recording should be stored to.
3. Subscribes to notifications.
4. Starts recording, tracking and logging.
5. Sleeps for a few seconds.
6. Stops recording, tracking and logging.

The **GetSetProfile** example does the following:
1. Tries to connect to the Smart Eye Pro JSON-RPC on localhost.
2. Sets path to where the profile file should be stored.
3. Starts tracking to build up a profile.
4. Sleeps for two seconds.
5. Stops tracking.
6. Gets the profile from SEP.
7. Parses out the profile form the json response.
8. Saves the profile to file.
9. Clears profile in SEP.
10. Loads profile string from file.
11. Sets profile in SEP to the loaded file.

Extending the example programs to call additional method should be straight
forward, please refer to the Programmer's Guide for a list of available RPC
methods. The included json.hpp in API/Include can be used for parsing the JSON
responses from the RPC.

## Prerequisites

* [CMake](https://cmake.org/) > 3.10
* Visual Studio 2019


## Setup and Building

Start by copying this project to a location on your computer where you
have both read and write permissions. Generally the Program Files
directory is only writeable by applications running as admin.

After copying the project you should have a folder structure that looks
like this:

```.
/
  - RPCExample/
    - src/
      - ...
    - inc/
      - ...
    - CMakeLists.txt
  - build.ps1
  - README.md (this file)
```

Next, update the `RPCExample_SEP_BIN_DIR` and `RPCExample_SEP_API_INCLUDE_DIR`
CMake variables in `RPCExample/CMakeLists.txt` so that they contain the paths to
the directories of your Smart Eye Pro installation. If Smart Eye Pro was
installed in the default location this should only require replacing `X.Y` with
the actual Smart Eye Pro version.

It should now be possible to build the example project by running the
build.ps1 file from a PowerShell prompt:

```
> ./build.ps1
```

The build.ps1 script uses CMake to generate a Visual Studio Project in a new
directory `build`, then builds the project in Release. The resulting
`RPCExample.exe` can be found in the `build\Release` directory. The generated
project is found in `build\RPCExample.sln` and can now be opened and built in
Visual Studio.
