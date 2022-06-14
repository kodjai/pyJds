"""Detect device type enum module

GigE device detection method type.
This will be used by DeviceFinder.
"""
from enum import IntEnum
import _module


class DetectDeviceType(IntEnum):
    """GigE vision detection method type"""

    DirectedBroadcast = (0,)
    """Indicates tetected method is directed broadcast"""
    LimitedBroadcast = (1,)
    """Indicates tetected method is limited broadcast"""
