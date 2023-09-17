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

// CanClient.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "windows.h"
#include <stdio.h>
#include <conio.h>
#include "vxlapi.h"
#include "../../include/SECANMsgTypes.h"
#define RECEIVE_EVENT_SIZE 1

typedef union
{
  unsigned long datau32;
  unsigned char fromBusu8[4];
} u32u8;

typedef union
{
  short datas16;
  unsigned char fromBusu8[2];
} s16u8;

typedef union
{
  unsigned short datau16;
  unsigned char fromBusu8[2];
} u16u8;

typedef union
{
  unsigned __int64 datau64;
  unsigned char fromBusu8[8];
} u64u8;

unsigned long receiveu32(unsigned char* message, unsigned char startAt)
{
  u32u8 dataUnion;
  for (int i = 0; i < 4; i++)
  {
    dataUnion.fromBusu8[i] = message[startAt + i];
  }
  return dataUnion.datau32;
}

short receives16(unsigned char* message, unsigned char startAt)
{
  s16u8 dataUnion;
  for (int i = 0; i < 2; i++)
  {
    dataUnion.fromBusu8[i] = message[startAt + i];
  }
  return dataUnion.datas16;
}

unsigned short receiveu16(unsigned char* message, unsigned char startAt)
{
  u16u8 dataUnion;
  for (int i = 0; i < 2; i++)
  {
    dataUnion.fromBusu8[i] = message[startAt + i];
  }
  return dataUnion.datau16;
}

__int64 receiveu64(unsigned char* message, unsigned char startAt)
{
  u64u8 dataUnion;
  for (int i = 0; i < 8; i++)
  {
    dataUnion.fromBusu8[i] = message[startAt + i];
  }
  return dataUnion.datau64;
}

void receiveSyncMessage(unsigned char* message)
{
  unsigned long frameNr = receiveu32(message, 0);
  unsigned short timeStamp = receiveu16(message, 4);
  unsigned short estDelay = receiveu16(message, 6);
  printf("FrameNr: %d, TimeStamp: %f (s), EstDelay: %f(s)\n",
         frameNr,
         timeStamp / 10000.0,
         estDelay / 10000.0);
}

void receiveUserTimeStampMessage(unsigned char* message)
{
  __int64 userTimeStamp = receiveu64(message, 0);
  printf("UserTimeStamp: %I64d\n", userTimeStamp);
}

void receiveHeadPositionMessage(unsigned char* message)
{
  short x = receives16(message, 0);
  short y = receives16(message, 2);
  short z = receives16(message, 4);
  short quality = receives16(message, 6);

  printf("HeadPosition: x = %f m, y = %f m,z = %f m, quality = %f\n",
         x / 10000.0,
         y / 10000.0,
         z / 10000.0,
         quality / 10000.0);
}

void receiveHeadRotationMessage(unsigned char* message)
{
  short x = receives16(message, 0);
  short y = receives16(message, 2);
  short z = receives16(message, 4);
  short quality = receives16(message, 6);

  printf("HeadRotation (rodrigues): x = %f, y = %f,z = %f, quality = %f\n",
         x / 10000.0,
         y / 10000.0,
         z / 10000.0,
         quality / 10000.0);
}

void receiveGazeOriginMessage(unsigned char* message)
{
  short x = receives16(message, 0);
  short y = receives16(message, 2);
  short z = receives16(message, 4);
  short quality = receives16(message, 6);

  printf("GazeOrigin: x = %f m, y = %f m,z = %f m, quality = %f\n",
         x / 10000.0,
         y / 10000.0,
         z / 10000.0,
         quality / 10000.0);
}

void receiveGazeDirectionMessage(unsigned char* message)
{
  short x = receives16(message, 0);
  short y = receives16(message, 2);
  short z = receives16(message, 4);
  short quality = receives16(message, 6);

  printf("GazeDirection: x = %f, y = %f,z = %f, quality = %f\n",
         x / 10000.0,
         y / 10000.0,
         z / 10000.0,
         quality / 10000.0);
}

void receiveEyeClosureMessage(unsigned char* message)
{
  short closure = receives16(message, 0);
  short quality = receives16(message, 2);

  printf("EyeClosure: x = %f m, quality = %f\n", closure / 10000.0, quality / 10000.0);
}

