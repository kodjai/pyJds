"""U3V Stream module"""
import _module
from .stream import *


class StreamU3V(Stream):
    """StreamU3V class."""

    def __init__(self, m_stream: _module.StreamU3V) -> None:
        assert isinstance(m_stream, _module.StreamU3V)
        super().__init__(m_stream)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @property
    def guid(self) -> str:
        """Get the stream's GUID

        Returns
        -------
        str
            GUID
        """
        return self._m_stream.guid
