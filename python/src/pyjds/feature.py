"""Featute module"""
from asyncio.log import logger
from logging import getLogger, DEBUG, NullHandler
import _module
from .enum_feature_type import *
from .enum_visibility_type import *


class Feature(object):
    """Feature base class."""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.Feature)
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
    def category(self) -> str:
        """Get category of the feature.

        Returns
        -------
        str
            category of the feature
        """
        return self._feature.category

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
    def feature_type(self) -> FeatureType:
        """Get a feature type.

        Returns
        -------
        FeatureType
            a feature type
        """
        return FeatureType.get(self._feature.feature_type)

    @property
    def visibility(self) -> VisibilityType:
        """Get the recommended visibility of the node.

        Returns
        -------
        Visibility
            recommended visibility of a node
        """
        return VisibilityType.get(self._feature.visibility)

    @property
    def value(self):
        pass

    @value.setter
    def value(self, value):
        pass

    def is_available(self) -> bool:
        """Checks if the node is available.

        Returns
        -------
        bool
            If true available, else unavailable
        """
        return self._feature.is_available()

    def is_implement(self) -> bool:
        """Checks if the node is implemented.

        Returns
        -------
        bool
            If true the node is implemented, else not implemented
        """
        return self._feature.is_implemented()

    def is_readable(self) -> bool:
        """Checks if the node is readable.

        Returns
        -------
        bool
            If true readable, else unreadable
        """
        return self._feature.is_readable()

    def is_selector(self) -> bool:
        """Checks if the node is selector.

        Returns
        -------
        bool
            If true selector, else not selector
        """
        return self._feature.is_selector()

    def is_streamable(self) -> bool:
        """Checks if the node is streamable.

        Returns
        -------
        bool
            If true streamable, else unstreamable
        """
        return self._feature.is_streamable()

    def is_writable(self) -> bool:
        """Checks if the node is writable.

        Returns
        -------
        bool
            If true writable, else unwritable
        """
        return self._feature.is_writable()

    def from_string(self, arg: str) -> None:
        """Set content of the node as string.

        Parameters
        ----------
        arg : str
            the node value

        """
        return self._feature.from_string(arg)
