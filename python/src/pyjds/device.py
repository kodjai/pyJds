"""Device module
Superclasses of DeviceGEV and DeviceU3V

It is possible to request AcqusitionStart/Stop to the device
and to get the feature of the device. Also,
depending on the number of Streams the device has,
it will automatically generate the necessary Streams.
"""
from asyncio.log import logger
from logging import getLogger, DEBUG, NullHandler
from typing import Union, Dict, List
from abc import *
import _module
from pyjds.feature_register import FeatureRegister
from .stream import *
from .feature import *
from .feature_integer import *
from .feature_bool import *
from .feature_float import *
from .feature_enum import *
from .feature_command import *
from .feature_string import *
from .device_gev import *
from .error_pyjds import *
from .enum_visibility_type import *
from .enum_interface_type import *


class Device(metaclass=ABCMeta):
    """Device class."""

    def __init__(self, _device: _module.Device) -> None:
        assert isinstance(_device, _module.Device)
        self._m_device = _device
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.propagate = True

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    def dis_connect(self) -> None:
        """Disconnect the device.

        Raises
        ------
        PyJdsConnectException
            Failed to disconnect to the device.

        """
        try:
            self._m_device.dis_connect()
        except _module.PyConnectExp as e:
            self._logger.error(f"{e}")
            raise PyJdsConnectException(e)

    @abstractmethod
    def create_and_open_streams(
        self, usermode_data_receiver_thread_priority
    ) -> List[Stream]:
        raise NotImplementedError()

    def acquisition_start(self, buffer_count: int = 16) -> None:
        """Send AcquisitionStart command to the device.

        Parameters
        ----------
        buffer_count : int, optional
            acquisition buffer count per stream , by default 16

        Raises
        ------
            PyJdsAcqusitionException
            PyJdsStreamException
        -------
        """
        self._logger.info(f"buffer_count({buffer_count})")
        try:
            self._m_device.acquisition_start()
        except _module.PyJdsAcqusitionExp as e:
            self._logger.error(f"{e}")
            raise PyJdsAcqusitionException(e)
        except _module.PyJdsStreamExp as e:
            self._logger.error(f"{e}")
            raise PyJdsStreamException(e)

    def acquisition_stop(self) -> None:
        """Send AcquisitionStop command to the device.

        Raises
        ------
            PyJdsAcqusitionException
        -------

        """
        self._logger.info("")
        try:
            self._m_device.acquisition_stop()
        except _module.PyJdsAcqusitionExp as e:
            self._logger.error(f"{e}")
            raise PyJdsAcqusitionException(e)

    def get_features(self) -> List[Feature]:
        """Get all features.

        Parameters
        ----------

        Returns
        -------
        List[Feature]
            [description]

        """

        features = self._m_device.get_features()

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
                elif feature_type == _module.FeatureType.REGISTER:
                    feature = FeatureRegister(m_feature)
                else:
                    self._logger.error(
                        f"Invalid feature type. feature_name({m_feature.name})"
                    )
                    raise AttributeError("Invalid feature type")

                l_feature.append(feature)

        return l_feature

    def get_feature(self, feature_name: str) -> Union[Feature, None]:
        """Get the appropriate feature class according to the feature name.

        If the specified feature name is of type Integer, it returns FeatureInteger Class,
        and if it is of type Enum, it returns FeatureEnum Class.
        If the specified feature name is not exist in the camera then return None.

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

        m_feature = self._m_device.get_feature(feature_name)
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

    def get_communication_parameters(self) -> List[Feature]:
        """Get all communication features.
        This method keeps the order of the retrieved items.

        Parameters
        ----------

        Returns
        -------
        List[Feature]
            [description]

        """
        features = self._m_device.get_communication_parameters()

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

    def get_communication_parameter(self, feature_name: str) -> Union[Feature, None]:
        """Get the appropriate communication feature class according to the feature name.
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

        m_feature = self._m_device.get_communication_parameter(feature_name)
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

    def is_connected(self) -> bool:
        """Check that the camera is already connected.

        Returns:
            bool:
                If true already connected, else not connected
        """
        return self._m_device.is_connected()

    @property
    def interface_type(self) -> InterfaceType:
        """Get device interface type of the device.

        Returns
        -------
        InterfaceType
            InterfaceType.GigEVision : if device is GigEVision
            InterfaceType.USB3Vision : if device is USB3Vision
        """
        return InterfaceType.get(self._m_device.interface_type)
