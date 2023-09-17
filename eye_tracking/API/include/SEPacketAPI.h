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
#include <algorithm>

template <class T>
static void ReverseByteOrder(T& value)
{
  unsigned char* p = reinterpret_cast<unsigned char*>(&value);
  std::reverse(p, p + sizeof(value));
}

template <class T>
void readValue(T& value, const char* data, int& pos)
{
  memcpy(&value, &(data[pos]), sizeof(value));
  ReverseByteOrder(value);
  pos += sizeof(value);
}

static void readValue(SEPoint2D& value, const char* data, int& pos)
{
  readValue(value.x, data, pos);
  readValue(value.y, data, pos);
}

static void readValue(SEVect2D& value, const char* data, int& pos)
{
  readValue(value.x, data, pos);
  readValue(value.y, data, pos);
}

static void readValue(SEPoint3D& value, const char* data, int& pos)
{
  readValue(value.x, data, pos);
  readValue(value.y, data, pos);
  readValue(value.z, data, pos);
}

static void readValue(SEVect3D& value, const char* data, int& pos)
{
  readValue(value.x, data, pos);
  readValue(value.y, data, pos);
  readValue(value.z, data, pos);
}

static void readValue(SEQuaternion& value, const char* data, int& pos)
{
  readValue(value.w, data, pos);
  readValue(value.x, data, pos);
  readValue(value.y, data, pos);
  readValue(value.z, data, pos);
}

static void readValue(SEUserMarkerStruct& value, const char* data, int& pos)
{
  readValue(value.error, data, pos);
  readValue(value.cameraClock, data, pos);
  readValue(value.cameraIdx, data, pos);
  readValue(value.data, data, pos);
}

static void readValue(SEString& value, const char* data, int& pos)
{
  readValue(value.size, data, pos);
  int i = 0;
  for (i = 0; i < value.size; i++)
  {
    readValue(value.ptr[i], data, pos);
  }
  value.ptr[i] = '\0';
}

static void readValue(SEWorldIntersectionStruct value[],
                      SEu16& numberOfIntersections,
                      const char* data,
                      int& pos)
{
  readValue(numberOfIntersections, data, pos);
  for (int i = 0; i < numberOfIntersections; i++)
  {
    readValue(value[i].worldPoint, data, pos);
    readValue(value[i].objectPoint, data, pos);
    readValue(value[i].objectName, data, pos);
  }
}

static void readValue(SEWorldIntersectionStruct& value, const char* data, int& pos)
{
  SEu16 numberOfIntersections;
  readValue(numberOfIntersections, data, pos);
  if (numberOfIntersections > 0)
  {
    readValue(value.worldPoint, data, pos);
    readValue(value.objectPoint, data, pos);
    readValue(value.objectName, data, pos);
  }
  else
  {
    *value.objectName.ptr = 0;
    value.objectName.size = 0;
  }
}

static void readValue(SESubPacketHeader& value, const char* data, int& pos)
{
  readValue(value.id, data, pos);
  readValue(value.length, data, pos);
}

static void readValue(SEPacketHeader& value, const char* data, int& pos)
{
  readValue(value.syncId, data, pos);
  readValue(value.packetType, data, pos);
  readValue(value.length, data, pos);
}

void printTypes(SEType type, char* data, int& pos)
{
  switch (type)
  {
    case SEType_u8:
      SEu8 my_u8;
      readValue(my_u8, data, pos);
      std::cout << static_cast<int>(my_u8);
      break;
    case SEType_u16:
      SEu16 my_u16;
      readValue(my_u16, data, pos);
      std::cout << my_u16;
      break;
    case SEType_u32:
      SEu32 my_u32;
      readValue(my_u32, data, pos);
      std::cout << my_u32;
      break;
    case SEType_u64:
      SEu64 my_u64;
      readValue(my_u64, data, pos);
      std::cout << my_u64;
      break;
    case SEType_f64:
      SEf64 my_float;
      readValue(my_float, data, pos);
      std::cout << my_float;
      break;
    case SEType_Point2D:
      SEPoint2D my_Point2D;
      readValue(my_Point2D, data, pos);
      std::cout << my_Point2D.x << "\t" << my_Point2D.y;
      break;
    case SEType_Point3D:
      SEPoint3D my_Point3D;
      readValue(my_Point3D, data, pos);
      std::cout << my_Point3D.x << "\t" << my_Point3D.y << "\t" << my_Point3D.z;
      break;
    case SEType_Vect3D:
      SEVect3D my_Vect3D;
      readValue(my_Vect3D, data, pos);
      std::cout << my_Vect3D.x << "\t" << my_Vect3D.y << "\t" << my_Vect3D.z;
      break;
    case SEType_Quaternion:
      SEQuaternion my_Quaternion;
      readValue(my_Quaternion, data, pos);
      std::cout << my_Quaternion.w << "\t" << my_Quaternion.x << "\t" << my_Quaternion.y << "\t"
                << my_Quaternion.z;
      break;
    case SEType_UserMarker:
    {
      SEu16 markerExists;
      readValue(markerExists, data, pos);
      if (markerExists)
      {
        SEUserMarkerStruct my_UserMarker{};
        readValue(my_UserMarker, data, pos);
        std::cout << static_cast<int>(my_UserMarker.error) << "\t" << my_UserMarker.cameraClock
                  << "\t" << static_cast<int>(my_UserMarker.cameraIdx) << "\t"
                  << my_UserMarker.data;
      }
    }
    break;

    // Worldintersections
    // There are actually two different types, WorldIntersection (0x40/41) and
    // WorldIntersections (0x42/43). Note the singular/plural forms.
    // Their binary implementation however, is exactly the same. The only difference
    // is that WorldIntersection may contain exacly zero or one intersection, while
    // WorldIntersections may have more.
    case SEType_WorldIntersection:
    case SEType_WorldIntersections:
    {
      SEWorldIntersectionStruct my_worldIntersection[10];
      SEu16 numberOfIntersections;
      readValue(my_worldIntersection, numberOfIntersections, data, pos);
      numberOfIntersections = numberOfIntersections < 10 ? numberOfIntersections : 10;
      for (int i = 0; i < numberOfIntersections; i++)
      {
        std::cout << "\nIntersection " << i << "\n";
        std::cout << "\t" << my_worldIntersection[i].worldPoint.x << " "
                  << my_worldIntersection[i].worldPoint.y << " "
                  << my_worldIntersection[i].worldPoint.z << "\n";
        std::cout << "\t" << my_worldIntersection[i].objectPoint.x << " "
                  << my_worldIntersection[i].objectPoint.y << " "
                  << my_worldIntersection[i].objectPoint.z << "\n";
        std::cout << "\t" << my_worldIntersection[i].objectName.ptr;
      }
    }

    break;

    case SEType_String:
      SEString str;
      readValue(str, data, pos);

      std::cout << str.ptr;

      break;

    case SEType_Vector:
      SEu16 nrOfElements;
      readValue(nrOfElements, data, pos);
      for (int i = 0; i < nrOfElements; i++)
      {
        SEu16 subId;
        readValue(subId, data, pos);
        printTypes((SEType)subId, data, pos);
      }

      break;
    default:
      pos = 0;
      break;
  }
  std::cout << "\n";
}

