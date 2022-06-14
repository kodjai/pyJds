import logging
import pytest
from my_logger import Logger
import pyjds
from pyjds.device_gev import DeviceGEV

logger = Logger.get_logger()


class Test(object):
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

    def test_feature_int(self):
        feature = self.__device.get_feature("Width")
        logger.debug("***** Width *****")
        assert feature.name == "Width"
        logger.debug(f"value: {feature.value}")
        feature.from_string("640")
        assert feature.value == 640
        feature.value = 320
        assert feature.value == 320
        logger.debug(feature.visibility)
        logger.debug(type(feature.visibility))
        logger.debug(pyjds.FeatureType.INTEGER)
        logger.debug(type(pyjds.VisibilityType.BEGINNER))
        assert feature.feature_type == pyjds.FeatureType.INTEGER
        assert feature.visibility == pyjds.VisibilityType.BEGINNER
        assert feature.is_available() == True
        assert feature.is_implement() == True
        assert feature.is_readable() == True
        assert feature.is_selector() == False
        assert feature.is_streamable() == True
        assert feature.is_writable() == True

        logger.debug("range: %s", feature.range)
        logger.debug("category: %s", feature.category)
        logger.debug("description: %s", feature.description)
        logger.debug("display_name: %s", feature.display_name)
        logger.debug("tool_tip: %s", feature.tool_tip)
        logger.debug("increment: %s", feature.increment)
        logger.debug("unit: %s", feature.unit)
        logger.debug("representation_type: %s", feature.representation_type)

    def test_expect_success_get_param(self):
        comm_param = param_answer_timeout = self.__device.get_feature("Width")
        logger.debug(f"Width({comm_param.value})")

    def test_invalid_featurename(self):
        """If the specified feature name is invalid then return None."""
        comm_param = param_answer_timeout = self.__device.get_feature("Xxxxxxxx")
        assert comm_param == None

    def test_get_all_params(self):
        """Get all camera feature."""
        try:
            parameters = self.__device.get_features()
            logger.debug(f"len:{len(parameters)}")

            param = [s for s in parameters if s.name == "Height"]
            assert param != None
            param[0].value
        except pyjds.PyJdsFeatureException as e:
            logger.debug(f"pyjds.PyJdsFeatureException:{e}")

    def test_get_all_params_then_get_invalid_feature(self):
        """Get all camera features.
        Get invalid feature from got params.
        """
        parameters = self.__device.get_features()
        logger.debug(f"len:{len(parameters)}")

        param = [s for s in parameters if s.name == "Invalid"]
        assert len(param) == 0

    def test_get_param_then_get_unavailable_feature(self):
        """Get camera feature.
        Get unavailable feature from got param.
        """
        parameter = self.__device.get_feature("EventAcquisitionTrigger")
        assert parameter != None

        with pytest.raises(pyjds.PyJdsFeatureException) as ex:
            parameter.value
        logger.debug(f"pyjds.PyJdsFeatureException:{ex}")

    def test_get_all_params_then_get_unavailable_feature(self):
        """Get all camera feature.
        Get unavailable feature from got params.
        """
        parameter = self.__device.get_features()
        logger.debug(f"len:{len(parameter)}")
        param = [s for s in parameter if s.name == "ChunkOffsetX"]
        assert len(param) == 1
        with pytest.raises(pyjds.PyJdsFeatureException) as ex:
            param[0].value
        logger.debug(f"ex:{ex}")

    def test_get_readonly_param(self):
        """Get readonly camera feature.
        Check available and readable for true and wretable for false.
        Check that exceptions are raised when setting values.
        """
        parameter = self.__device.get_feature("DeviceSFNCVersionMajor")
        assert parameter.is_available() == True
        assert parameter.is_readable() == True
        assert parameter.is_writable() == False
        logger.debug(f"value:{parameter.value}")
        with pytest.raises(pyjds.PyJdsFeatureException) as einfo:
            logger.debug(f"value:{parameter.value}")
            parameter.value = 2
        logger.debug(f"value:{einfo}")

    def test_get_writable_param(self):
        """Get wraitable camera feature.
        Check available and readable for true and writable for false.
        Check that no exceptions are raised when setting values.
        """
        width_max = self.__device.get_feature("WidthMax")
        param = self.__device.get_feature("Width")
        assert param != None
        assert param.is_available() == True
        assert param.is_readable() == True
        assert param.is_writable() == True
        param.value = width_max.value
        logger.debug(f"value:{param.value}")
