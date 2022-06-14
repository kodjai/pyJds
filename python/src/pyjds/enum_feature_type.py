"""Feature type enum module

Indicates the feature type to be acquired by the Device class or Stream class.
"""
from enum import Enum, IntEnum
import _module


class FeatureType(IntEnum):
    """typedef for feature type"""

    BOOLEAN = (_module.FeatureType.BOOLEAN,)
    """Indicates IBoolean interface"""
    COMMAND = (_module.FeatureType.COMMAND,)
    """Indicates ICommand interface"""
    ENUMERATION = (_module.FeatureType.ENUMERATION,)
    """Indicates IEnumeration interface"""
    FLOAT = (_module.FeatureType.FLOAT,)
    """Indicates IFloat interface"""
    INTEGER = (_module.FeatureType.INTEGER,)
    """Indicates IInteger interface"""
    REGISTER = (_module.FeatureType.REGISTER,)
    """Indicates IRegister interface"""
    STRING = (_module.FeatureType.STRING,)
    """Indicates IString interface"""

    @classmethod
    def get(cls, module_feature_type):
        assert isinstance(module_feature_type, _module.FeatureType) == True
        if module_feature_type == _module.FeatureType.BOOLEAN:
            return FeatureType.BOOLEAN
        elif module_feature_type == _module.FeatureType.COMMAND:
            return FeatureType.COMMAND
        elif module_feature_type == _module.FeatureType.ENUMERATION:
            return FeatureType.ENUMERATION
        elif module_feature_type == _module.FeatureType.FLOAT:
            return FeatureType.FLOAT
        elif module_feature_type == _module.FeatureType.INTEGER:
            return FeatureType.INTEGER
        elif module_feature_type == _module.FeatureType.STRING:
            return FeatureType.STRING
        else:
            raise RuntimeError(
                f"Invalid argument:{type(module_feature_type)}({module_feature_type})"
            )
