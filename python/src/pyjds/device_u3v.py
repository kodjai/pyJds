"""U3V device module"""
from typing import List
import _module
from .device import *
from .error_pyjds import *
from pyjds.stream_u3v import StreamU3V


class DeviceU3V(Device):
    """DeviceU3V class."""

    def __init__(self, _device: _module.Device) -> None:
        assert isinstance(_device, _module.DeviceU3V)
        super().__init__(_device)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @classmethod
    def create(cls, connection_id: str):
        """Create the U3V device.

        Parameters
        ----------
            connection_id : str
            GUID is valid.

        """
        m_device = _module.DeviceU3V.create_gev(connection_id)
        device = DeviceU3V(m_device)
        return device

    def connect(self) -> None:
        """Connect to the U3V device.

        Raises
        -------
        PyJdsConnectException
            Failed to connect to the device.

        """
        try:
            self._m_device.connect()
        except _module.PyConnectExp as e:
            self._logger.error(f"{e}")
            raise PyJdsConnectException(e)

    def create_and_open_streams(
        self, usermode_data_receiver_thread_priority: int = -1
    ) -> List[StreamU3V]:
        """Create streams to the connecting device.
        If the device has multiple streams, automatically generate the corresponding stream.

        Returns
        -------
        stream_list : list of Stream
            list of stream description
        """
        streams = self._m_device.create_and_open_streams()
        stream_list = []
        for s in streams:
            ss = StreamU3V(s)
            stream_list.append(ss)

        return stream_list

    @property
    def guid(self) -> str:
        """Get guid

        Returns
        -------
        str
            guid
        """
        self._m_device.guid
