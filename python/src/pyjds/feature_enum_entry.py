"""Feature enum entry module"""
from asyncio.log import logger
from logging import getLogger, DEBUG, NullHandler
import _module
from .error_pyjds import *

# from .feature import *
from .enum_visibility_type import *


class FeatureEnumEntry:
    """Feature enum entry class."""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureEnumEntry)
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.propagate = True
        self._feature = feature

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"

    @property
    def name(self) -> str:
        """Get feature name.

        Returns
        -------
        str
            feature name
        """
        return self._feature.name

    @property
    def description(self) -> str:
        """Get a long description of the feature.

        Returns
        -------
        str
            a long description of the feature
        """
        return self._feature.description

    @property
    def display_name(self) -> str:
        """Get a name string for display.

        Returns
        -------
        str
            a name string for display
        """
        return self._feature.display_name

    @property
    def tool_tip(self) -> str:
        """Get a short description of the node.

        Returns
        -------
        str
            a short description of the node
        """
        return self._feature.tool_tip

    @property
    def visibility(self) -> VisibilityType:
        """Get the recommended visibility of the node.

        Returns
        -------
        Visibility
            recommended visibility of a node
        """
        return self._feature.visibility

    @property
    def value(self) -> int:
        """Get the feature value.

        Returns
        -------
        int
            the feature value

        Raises
        ------
            PyJdsFeatureException
        """
        try:
            return self._feature.value
        except _module.PyFeatureExp as e:
            self._logger.error(f"<{__name__}#{self._feature.name}> {e}")
            raise PyJdsFeatureException(e)

    def is_available(self) -> bool:
        """Checks if the entry is available.

        Returns
        -------
        bool
            If true available, else unavailable
        """
        return self._feature.is_available()