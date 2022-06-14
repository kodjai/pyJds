"""Interface type enum module"""
from enum import Enum, IntEnum
import _module


class InterfaceType(IntEnum):
    """device interface type"""

    GigEVision = (_module.DeviceInterfaceType.GigEVision,)
    """Indicates GigEVision interface"""
    USB3Vision = (_module.DeviceInterfaceType.USB3Vision,)
    """Indicates USB3Vision interface"""

    @classmethod
    def get(cls, module_device_interface_type):
        assert (
            isinstance(module_device_interface_type, _module.DeviceInterfaceType)
            == True
        )
        if module_device_interface_type == _module.DeviceInterfaceType.GigEVision:
            return InterfaceType.GigEVision
        elif module_device_interface_type == _module.DeviceInterfaceType.USB3Vision:
            return InterfaceType.USB3Vision
        else:
            raise RuntimeError(
                f"Invalid argument:{type(module_device_interface_type)}({module_device_interface_type})"
            )
