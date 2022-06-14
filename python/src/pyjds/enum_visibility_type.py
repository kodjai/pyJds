"""Visivility type enum module"""
from enum import Enum, IntEnum
import _module
from .enum_visibility_type import *


class VisibilityType(IntEnum):
    """recommended visibility of a node"""

    BEGINNER = (_module.Visibility.BEGINNER,)
    """Indicates always visible"""
    EXPERT = (_module.Visibility.EXPERT,)
    """Indicates visible for experts or Gurus"""
    GURU = (_module.Visibility.GURU,)
    """Indicates visible for Gurus"""
    INVISIBLE = (_module.Visibility.INVISIBLE,)
    """Indicates unvisible"""

    @classmethod
    def get(cls, module_visibility):
        """"""
        assert isinstance(module_visibility, _module.Visibility) == True

        if module_visibility == _module.Visibility.BEGINNER:
            return VisibilityType.BEGINNER
        elif module_visibility == _module.Visibility.EXPERT:
            return VisibilityType.EXPERT
        elif module_visibility == _module.Visibility.GURU:
            return VisibilityType.GURU
        elif module_visibility == _module.Visibility.INVISIBLE:
            return VisibilityType.INVISIBLE
        else:
            raise RuntimeError(
                f"Invalid argument:{type(module_visibility)}({module_visibility})"
            )