void receiveBothEyeClosureMessage(unsigned char* message)
{
  short leftClosure = receives16(message, 0);
  short leftQ = receives16(message, 2);
  short rightClosure = receives16(message, 4);
  short rightQ = receives16(message, 6);

  printf("EyeClosure: Left = %f m, LeftQ = %f,Right = %f m, RightQ = %f\n",
         leftClosure / 10000.0,
         leftQ / 10000.0,
         rightClosure / 10000.0,
         rightQ / 10000.0);
}

void receivePupilDiameterMessage(unsigned char* message)
{
  short pupilDiameter = receives16(message, 0);
  short quality = receives16(message, 2);

  printf("PupilDiameter: x = %f m, quality = %f\n", pupilDiameter / 10000.0, quality / 10000.0);
}

void receiveBothPupilDiameterMessage(unsigned char* message)
{
  short leftPupilDiameter = receives16(message, 0);
  short leftQ = receives16(message, 2);
  short rightPupilDiameter = receives16(message, 4);
  short rightQ = receives16(message, 6);

  printf("Both PupilDiameters: Left = %f m, LeftQ = %f,Right = %f m, RightQ = %f\n",
         leftPupilDiameter / 10000.0,
         leftQ / 10000.0,
         rightPupilDiameter / 10000.0,
         rightQ / 10000.0);
}

void receiveFilteredGazeDirection(unsigned char* message)
{
  short x = receives16(message, 0);
  short y = receives16(message, 2);
  short z = receives16(message, 4);
  short quality = receives16(message, 6);

  printf("FilteredGazeDirection: x = %f, y = %f,z = %f, quality = %f\n",
         x / 10000.0,
         y / 10000.0,
         z / 10000.0,
         quality / 10000.0);
}
void receiveFilteredLeftGazeDirection(unsigned char* message)
{
  short x = receives16(message, 0);
  short y = receives16(message, 2);
  short z = receives16(message, 4);
  short quality = receives16(message, 6);

  printf("FilteredLeftGazeDirection: x = %f, y = %f,z = %f, quality = %f\n",
         x / 10000.0,
         y / 10000.0,
         z / 10000.0,
         quality / 10000.0);
}
void receiveFilteredRightGazeDirection(unsigned char* message)
{
  short x = receives16(message, 0);
  short y = receives16(message, 2);
  short z = receives16(message, 4);
  short quality = receives16(message, 6);

  printf("FilteredRightGazeDirection: x = %f, y = %f,z = %f, quality = %f\n",
         x / 10000.0,
         y / 10000.0,
         z / 10000.0,
         quality / 10000.0);
}
void receiveBlink(unsigned char* message)
{
  unsigned long blink = receiveu32(message, 0);
  printf("Blink: %d\n", blink);
}
void receiveSaccade(unsigned char* message)
{
  unsigned long saccade = receiveu32(message, 0);
  printf("Saccade: %d\n", saccade);
}
void receiveLeftBlinkClosingMidTime(unsigned char* message)
{
  __int64 blink = receiveu64(message, 0);
  printf("Left blink closing mid time: %I64d\n", blink);
}
void receiveLeftBlinkClosingAmplitude(unsigned char* message)
{
  short bca = receives16(message, 0);
  printf("Left blink closing amplitude: %f\n", bca / 10000.0);
}
void receiveLeftBlinkClosingSpeed(unsigned char* message)
{
  short value = receives16(message, 0);
  printf("Left blink closing speed: %f\n", value / 10000.0);
}
void receiveLeftBlinkOpeningMidTime(unsigned char* message)
{
  __int64 value = receiveu64(message, 0);
  printf("Left blink opening mid time: %I64d\n", value);
}
void receiveLeftBlinkOpeningAmplitude(unsigned char* message)
{
  short value = receives16(message, 0);
  printf("Left blink opening amplitude: %f\n", value / 10000.0);
}
void receiveLeftBlinkOpeningSpeed(unsigned char* message)
{
  short value = receives16(message, 0);
  printf("Left blink opening speed: %f\n", value / 10000.0);
}
void receiveRightBlinkClosingMidTime(unsigned char* message)
{
  __int64 value = receiveu64(message, 0);
  printf("Right blink closing mid time: %I64d\n", value);
}
void receiveRightBlinkClosingAmplitude(unsigned char* message)
{
  short bca = receives16(message, 0);
  printf("Right blink closing amplitude: %f\n", bca / 10000.0);
}
void receiveRightBlinkClosingSpeed(unsigned char* message)
{
  short value = receives16(message, 0);
  printf("Right blink closing speed: %f\n", value / 10000.0);
}
void receiveRightBlinkOpeningMidTime(unsigned char* message)
{
  __int64 value = receiveu64(message, 0);
  printf("Right blink opening mid time: %I64d\n", value);
}
void receiveRightBlinkOpeningAmplitude(unsigned char* message)
{
  short value = receives16(message, 0);
  printf("Right blink opening amplitude: %f\n", value / 10000.0);
}
void receiveRightBlinkOpeningSpeed(unsigned char* message)
{
  short value = receives16(message, 0);
  printf("Right blink opening speed: %f\n", value / 10000.0);
}
typedef struct
{
  XLhandle msgEvent;
  XLaccess xlChannelMask;
  XLportHandle xlPortHandle;
  int threadRunning;
  HANDLE threadHandle;

} CANBusInfo;

