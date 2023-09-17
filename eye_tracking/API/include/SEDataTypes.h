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


#if !defined(SE_DATA_TYPES__INCLUDED_)
#define SE_DATA_TYPES__INCLUDED_

#ifdef WIN32
  typedef unsigned __int64 SEu64;
#else
  typedef unsigned long long SEu64;
#endif

typedef unsigned char SEu8;
typedef unsigned short SEu16;
typedef unsigned int SEu32;
typedef int SEs32;

typedef float SEf32;
typedef double SEf64;

struct SEPoint2D {
  SEf64 x;
  SEf64 y;
};

struct SEVect2D {
  SEf64 x;
  SEf64 y;
};

struct SEPoint3D {
  SEf64 x;
  SEf64 y;
  SEf64 z;
};

struct SEVect3D {
  SEf64 x;
  SEf64 y;
  SEf64 z;
};

struct SEString {
  SEu16 size;
  char ptr[1024];
};

struct SEWorldIntersectionStruct {
  SEPoint3D worldPoint;     // intersection point in world coordinates
  SEPoint3D objectPoint;    // intersection point in local object coordinates
  SEString objectName;      // name of intersected object
};

struct SEQuaternion {
  SEf64 w;
  SEf64 x;
  SEf64 y;
  SEf64 z;
};

// SEUserMarkerStruct is an implementation of the value optionally contained in SEType_UserMarker
struct SEUserMarkerStruct {
  SEs32 error;         // 0 if no error, otherwise error.
  SEu64 cameraClock;   // CameraClock of this marker.
  SEu8 cameraIdx;      // Index of the camera that received this marker.
  SEu64 data;          // User-defined data.
};

enum SEType {
SEType_u8 = 0x0000,
SEType_u16 = 0x0001,
SEType_u32 = 0x0002,
SEType_s32 = 0x0003,
SEType_u64 = 0x0004,
SEType_f64 = 0x0005,
SEType_float = 0x0005,
SEType_Point2D = 0x0006,
SEType_Vect2D = 0x0007,
SEType_Point3D = 0x0008,
SEType_Vect3D = 0x0009,
SEType_String = 0x000A,
SEType_Vector = 0x000B,
SEType_Struct = 0x000C,
SEType_WorldIntersection = 0x000D,
SEType_WorldIntersections = 0x000E,
SEType_PacketHeader = 0x000F,
SEType_SubPacketHeader = 0x0010,
SEType_f32 = 0x0011,
SEType_Matrix3x3 = 0x0012,
SEType_Matrix2x2 = 0x0013,
SEType_Quaternion = 0x0014,
SEType_UserMarker = 0x0015,
SEType_PupilMatchPointAnalysis = 0x0016,
};

struct SEOutputData
{
  int numericalDataId;
  const char* dataId;
  SEType typeId;
};

/**
*	A header for the SmartEyePacket
*	- should be 64 bits ( 8 bytes )
**/
#define PACKET_HEADER_SIZE 8
struct SEPacketHeader
{
  SEu32 syncId;		      /**< always 'SEPD' */
  SEu16 packetType;     /**< always 4 */
  SEu16 length;         /**< number of bytes following this header, that is, not including size of this header  */
};

#define SUB_PACKET_HEADER_SIZE 4
struct SESubPacketHeader
{
  SEu16 id;             /**< Output data identifier, refer to SEOutputDataIds for existing ids */
  SEu16 length;         /**< number of bytes following this header  */
};

#endif // SE_DATA_TYPES__INCLUDED_
