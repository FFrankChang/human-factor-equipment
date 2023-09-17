# Copyright (C) Smart Eye AB 2002-2018
# THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.

#pylint: disable=R0903,C0111
import ctypes

MAX_MSG_LEN = 8

XLUINT64 = ctypes.c_ulonglong
XLACCESS = XLUINT64
XLstatus = ctypes.c_short
XLporthandle = ctypes.c_long


class SXlCanMsg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ulong), ("flags", ctypes.c_ushort),
                ("dlc", ctypes.c_ushort), ("res1", XLUINT64),
                ("data", ctypes.c_ubyte * MAX_MSG_LEN)]


class SXlChipState(ctypes.Structure):
    _fields_ = [("busStatus", ctypes.c_ubyte),
                ("txErrorCounter", ctypes.c_ubyte), ("rxErrorCounter",
                                                     ctypes.c_ubyte),
                ("chipStatte", ctypes.c_ubyte), ("flags", ctypes.c_uint)]


class SXlLinCrcInfo(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte), ("flags", ctypes.c_ubyte)]


class SXlLinWakeUp(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]


class SXlLinNoAns(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte)]


class SXlLinSleep(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]


class SXlLinMsg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte), ("dlc", ctypes.c_ubyte),
                ("flags", ctypes.c_ushort), ("data", ctypes.c_ubyte * 8),
                ("crc", ctypes.c_ubyte)]


class SXlLinMsgApi(ctypes.Union):
    _fields_ = [("SXlLinMsg", SXlLinMsg), ("SXlLinNoAns", SXlLinNoAns),
                ("SXlLinWakeUp", SXlLinWakeUp), ("SXlLinSleep", SXlLinSleep),
                ("SXlLinCrcInfo", SXlLinCrcInfo)]


class SXlSyncPulse(ctypes.Structure):
    _fields_ = [("pulseCode", ctypes.c_ubyte), ("time", XLUINT64)]


class SXlDaioData(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_ubyte), ("timestamp_correction",
                                            ctypes.c_uint), ("mask_digital",
                                                             ctypes.c_ubyte),
                ("value_digital",
                 ctypes.c_ubyte), ("mask_analog",
                                   ctypes.c_ubyte), ("reserved",
                                                     ctypes.c_ubyte),
                ("value_analog",
                 ctypes.c_ubyte * 4), ("pwm_frequency",
                                       ctypes.c_uint), ("pwm_value",
                                                        ctypes.c_ubyte),
                ("reserved1", ctypes.c_uint), ("reserved2", ctypes.c_uint)]


class SXlTransceiver(ctypes.Structure):
    _fields_ = [("event_reason", ctypes.c_ubyte), ("is_present",
                                                   ctypes.c_ubyte)]


class SXlTagData(ctypes.Union):
    _fields_ = [("msg", SXlCanMsg), ("chipState", SXlChipState),
                ("linMsgApi", SXlLinMsgApi), ("syncPulse", SXlSyncPulse),
                ("daioData", SXlDaioData), ("transceiver", SXlTransceiver)]


XLEVENTTAG = ctypes.c_ubyte


class SXlEvent(ctypes.Structure):
    _fields_ = [("tag", XLEVENTTAG), ("chanIndex", ctypes.c_ubyte),
                ("transId", ctypes.c_ushort), ("portHandle", ctypes.c_ushort),
                ("reserved", ctypes.c_ushort), ("timeStamp",
                                                XLUINT64), ("tagData",
                                                            SXlTagData)]
