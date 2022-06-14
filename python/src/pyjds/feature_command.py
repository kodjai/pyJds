"""Feature command module"""
import _module
from .feature import *


class FeatureCommand(Feature):
    """Feature command class"""

    def __init__(self, feature) -> None:
        assert isinstance(feature, _module.FeatureCommand)
        super().__init__(feature)

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}:{self._feature.name}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}:{self._feature.name}"

    def execute(self) -> None:
        """Execute command of the feature.

        Raise
        -----
        """
        self._feature.execute()

    def is_done(self) -> bool:
        """Query whether the command is executed.

        Returns
        -------
        bool
            If true the command done else not done.
        """
        return self._feature.is_done()
