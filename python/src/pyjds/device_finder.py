"""Device finder module

Class to search for devices connected to the host computer.
For GigE cameras, use directed broadcast or limited broadcast for detection.
The default is to use directed broadcast.
"""
from logging import getLogger, DEBUG, NullHandler
from typing import List
import _module
from .device_info import *
from .enum_detect_device_method_type import *


class DeviceFinder:
    def __init__(self) -> None:
        """[summary]"""
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.__device_finder = _module.DeviceFinder()

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    def find(
        self,
        timeout_ms: int = 1500,
        detect_type: DetectDeviceType = DetectDeviceType.DirectedBroadcast,
    ) -> List[DeviceInfo]:
        """Find GigE and USB3 Vision devices reachable from this system.

        Parameters
        ----------
        timeout_ms : int, optional
            timeout millisec, by default 1500
        detect_type : DetectDeviceType, optional
            Set the detection method, by default is using directed broadcast.

        Returns
        -------
        List[DeviceInfo]
            list of DeviceInfo
        """
        detection_type = (
            True if detect_type == DetectDeviceType.DirectedBroadcast else False
        )
        devices = self.__device_finder.find(timeout_ms, detect_type)

        devices_lists = []
        for device in devices:
            device = DeviceInfo(device)
            devices_lists.append(device)

        return devices_lists
