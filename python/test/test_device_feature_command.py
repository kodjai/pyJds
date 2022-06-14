from logging.handlers import TimedRotatingFileHandler
import logging
import pytest
from my_logger import Logger
import pyjds

logger = Logger.get_logger()


class TestFeatureCommand(object):
    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        finder = pyjds.device_finder.DeviceFinder()
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
        user_set_selector = self.__device.get_feature("UserSetSelector")
        logger.debug(user_set_selector)
        assert user_set_selector.name == "UserSetSelector"
        logger.debug("***** %s *****", user_set_selector.name)
        orginal_value = user_set_selector.value
        logger.debug("value: %s", orginal_value)
        user_set_selector.value = "UserSet1"

        feature = self.__device.get_feature("UserSetLoad")
        logger.debug(feature)
        assert feature.name == "UserSetLoad"
        logger.debug("***** %s *****", feature.name)

        assert feature.feature_type == pyjds.FeatureType.COMMAND
        assert feature.visibility == pyjds.VisibilityType.BEGINNER
        assert feature.is_available() == True
        assert feature.is_implement() == True
        assert feature.is_readable() == False
        assert feature.is_selector() == False
        assert feature.is_streamable() == False
        assert feature.is_writable() == True
        assert feature.category == "Root\\UserSetControl"

        logger.debug("description: %s", feature.description)
        logger.debug("display_name: %s", feature.display_name)
        logger.debug("tool_tip: %s", feature.tool_tip)

        feature.execute()
        feature.is_done()
