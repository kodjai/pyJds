"""Host interface module"""
from logging import getLogger, DEBUG, NullHandler
import _module


class HostInterface:
    """Host interface class"""

    def __init__(self, host_interface) -> None:
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.propagate = True

        assert isinstance(host_interface, _module.HostInterface)
        self.__mod_host_interface = host_interface

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @property
    def display_id(self) -> str:
        return self.__mod_host_interface.display_id

    # @property
    # def ip_address(self) -> str:
    #     return self.__mod_host_interface.ip_address

    # @property
    # def mac_address(self) -> str:
    #     return self.__mod_host_interface.mac_address
