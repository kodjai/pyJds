"""Feature bool module"""
import _module
from .error_pyjds import *
from .feature import *


class FeatureBool(Feature):
    """Feature bool class"""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureBool)
        super().__init__(feature)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"

    @Feature.value.getter
    def value(self) -> bool:
        """Get value of the feature.

        Returns
        -------
        bool
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
    def value(self, value: bool) -> None:
        """Set value of the feature

        Parameters
        ----------
        value : bool
            the feature value

        Raise
            PyJdsFeatureException
        -----
        """
        try:
            self._feature.value = value
        except _module.PyFeatureExp as e:
            self._logger.error(f"<{__name__}#{self._feature.name}> {e}")
            raise PyJdsFeatureException(e)
