"""Stream module
Class that represents an image stream.
A device may have multiple Streams. 
In this case, it is necessary to create multiple Stream instances.
In this library, by executing the create_streams() method of the Device class,
the Stream corresponding to the device will be created.

A Stream has multiple image buffers to be received from the device.
The number of buffers can be specified in the argument of the acquisition_start() method of the Device class.

Since the Buffer is finite, it needs to be released after image processing. 
This library will automatically release the Image class obtained by get_image() when it is out of scope.
In other words, if you continue to use the Image class, you will not be able to acquire images.
"""

from typing import Union, Dict, List
import _module
from pyjds import *
from .buffer import *
from .enum_visibility_type import *
from .error_pyjds import *
from .feature import *
from .feature_integer import *
from .feature_bool import *
from .feature_float import *
from .feature_enum import *
from .feature_command import *
from .feature_string import *
from .stream import *


class Stream:
    """Stream class."""

    def __init__(self, stream):
        """"""
        assert isinstance(stream, _module.Stream)
        self._m_stream = stream
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.propagate = True

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @property
    def channel(self) -> int:
        """Get stream channel number

        Returns
        -------
        int
            Stream channel number
        """
        return self._m_stream.channel

    @property
    def queued_buffer_count(self) -> int:
        """Get number of buffer waiting

        Returns
        -------
        int
             number of buffer waiting
        """
        return self._m_stream.queued_buffer_count

    @property
    def queued_buffer_maximun(self) -> int:
        """Get number of maximum queue buffer

        Returns
        -------
        int
            number of maximum queue buffer
        """
        return self._m_stream.queued_buffer_maximun

    def get_parameters(self) -> List[Feature]:
        """Get all stream features.

        Parameters
        ----------

        Returns
        -------
        List[Feature]

        """
        features = self._m_stream.get_features()

        l_feature = []
        for m_feature in features:
            if m_feature != None:
                feature_type = m_feature.feature_type

                if feature_type == _module.FeatureType.BOOLEAN:
                    feature = FeatureBool(m_feature)
                elif feature_type == _module.FeatureType.INTEGER:
                    feature = FeatureInteger(m_feature)
                elif feature_type == _module.FeatureType.FLOAT:
                    feature = FeatureFloat(m_feature)
                elif feature_type == _module.FeatureType.STRING:
                    feature = FeatureString(m_feature)
                elif feature_type == _module.FeatureType.ENUMERATION:
                    feature = FeatureEnum(m_feature)
                elif feature_type == _module.FeatureType.COMMAND:
                    feature = FeatureCommand(m_feature)
                else:
                    self._logger.error(
                        f"Invalid feature type. feature_name({m_feature.name})"
                    )
                    raise AttributeError("Invalid feature type")

                l_feature.append(feature)

        return l_feature

    def get_parameter(self, feature_name: str) -> Union[Feature, None]:
        """Get the appropriate stream feature class according to the feature name.
        The communication feature class is used to communicate between host and devices.

        If the specified feature name is of type Integer, it returns FeatureInteger Class,
        and if it is of type Enum, it returns FeatureEnum Class.

        Parameters
        ----------
        feature_name : str
            feature name

        Returns
        -------
        FeatureBool
            If type of the feature name is Boolean returns FutureBool class
        FeatureInteger
            If type of the feature name is Integer returns FeatureInteger class
        FeatureFloat
            If type of the feature name is Float returns FeatureFloat class
        FeatureString
            If type of the feature name is String returns FeatureString class
        FeatureEnum
            If type of the feature name is Enumeration returns FeatureEnum class
        FeatureCommand
            If type of the feature name is Command returns FeatureCommand class
        None
            If the specified feature_name does not exist in the camera.
            Whether the specified feature exists or not is determined by the specifications
            of each camera model, and it is possible that the feature does not exist,
            so this is not an error.

        Raises
        -------
        """

        m_feature = self._m_stream.get_feature(feature_name)
        if m_feature == None:
            return None

        feature = None
        feature_type = m_feature.feature_type
        if feature_type == _module.FeatureType.BOOLEAN:
            feature = FeatureBool(m_feature)
        elif feature_type == _module.FeatureType.INTEGER:
            feature = FeatureInteger(m_feature)
        elif feature_type == _module.FeatureType.FLOAT:
            feature = FeatureFloat(m_feature)
        elif feature_type == _module.FeatureType.STRING:
            feature = FeatureString(m_feature)
        elif feature_type == _module.FeatureType.ENUMERATION:
            feature = FeatureEnum(m_feature)
        elif feature_type == _module.FeatureType.COMMAND:
            feature = FeatureCommand(m_feature)
        else:
            self._logger.error(f"Invalid feature type. feature_name({m_feature.name})")
            raise AttributeError("Invalid feature type")

        return feature

    def get_buffer(self, timeout_millsec: int = 1500) -> Buffer:
        """Get buffer.

        Returns
        -------
        Buffer

        Raises
            PyJdsAcqusitionException
        """
        try:
            buffer = self._m_stream.get_buffer(timeout_millsec)
            buffer = Buffer(buffer)
            return buffer
        except _module.PyJdsAcqusitionExp as e:
            self._logger.error(f"{e}")
            raise PyJdsAcqusitionException(e)
