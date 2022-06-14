"""Feature integer module"""
from pyexpat import features
from typing import Tuple

import _module
from .feature import *
from .enum_representation_type import *
from .error_pyjds import *


class FeatureInteger(Feature):
    """Feature integer class."""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureInteger)
        super().__init__(feature)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"

    @property
    def increment(self) -> int:
        """Get increment value.

        Returns
        -------
        int
            increment value of the feature
        """
        return self._feature.increment

    @property
    def range(self) -> Tuple[int, int]:
        """Get range of writable value.

        Returns
        -------
        Tuple[int,int]
            range of writable value
        """
        return self._feature.range

    @property
    def unit(self) -> str:
        """Get the physical unit name.

        Returns
        -------
        str
            the physical unit name
        """
        return self._feature.unit

    @Feature.value.getter
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

    @value.setter
    def value(self, value: int) -> None:
        """Set the feature value.

        Parameters
        ----------
        value : int
            the feature value

        Raises
        ------
            PyJdsFeatureException
        """
        try:
            self._feature.value = value
        except _module.PyFeatureExp as e:
            self._logger.error(f"<{__name__}#{self._feature.name}> {e}")
            raise PyJdsFeatureException(e)

    @property
    def representation_type(self) -> RepresentationType:
        """Get recommended representation.

        Returns
        -------
        RepresentationType
            recommended representation
        """
        return RepresentationType.get(self._feature.representation_type)
