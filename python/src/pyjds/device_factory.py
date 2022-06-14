"""Device factory module

Create an instance Device class using the DeviceInfo obtained by DeviceFinder.
"""
import logging
from logging import getLogger, DEBUG, NullHandler, StreamHandler
import _module
from .device import Device
from .device_gev import *
from .device_info import *
from .device_u3v import *
from .error_pyjds import PyJdsConnectException
from .enum_interface_type import *


class DeviceFactory:
    """Device factory class"""

    def __init__(self) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.addHandler(NullHandler())
        self.__logger.propagate = True

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @classmethod
    def create(cls, device_info: DeviceInfo) -> Device:
        """Create Device instance corresponding of device_info.

        Parameters
        ----------
        device_info : DeviceInfo
            DeviceInfo found by DeviceFinder

        Returns
        -------
        Device
            Returns DeviceGEV or DeviceU3V according to the type specified in device_info.interface_type.

        Raises
        ------
            PyJdsConnectException
                Invalid interface type
        """

        m_interface_type = None
        if device_info.interface_type == InterfaceType.GigEVision:
            m_interface_type = _module.DeviceInterfaceType.GigEVision
        elif device_info.interface_type == InterfaceType.USB3Vision:
            m_interface_type = _module.DeviceInterfaceType.USB3Vision
        else:
            raise PyJdsConnectException("Invalid interface type")

        m_device = _module.Device.create(device_info.connection_id, m_interface_type)
        device = None
        if m_device.interface_type == _module.DeviceInterfaceType.GigEVision:
            device = DeviceGEV(m_device)
        elif m_device.interface_type == _module.DeviceInterfaceType.USB3Vision:
            device = DeviceU3V(m_device)
        else:
            raise PyJdsConnectException("Invalid interface type")

        return device
