import pytest
from logging.handlers import TimedRotatingFileHandler
import logging
from my_logger import Logger
import pyjds

logger = Logger.get_logger(logging.DEBUG)


class Test(object):
    @classmethod
    def setup_class(self):
        pass

    def setup_method(self, method):
        finder = pyjds.DeviceFinder()
        found_devices = finder.find()
        logger.debug("number of found device: %s", len(found_devices))

        if len(found_devices) >= 1:
            self.__connection_id = found_devices[0].connection_id
            logger.debug("connection_id: %s", self.__connection_id)
            self.__device = pyjds.DeviceFactory.create(found_devices[0])
            self.__device.connect()
        else:
            raise Exception

    def teardown_method(self, method):
        if self.__device.is_connected():
            self.__device.dis_connect()

    def test_feature(self):
        feature = self.__device.get_feature("GevCurrentIPConfigurationDHCP")
        logger.debug(feature)
        assert feature.name == "GevCurrentIPConfigurationDHCP"
        logger.debug(f"*****{feature.name}*****")
        orginal_value = feature.value
        logger.debug(f"value: {orginal_value}")
        feature.value = not orginal_value
        logger.debug(f"value: {feature.value}")
        feature.value = True

        feature.from_string(str(orginal_value))
        logger.debug("value: %s", feature.value)
        assert feature.feature_type == pyjds.FeatureType.BOOLEAN
        assert feature.visibility == pyjds.VisibilityType.BEGINNER
        assert feature.is_available() == True
        assert feature.is_implement() == True
        assert feature.is_readable() == True
        assert feature.is_selector() == False
        assert feature.is_streamable() == True
        assert feature.is_writable() == True
        assert feature.category == "Root\\TransportLayerControl\\GigEVision"

        logger.debug("description: %s", feature.description)
        logger.debug("display_name: %s", feature.display_name)
        logger.debug("tool_tip: %s", feature.tool_tip)

    def test_get_writable_param(self):
        """Get writable camera feature.
        Check available and readable for true and writable for false.
        Check that no exceptions are raised when setting values.
        """
        param = self.__device.get_feature("GevCurrentIPConfigurationDHCP")
        assert param != None
        assert param.is_available() == True
        assert param.is_readable() == True
        assert param.is_writable() == True
        current = param.value
        logger.debug(f"value:{current}")
        param.value = not current
        logger.debug(f"value:{current}")
