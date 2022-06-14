"""Feature string module"""
from typing import Tuple
import _module
from .feature import *
from .error_pyjds import *


class FeatureString(Feature):
    """Feature string class."""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureString)
        super().__init__(feature)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"

    @Feature.value.getter
    def value(self) -> str:
        """Get the feature value.

        Returns
        -------
        str
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
    def value(self, value: str) -> None:
        """Set the feature value.

        Parameters
        ----------
        value : str
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
    def max_length(self) -> int:
        """Get max length of the feature

        Returns
        -------
        int
            max length of the feature
        """
        return self._feature.max_length
