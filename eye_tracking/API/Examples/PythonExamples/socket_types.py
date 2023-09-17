# Copyright (C) Smart Eye AB 2002-2018
# THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.

# pylint: disable=R0903, C0111
import ctypes


class SEPacketHeader(ctypes.Structure):
    _fields_ = [("syncId", ctypes.c_uint32), ("packetType", ctypes.c_uint16),
                ("length", ctypes.c_uint16)]


class SESubPacketHeader(ctypes.Structure):
    _fields_ = [("id", ctypes.c_uint16), ("length", ctypes.c_uint16)]


class SETypePoint2D(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double)]


class SETypeVect2D(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double)]


class SETypePoint3D(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double),
                ('z', ctypes.c_double)]


class SETypeVect3D(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double),
                ('z', ctypes.c_double)]


class SETypeQuaternion(ctypes.Structure):
    _fields_ = [('w', ctypes.c_double), ('x', ctypes.c_double),
                ('y', ctypes.c_double), ('z', ctypes.c_double)]


class SETypeString(ctypes.Structure):
    _fields_ = [('size', ctypes.c_uint16), ('ptr', ctypes.c_char_p)]


class SETypeWorldIntersection(ctypes.Structure):
    _fields_ = [('world_point', SETypePoint3D),
                ('object_point', SETypePoint3D), ('object_name', SETypeString)]


class SETypeUserMarker(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('error', ctypes.c_int32), ('cameraClock', ctypes.c_uint64),
                ('cameraIdx', ctypes.c_uint8), ('data', ctypes.c_uint64)]
