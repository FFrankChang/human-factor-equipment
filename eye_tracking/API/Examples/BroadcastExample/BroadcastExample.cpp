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

/* Broadcast Example

  Simple broadcast example based on the Low level API provided
  by Basler.

  It will look up connected devices and set up a stream grabber
  for each GigE camera in monitoring(broadcast) mode.

  The grabbed video feed will be displayed for each camera
  in a separate window.

*/

#include "stdafx.h"
#include <pylon/PylonIncludes.h>
#include <pylon/gige/BaslerGigECamera.h>

#include <pylon/PylonGUI.h>
#include <map>

// Number of images to be grabbed.
static const int NUM_GRABS = 1000;

struct MyContext
{
  // Define some application specific context information here.
};

#define MAX_NUM_BUFFERS 10
struct BroadcastDeviceContainer
{
  Pylon::IPylonDevice* device;
  Pylon::CBaslerGigECamera camera;
  Pylon::CBaslerGigECamera::StreamGrabber_t streamGrabber;

  unsigned char* buffers[MAX_NUM_BUFFERS];
  MyContext context[MAX_NUM_BUFFERS];
  Pylon::StreamBufferHandle handles[MAX_NUM_BUFFERS];
}; // Container for objects associated to one device.

static void ProcessImage(int windowId, Pylon::GrabResult result)
{
  Pylon::CGrabResultImage resultImage(result, true);
  Pylon::DisplayImage(windowId, resultImage);
}

