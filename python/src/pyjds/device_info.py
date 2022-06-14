"""Device info module

Device information class found by DeviceFinder
Used by DeviceFactory to create camera instances.
"""
import _module
from .host_interface import *
from .enum_interface_type import *


class DeviceInfo:
    def __init__(self, device_info) -> None:
        """[summary]

        Parameters
        ----------
        arg1 : [type]
            [description]
        """
        assert isinstance(device_info, _module.DeviceInfo)
        self.__mod_device_info = device_info

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @property
    def connection_id(self) -> str:
        """Get connection id  of the device.

        Returns
        -------
        str
            connection id
        """
        return self.__mod_device_info.connection_id

    @property
    def interface_type(self) -> InterfaceType:
        """Get device interface type of the device.

        Returns
        -------
        InterfaceType
            InterfaceType.GigEVision : if device is GigEVision
            InterfaceType.USB3Vision : if device is USB3Vision
        """
        return InterfaceType.get(self.__mod_device_info.iftype)

    @property
    def manufacture_info(self) -> str:
        """Get manufacturer information of the device.

        Returns
        -------
        str
            Manufacturer information about the device
        """

        return self.__mod_device_info.manufacture_info

    @property
    def model_name(self) -> str:
        """Get model name of the device.

        Returns
        -------
        str
            model name of the device
        """

        return self.__mod_device_info.model_name

    @property
    def serial_number(self) -> str:
        """Get serial number of the device.
        Returns
        -------
        str
            serial number. This string is a unique identifier of the device.
        """
        return self.__mod_device_info.serial_number

    @property
    def user_id(self) -> str:
        """Get user-programmable device identifier.

        Returns
        -------
        str
            User-programmable device identifier.
        """
        return self.__mod_device_info.user_define_name

    @property
    def vendor_name(self) -> str:
        """Get name of the manufacturer of the device.

        Returns
        -------
        str
            Name of the manufacturer of the device.
        """
        return self.__mod_device_info.vendor_name

    @property
    def device_version(self) -> str:
        """Get device version of the device

        Returns
        -------
        str
            device version of the device
        """
        return self.__mod_device_info.version

    def get_host_interface(self) -> HostInterface:
        host_interface = HostInterface(self.__mod_device_info.get_host_interface())
        return host_interface
