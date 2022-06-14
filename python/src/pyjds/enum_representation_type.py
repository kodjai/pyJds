"""Representation type enum module"""
from enum import Enum, IntEnum
import _module


class RepresentationType(IntEnum):
    """recommended representation of a node value"""

    LINEAR = (_module.RepresentationType.LINEAR,)
    """Indicates recommend is slider with linear behavior"""
    HEXNUMBER = (_module.RepresentationType.HEXNUMBER,)
    """Indicates recommend is hex number in an edit control"""
    BOOLEAN = (_module.RepresentationType.BOOLEAN,)
    """Indicates recommend is slider with logarithmic behaviour"""
    LOGARITHMIC = (_module.RepresentationType.LOGARITHMIC,)
    """Indicates recommend is slider with logarithmic behaviour"""
    PURENUMBER = (_module.RepresentationType.PURENUMBER,)
    """Indicates recommend is secimal number in an edit control"""

    @classmethod
    def get(cls, module_representation):
        assert isinstance(module_representation, _module.RepresentationType) == True

        if module_representation == _module.RepresentationType.LINEAR:
            return RepresentationType.LINEAR
        elif module_representation == _module.RepresentationType.HEXNUMBER:
            return RepresentationType.HEXNUMBER
        elif module_representation == _module.RepresentationType.BOOLEAN:
            return RepresentationType.BOOLEAN
        elif module_representation == _module.RepresentationType.LOGARITHMIC:
            return RepresentationType.LOGARITHMIC
        elif module_representation == _module.RepresentationType.PURENUMBER:
            return RepresentationType.PURENUMBER
        else:
            raise RuntimeError(
                f"Invalid argument:{type(module_representation)}({module_representation})"
            )
