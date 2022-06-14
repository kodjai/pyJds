import _module
from .feature import *


class FeatureRegister(Feature):
    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureRegister)
        super().__init__(feature)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"
