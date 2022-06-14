"""GEV Stream module"""
import _module
from .stream import *


class StreamGEV(Stream):
    """StreamGEV class."""

    def __init__(self, m_stream: _module.StreamGEV) -> None:
        assert isinstance(m_stream, _module.StreamGEV)
        super().__init__(m_stream)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @property
    def device_ip_adress(self) -> str:
        """Get the IPAddress of device

        Returns
        -------
        str
            IPAddress
        """
        return self._m_stream.device_ip_address

    @property
    def local_ip_address(self) -> str:
        """Get the IPAddress of host pc

        Returns
        -------
        str
            IPAddress
        """
        return self._m_stream.local_ip_address

    @property
    def local_port(self) -> int:
        """Get the port number of host pc

        Returns
        -------
        int
            port number
        """
        return self._m_stream.local_port

    @property
    def user_mode_data_receiver_thread_priority(self):
        """
        The thread priority of user mode data receiver

        :getter: Returns the thread priority of user mode data receiver
        :setter: Sets the thread priority of user mode data receiver
        :type: int
        """
        return self._m_stream.thread_priority

