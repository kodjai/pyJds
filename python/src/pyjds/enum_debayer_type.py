"""Debayer type module

DeBayer method to be used when PixelFormat is Bayer format.
"""
from enum import Enum, IntEnum
import _module


class DebayerType(IntEnum):
    """Debayer type"""

    SIMPLE = (1,)
    """Indicates the debayer method is 2x2"""
    INTERPOLATION = (2,)
    """Indicates the debayer method is 3x3"""
    NOBAYERPROCESS = 3
    """
    DeBayer processing is not performed;
    only UnPack processing is performed when PixelFormat is Packed.
    If the PixelFormat is not Packed, the camera output remains the same.
    """