int main()
{
  // The exit code of the sample application.
  int exitCode = 0;

  // Specify port for each UserDefinedName.
  // This maps to DeviceUserID specified in Pylon IP configurator.
  std::map<std::string, int> customBroadcastPorts;
  customBroadcastPorts["1"] = 49154;
  customBroadcastPorts["2"] = 49154;

  // Before using any pylon methods, the pylon runtime must be initialized.
  Pylon::PylonInitialize();

  Pylon::ITransportLayer* transportLayer = nullptr;
  Pylon::DeviceInfoList_t devices;

  // Create transport layer object.
  Pylon::CTlFactory& transportLayerFactory = Pylon::CTlFactory::GetInstance();
  transportLayer = transportLayerFactory.CreateTl(Pylon::CBaslerGigECamera::DeviceClass());

  if (transportLayer == nullptr)
  {
    std::cerr << "Error: Could not create Pylon transport layer." << std::endl;
    return 1;
  }

  // Look up available devices.
  int numCamerasAvailable = transportLayer->EnumerateDevices(devices);
  std::cout << "NumCamerasAvailable: " << numCamerasAvailable << std::endl;

  if (numCamerasAvailable == 0)
  {
    std::cout
        << "No camera available. Make sure cameras are connected and that they are configured "
           "properly."
        << std::endl;
    exitCode = 1;
    return exitCode;
  }

  try
  {
    std::vector<BroadcastDeviceContainer> broadcastDevices(numCamerasAvailable);
    for (int i = 0; i < numCamerasAvailable; i++)
    {
      // Create device object.
      broadcastDevices[i].device = transportLayer->CreateDevice(devices[i]);
      Pylon::String_t userDefinedName =
          broadcastDevices[i].device->GetDeviceInfo().GetUserDefinedName();
      Pylon::String_t modelName = broadcastDevices[i].device->GetDeviceInfo().GetModelName();
      Pylon::String_t serialNumber = broadcastDevices[i].device->GetDeviceInfo().GetSerialNumber();
      std::cout << "First camera - UserDefinedName: " << userDefinedName << " Model: " << modelName
                << " Serial: " << serialNumber << std::endl;

      // Attach camera object to the device.
      broadcastDevices[i].camera.Attach(broadcastDevices[i].device, true);
      std::cout << "Camera " << userDefinedName << " is attached!" << std::endl;

      // Open with access mode Stream to specify
      // that we want to run in monitor mode.
      broadcastDevices[i].camera.Open(Pylon::Stream);
      std::cout << "Camera " << userDefinedName << " is open!" << std::endl;

      // Attach stream grabber.
      broadcastDevices[i].streamGrabber.Attach(broadcastDevices[i].camera.GetStreamGrabber(0));
      std::cout << "Stream grabber for camera " << userDefinedName << " is attached!" << std::endl;

      // Specify the transmission type as broadcast and provide port.
      broadcastDevices[i].streamGrabber.TransmissionType =
          Basler_GigEStreamParams::TransmissionType_SubnetDirectedBroadcast;
      int port;

      if (customBroadcastPorts.count(userDefinedName.c_str()) > 0)
      { // If the UserDefinedName is found in customBroadcastPorts.
        port = customBroadcastPorts[userDefinedName.c_str()];
      }
      else
      { // Otherwise use default port.
        port = 49154;
      }

      broadcastDevices[i].streamGrabber.DestinationPort = port;

      // Open stream grabber.
      broadcastDevices[i].streamGrabber.Open();
      std::cout << "Stream grabber for camera " << userDefinedName << " is open!" << std::endl;

      // Parameterize the stream grabber.
      const int bufferSize = (int)broadcastDevices[i].camera.PayloadSize();
      broadcastDevices[i].streamGrabber.MaxBufferSize = bufferSize;
      broadcastDevices[i].streamGrabber.MaxNumBuffer = MAX_NUM_BUFFERS;
      broadcastDevices[i].streamGrabber.PrepareGrab();

      // Allocate and register image buffers, put them into the
      // grabber's input queue.
      for (int k = 0; k < MAX_NUM_BUFFERS; ++k)
      {
        broadcastDevices[i].buffers[k] = new unsigned char[bufferSize];
        broadcastDevices[i].handles[k] = broadcastDevices[i].streamGrabber.RegisterBuffer(
            broadcastDevices[i].buffers[k], bufferSize);
        broadcastDevices[i].streamGrabber.QueueBuffer(broadcastDevices[i].handles[k],
                                                      &broadcastDevices[i].context[k]);
      }
    }

    // Grab and process images.
    Pylon::GrabResult result;
    for (int i = 0; i < NUM_GRABS; ++i)
    {
      for (int k = 0; k < numCamerasAvailable; k++)
      {
        // Wait for the grabbed image with a timeout of 3 seconds.
        if (broadcastDevices[k].streamGrabber.GetWaitObject().Wait(3000))
        {
          // Get an item from the grabber's output queue.
          if (!broadcastDevices[k].streamGrabber.RetrieveResult(result))
          {
            std::cerr << "Failed to retrieve an item from the output queue" << std::endl;
            break;
          }
          if (result.Succeeded())
          {
            // Grabbing was successful. Process the image.
            ProcessImage(k, result);
          }
          else
          {
            std::cerr << "Grab failed: " << result.GetErrorDescription() << std::endl;
            break;
          }
          // Requeue the buffer.
          if (i + MAX_NUM_BUFFERS < NUM_GRABS)
            broadcastDevices[k].streamGrabber.QueueBuffer(result.Handle(), result.Context());
        }
        else
        {
          std::cerr << "timeout occurred when waiting for a grabbed image" << std::endl;
          break;
        }
      }
    }

    // Finished. Stop grabbing and do clean-up.
    // Flush the input queue, grabbing may have failed.
    for (int k = 0; k < numCamerasAvailable; k++)
    {
      broadcastDevices[k].streamGrabber.CancelGrab();

      // Consume all items from the output queue.
      while (broadcastDevices[k].streamGrabber.GetWaitObject().Wait(0))
      {
        broadcastDevices[k].streamGrabber.RetrieveResult(result);
        if (result.Status() == Pylon::Canceled)
          std::cout << "Got canceled buffer camera: " << k << std::endl;
      }

      // Deregister and free buffers.
      for (int i = 0; i < MAX_NUM_BUFFERS; ++i)
      {
        broadcastDevices[k].streamGrabber.DeregisterBuffer(broadcastDevices[k].handles[i]);
        delete[] broadcastDevices[k].buffers[i];
      }

      // Clean up.
      broadcastDevices[k].streamGrabber.FinishGrab();
      broadcastDevices[k].streamGrabber.Close();

      broadcastDevices[k].camera.Close();
    }
    transportLayerFactory.ReleaseTl(transportLayer);
  }
  catch (const Pylon::GenericException& e)
  {
    // Error handling.
    std::cerr << "An exception occurred." << std::endl << e.GetDescription() << std::endl;
    exitCode = 2;
  }

  if (exitCode == 0)
  {
    std::cout << "Grabbing was succesful, exiting application." << std::endl;
  }

  // Releases all pylon resources.
  Pylon::PylonTerminate();

  return exitCode;
}
