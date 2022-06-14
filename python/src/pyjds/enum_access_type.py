"""Interface type enum module

Access type for connection that can be specified in case of GigE device
"""
from enum import IntEnum
import _module


class AccessType(IntEnum):
    """GigE vision device access type"""

    Control = (_module.AccessType.Control,)
    """Indicates control access"""
    Exclusive = (_module.AccessType.Exclusive,)
    """Indicates exclusive access"""
    ReadOnly = (_module.AccessType.ReadOnly,)
    """Indicates readonly access"""
