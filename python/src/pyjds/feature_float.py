"""Feature float module"""
from typing import Tuple
import _module
from .feature import *
from .enum_representation_type import *
from .error_pyjds import *


class FeatureFloat(Feature):
    """Feature float class."""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureFloat)
        super().__init__(feature)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"

    @property
    def range(self) -> Tuple[float, float]:
        """Get range of writable value.

        Returns
        -------
        Tuple[float,float]
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
    def value(self) -> float:
        """Get the feature value.

        Returns
        -------
        float
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
    def value(self, value: float) -> None:
        """Set the feature value.

        Parameters
        ----------
        value : float
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