XLstatus initDriver(CANBusInfo* canInfo, char* appName)
{
  XLstatus xlStatus;

  // ------------------------------------
  // open the driver
  // ------------------------------------
  xlStatus = xlOpenDriver();

  if (XL_SUCCESS != xlStatus)
    return 0;

  unsigned int hwType;
  unsigned int hwIndex;
  unsigned int hwChannel;

  xlStatus = xlGetApplConfig(appName, 0, &hwType, &hwIndex, &hwChannel, XL_BUS_TYPE_CAN);
  if (XL_SUCCESS != xlStatus || XL_HWTYPE_NONE == hwType)
  {
    xlPopupHwConfig(NULL, 0);
    char errorMessage[1024];
    sprintf_s(errorMessage, 1024, "Please assign one CAN channel to Application=\"%s\"", appName);
    //MessageBox(NULL, "Please assign one CAN channel to Application=\"" appName "\"", 0, MB_OK);
    MessageBox(NULL, errorMessage, 0, MB_OK);
    return 0;
  }

  canInfo->xlChannelMask = 0;
  canInfo->xlChannelMask = xlGetChannelMask(hwType, hwIndex, hwChannel);
  if (!canInfo->xlChannelMask)
    return 0;

  canInfo->xlPortHandle = XL_INVALID_PORTHANDLE;
  XLaccess permissionMask = canInfo->xlChannelMask;
  xlStatus = xlOpenPort(&canInfo->xlPortHandle,
                        appName,
                        canInfo->xlChannelMask,
                        &permissionMask,
                        256,
                        XL_INTERFACE_VERSION,
                        XL_BUS_TYPE_CAN);
  if (XL_SUCCESS != xlStatus)
    return 0;
  if (XL_INVALID_PORTHANDLE == canInfo->xlPortHandle)
    return 0;

  if ((XL_SUCCESS == xlStatus) && (XL_INVALID_PORTHANDLE != canInfo->xlPortHandle))
  {
    printf("Connected\n");
  }
  else
  {
    printf("Invalid Port Handle\n");
    xlClosePort(canInfo->xlPortHandle);
    canInfo->xlPortHandle = XL_INVALID_PORTHANDLE;
    xlStatus = XL_ERROR;
  }

  return xlStatus;
}
int receiveMessage(XLevent xlEvent)
{
  switch (xlEvent.tagData.msg.id - SE_CAN_MSG_BASE)
  {
    case SE_CAN_SYNCH:
      receiveSyncMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_USERTIMESTAMP:
      receiveUserTimeStampMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_HEADPOSITION:
      receiveHeadPositionMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_HEADROTATION:
      receiveHeadRotationMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_GAZEORIGIN:
      receiveGazeOriginMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_GAZEDIRECTION:
      receiveGazeDirectionMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_EYECLOSURE:
      receiveEyeClosureMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_BOTHEYECLOSURES:
      receiveBothEyeClosureMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_PUPILDIAMETER:
      receivePupilDiameterMessage(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_BOTHPUPILDIAMETERS:
      receiveBothPupilDiameterMessage(xlEvent.tagData.msg.data);
      break;

    case SE_CAN_FILTEREDGAZEDIRECTION:
      receiveFilteredGazeDirection(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_FILTEREDLEFTGAZEDIRECTION:
      receiveFilteredLeftGazeDirection(xlEvent.tagData.msg.data);
      break;

    case SE_CAN_FILTEREDRIGHTGAZEDIRECTION:
      receiveFilteredRightGazeDirection(xlEvent.tagData.msg.data);
      break;

    case SE_CAN_BLINK:
      receiveBlink(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_SACCADE:
      receiveSaccade(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_LEFTBLINKCLOSINGMIDTIME:
      receiveLeftBlinkClosingMidTime(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_LEFTBLINKCLOSINGAMPLITUDE:
      receiveLeftBlinkClosingAmplitude(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_LEFTBLINKCLOSINGSPEED:
      receiveLeftBlinkClosingSpeed(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_LEFTBLINKOPENINGMIDTIME:
      receiveLeftBlinkOpeningMidTime(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_LEFTBLINKOPENINGAMPLITUDE:
      receiveLeftBlinkOpeningAmplitude(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_LEFTBLINKOPENINGSPEED:
      receiveLeftBlinkOpeningSpeed(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_RIGHTBLINKCLOSINGMIDTIME:
      receiveRightBlinkClosingMidTime(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_RIGHTBLINKCLOSINGAMPLITUDE:
      receiveRightBlinkClosingAmplitude(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_RIGHTBLINKCLOSINGSPEED:
      receiveRightBlinkClosingSpeed(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_RIGHTBLINKOPENINGMIDTIME:
      receiveRightBlinkOpeningMidTime(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_RIGHTBLINKOPENINGAMPLITUDE:
      receiveRightBlinkOpeningAmplitude(xlEvent.tagData.msg.data);
      break;
    case SE_CAN_RIGHTBLINKOPENINGSPEED:
      receiveRightBlinkOpeningSpeed(xlEvent.tagData.msg.data);
      break;
    default:
      printf("Received Unknown Message with id:%x\n", xlEvent.tagData.msg.id);
      return -1;
  }

  return 0;
}
DWORD WINAPI RxThread(LPVOID par);
///////////////////////////////////////////////////////////////////////////

/// createRxThread

/// set the notification and creates the thread.
///
////////////////////////////////////////////////////////////////////////////

XLstatus createRxThread(CANBusInfo* info)
{
  XLstatus xlStatus = XL_ERROR;
  DWORD ThreadId = 0;

  if (info->xlPortHandle != XL_INVALID_PORTHANDLE)
  {
    // Send a event for each Msg!!!
    xlStatus = xlSetNotification(info->xlPortHandle, &info->msgEvent, 1);

    info->threadHandle =
        CreateThread(0, 0x1000, RxThread, (LPVOID)info, CREATE_SUSPENDED, &ThreadId);
  }
  return xlStatus;
}

int main(int argc, char* argv[])
{
  char appName[XL_MAX_LENGTH - 1] = "SeCanClient";
  unsigned int baudRate = 500000;
  CANBusInfo info;
  info.threadRunning = 0;

  initDriver(&info, appName);
  createRxThread(&info);

  XLstatus xlStatus =
      xlActivateChannel(info.xlPortHandle, info.xlChannelMask, XL_BUS_TYPE_CAN, XL_ACTIVATE_NONE);
  info.threadRunning = 1;
  ResumeThread(info.threadHandle);

  while (!_kbhit())
    Sleep(100);
  ;
  ///Kill thread
  info.threadRunning = 0;

  return 0;
}

DWORD WINAPI RxThread(LPVOID par)
{
  XLstatus xlStatus;

  unsigned int msgsrx = RECEIVE_EVENT_SIZE;
  XLevent xlEvent;

  CANBusInfo* info = (CANBusInfo*)par;

  while (true)
  {
    if (!info->threadRunning)
    {
      break;
    }

    WaitForSingleObject(info->msgEvent, 100);

    xlStatus = XL_SUCCESS;

    while (!xlStatus)
    {
      msgsrx = RECEIVE_EVENT_SIZE;
      xlStatus = xlReceive(info->xlPortHandle, &msgsrx, &xlEvent);

      if (xlStatus != XL_ERR_QUEUE_IS_EMPTY)
      {
        if (xlEvent.tag == XL_RECEIVE_MSG)
        {
          receiveMessage(xlEvent);
        }
      }
    }
  }
  return NO_ERROR;
}
