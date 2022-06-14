"""Feature enum module"""
from typing import Union, List
import _module
from .feature import *
from .feature_enum_entry import *
from .error_pyjds import *


class FeatureEnum(Feature):
    """Feature enum class."""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureEnum)
        super().__init__(feature)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"

    @Feature.value.getter
    def value(self) -> int:
        """Get the feature value.

        :getter: Returns the feature value
        :setter: Sets the feature value
        :type: string

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
    def value(self, value: Union[str, int]) -> None:
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
            if isinstance(value, str):
                self._feature.value_as_string = value
            elif isinstance(value, FeatureEnumEntry):
                self._feature.value_as_string = value.name
            elif isinstance(value, int):
                self._feature.value = value
            else:
                msg = f"unsupported type:{type(value)}"
                self._logger.error(msg)
                raise AttributeError(msg)

        except _module.PyFeatureExp as e:
            self._logger.error(f"<{__name__}#{self._feature.name}> {e}")
            raise PyJdsFeatureException(e)

    @property
    def value_as_str(self) -> str:
        """Get the feature value as str.

        Returns
        -------
        str
            the feature value

        Raises
        ------
            PyJdsFeatureException
        """
        try:
            return self._feature.value_as_string
        except _module.PyFeatureExp as e:
            self._logger.error(f"<{__name__}#{self._feature.name}> {e}")
            raise PyJdsFeatureException(e)

    @property
    def entries(self) -> List[FeatureEnumEntry]:
        """Get entries of the feature.

        Returns
        -------
        list
            entries of the feature
        """
        entries = self._feature.get_entries(True)
        entry_list = []
        for e in entries:
            ee = FeatureEnumEntry(e)
            entry_list.append(ee)
        return entry_list
