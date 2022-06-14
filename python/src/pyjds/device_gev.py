"""GEV device module

For GigE cameras, the access type can be specified at the time of connection
"""
from logging import getLogger, DEBUG, NullHandler
from typing import List
import _module
from pyjds.stream_gev import StreamGEV
from .device_gev import *
from .device import *
from .enum_access_type import *
from .error_pyjds import *


class DeviceGEV(Device):
    def __init__(self, _device: _module.DeviceGEV) -> None:
        assert isinstance(_device, _module.DeviceGEV)
        super().__init__(_device)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @classmethod
    def create(cls, connection_id: str):
        """Create the GigE device.

        Parameters
        ----------
            connection_id : str
            IP address, MAC address and DeviceUserID are valid.

        """
        m_device = _module.DeviceGEV.create_gev(connection_id)
        device = DeviceGEV(m_device)
        return device

    def connect(self, access_type: AccessType = AccessType.Control) -> None:
        """Connect to the GigE device.

        For GigE devices, the packet size is determined automatically.

        Raises
        -------
        PyJdsConnectException
            Failed to connect to the device.

        """
        try:
            access_type_dict = {AccessType.Control:_module.AccessType.Control,
            AccessType.Exclusive:_module.AccessType.Exclusive,
            AccessType.ReadOnly:_module.AccessType.ReadOnly}
            access_type = access_type_dict.get(access_type)
            self._m_device.connect(access_type)
        except KeyError as e:
            raise PyJdsConnectException(f"Invalid access_type({access_type})")
        except _module.PyConnectExp as e:
            self._logger.error(f"{e}")
            raise PyJdsConnectException(e)

    def create_and_open_streams(
        self, usermode_data_receiver_thread_priority: int = -1
    ) -> List[StreamGEV]:
        """Create streams to the connecting device.
        If the device has multiple streams, automatically generate the corresponding stream.

        Parameters
        ----------
        usermode_data_receiver_thread_priority : int, optional
            Set usermode_data_receiver_thread_priority in stream class
            In Windows, 0-6 is valid.
                0:THREAD_PRIORITY_IDLE
                1:THREAD_PRIORITY_LOWEST
                2:THREAD_PRIORITY_BELOW_NORMAL
                3:THREAD_PRIORITY_NORMAL
                4:THREAD_PRIORITY_ABOVE_NORMAL
                5:THREAD_PRIORITY_HIGHEST
                6:THREAD_PRIORITY_TIME_CRITICAL

        Returns
        -------
        stream_list : list of Stream
            list of stream description

        Raises
        -------
        PyJdsStreamException
        """
        try:
            streams = self._m_device.create_and_open_streams(
                usermode_data_receiver_thread_priority
            )
            stream_list = []
            for s in streams:
                ss = StreamGEV(s)
                stream_list.append(ss)

            return stream_list
        except _module.PyJdsStreamExp as e:
            self._logger.error(f"{e}")
            raise PyJdsStreamException(e)

    @property
    def ip_address(self) -> str:
        """Get ip address.

        Returns
        -------
        str
            ip address
        """
        return self._m_device.ip_address

    @property
    def mac_address(self) -> str:
        """Get mac address

        Returns
        -------
        str
            mac address
        """
        return self._m_device.mac_address