/// Print function for generic packets of type 4
/// Loops throuh the contents of the packet and prints the data
int printSmartEyePacket4(char* pPacket)
{
  int pos = 0;
  SEPacketHeader packetHeader;
  readValue(packetHeader, pPacket, pos);

  int packetSize =
      sizeof(SEPacketHeader) + packetHeader.length; // header.length does not include size of header

  // Loop over all subpackets in packet
  while (pos < packetSize)
  {
    // Read one subpacket header from received packet
    SESubPacketHeader subPacketHeader;
    readValue(subPacketHeader, pPacket, pos);

    // Look up type from packetId
    // This is done by looking up the data id in OutputDataList
    // listIdx will point out the correct list item if found
    int listIdx = 0;
    for (listIdx = 0; OutputDataList[listIdx].numericalDataId != 0 &&
                      OutputDataList[listIdx].numericalDataId != subPacketHeader.id;
         listIdx++)
      ;

    // Was the data id found in our list of known data ids?
    if (OutputDataList[listIdx].numericalDataId != 0)
    {
      // Print id of this data item
      std::cout << OutputDataList[listIdx].dataId << "\t\t";

      // Iterpret data depending on type
      printTypes(OutputDataList[listIdx].typeId, pPacket, pos);
    }
    else
    {
      // we have been sent data that we do not know anything about, probably because it was sent by a more recent program version
      std::cout << "Unknown subpacket with id = " << subPacketHeader.id
                << " and data length = " << subPacketHeader.length << "\n";
      pos += subPacketHeader.length;
    }
  }
  std::cout << "\n";

  return 0;
}

/// Prints content of all types of packet formats
void printPacketContents(char* pPacket, const SEu16& packetType)
{
  switch (packetType)
  {
    case 4:
    { // Custom packet (type = 4)

      // This is the recommended packet to use with Smart Eye 3.0 and above
      printSmartEyePacket4(pPacket);
      break;
    }
    default:
    {
      printf("Trying to print unknown packet type: %d\n", packetType);
      break;
    }
  }
}

/// Looks up data with the given id in the packet
/// Returns true if data was found, false otherwise
/// Note: This function may not be used for SEAllWorldIntersections (note plural), use function below instead
template <class T>
bool findDataInPacket(const unsigned int& numericalId, const char* pPacket, T& value)
{
  int pos = 0;
  SEPacketHeader packetHeader;
  readValue(packetHeader, pPacket, pos);

  int packetSize =
      sizeof(SEPacketHeader) + packetHeader.length; // header.length does not include size of header

  // Loop over all subpackets in packet
  while (pos < packetSize)
  {
    // Read one subpacket header from received packet
    SESubPacketHeader subPacketHeader;
    readValue(subPacketHeader, pPacket, pos);

    // Check if this is the correct id
    if (subPacketHeader.id == numericalId)
    {
      readValue(value, pPacket, pos);
      return true;
    }
    else
    {
      // Jump to next subpacket header
      pos += subPacketHeader.length;
    }
  }

  return false;
}

/// Looks up data with the given id in the packet
/// Returns true if data was found, false otherwise
/// Note: This function may only be used for SEAllWorldIntersections (note plural).
bool findDataInPacket(const unsigned int& numericalId,
                      const char* pPacket,
                      SEWorldIntersectionStruct value[],
                      SEu16& numberOfIntersections)
{
  int pos = 0;
  SEPacketHeader packetHeader;
  readValue(packetHeader, pPacket, pos);

  int packetSize =
      sizeof(SEPacketHeader) + packetHeader.length; // header.length does not include size of header

  // Loop over all subpackets in packet
  while (pos < packetSize)
  {
    // Read one subpacket header from received packet
    SESubPacketHeader subPacketHeader;
    readValue(subPacketHeader, pPacket, pos);

    // Check if this is the correct id
    if (subPacketHeader.id == numericalId)
    {
      readValue(value, numberOfIntersections, pPacket, pos);
      return true;
    }
    else
    {
      // Jump to next subpacket header
      pos += subPacketHeader.length;
    }
  }

  return false;
}
