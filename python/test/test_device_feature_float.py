import logging
import pytest
from my_logger import Logger
import pyjds

logger = Logger.get_logger()


class TestFeatureFloat(object):
    @classmethod
    def setup_class(cls):
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
        feature = self.__device.get_feature("AcquisitionFrameRate")
        logger.debug(feature)
        logger.debug("***** AcquisitionFrameRate *****")
        assert feature.name == "AcquisitionFrameRate"
        orginal_value = feature.value
        logger.debug("value: %s", orginal_value)
        feature.value = feature.range[1] - 1
        logger.debug("value: %s", feature.value)
        feature.from_string(str(orginal_value))
        logger.debug("value: %s", feature.value)
        assert feature.feature_type == pyjds.FeatureType.FLOAT
        assert feature.visibility == pyjds.VisibilityType.BEGINNER
        assert feature.is_available() == True
        assert feature.is_implement() == True
        assert feature.is_readable() == True
        assert feature.is_selector() == False
        assert feature.is_streamable() == True
        assert feature.is_writable() == True
        assert feature.unit == "Hz"
        # assert feature.representation_type == pyjds.RepresentationType.LINEAR
        assert feature.category == "Root\\AcquisitionControl"

        logger.debug("range: %s", feature.range)
        logger.debug("category: %s", feature.category)
        logger.debug("description: %s", feature.description)
        logger.debug("display_name: %s", feature.display_name)
        logger.debug("tool_tip: %s", feature.tool_tip)

    def test_expect_success_get_param(self):
        param = param_answer_timeout = self.__device.get_feature("AcquisitionFrameRate")
        logger.debug(f"AcquisitionFrameRate({param.value})")

    def test_get_all_features(self):
        """Get all camera features."""
        parameters = self.__device.get_features()
        logger.debug(f"len:{len(parameters)}")
        param = [s for s in parameters if s.name == "ExposureTime"]
        assert param != None
        param[0].value

    def test_get_feature_then_get_unavailable_feature(self):
        """Get camera feature.
        Get unavailable feature from got param.
        """
        parameter = self.__device.get_feature("ChunkWidth")
        assert parameter != None

        with pytest.raises(pyjds.PyJdsFeatureException) as ex:
            parameter.value
        logger.debug(f"pyjds.PyJdsFeatureException:{ex}")

    def test_get_readonly_param(self):
        """Get readonly camera feature.
        Check available and readable for true and wretable for false.
        Check that exceptions are raised when setting values.
        """
        parameter = self.__device.get_feature("GevMCSP")
        assert parameter.is_available() == True
        assert parameter.is_readable() == True
        assert parameter.is_writable() == False
        logger.debug(f"value:{parameter.value}")
        with pytest.raises(pyjds.PyJdsFeatureException) as einfo:
            logger.debug(f"value:{parameter.value}")
            parameter.value = 1005
        logger.debug(f"value:{einfo}")

    def test_get_writable_param(self):
        """Get writable camera feature.
        Check available and readable for true and writable for false.
        Check that no exceptions are raised when setting values.
        """
        param = self.__device.get_feature("AcquisitionFrameRate")
        assert param != None
        assert param.is_available() == True
        assert param.is_readable() == True
        assert param.is_writable() == True
        logger.debug(f"range:{param.range}")
        fps = param.range[0] + (param.range[1] - param.range[0]) / 2
        param.value = fps
        assert param.value > fps - 0.5
        assert param.value < fps + 0.5
        # assert param.value == fps
