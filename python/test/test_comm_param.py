from msilib.schema import Error
import sys
import os
import pprint
import logging

import pytest
from my_logger import Logger
import pyjds
from pyjds.enum_visibility_type import VisibilityType

logger = Logger.get_logger()


class Test(object):
    @classmethod
    def setup_class(cls):
        # logger.debug("@@@ setup_class @@@")
        pass

    def setup_method(self, method):
        logger.debug(f"<<<<< setup ({method.__name__}())>>>>>")
        found_devices = pyjds.DeviceFinder().find()
        logger.debug("number of found device: %s", len(found_devices))
        if len(found_devices) != 0:
            self.__deviceinfo = found_devices[0]
            self.__device = pyjds.DeviceFactory.create(self.__deviceinfo)
        else:
            raise RuntimeError("Not found device")

        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

    def teardown_method(self, method):
        logger.debug(f"<<<<< teardown ({method.__name__}())>>>>>")
        if self.__device.is_connected():
            self.__device.dis_connect()

    @classmethod
    def teardown_class(cls):
        # logger.debug("@@@ teardown_class @@@")
        pass

    def test_expect_success_get_param(self):
        comm_param = param_answer_timeout = self.__device.get_communication_parameter(
            "AnswerTimeout"
        )
        logger.debug(f"AnswerTimeout({comm_param.value})")

    def test_invalid_featurename(self):
        """If the specified feature name is invalid then return None."""
        comm_param = param_answer_timeout = self.__device.get_communication_parameter(
            "ReadMemPacketX"
        )
        assert comm_param == None

    def test_ip_address(self):
        """Get IPAddress feature from cummunication feature without connecting the camera.
        Connectiong to the camera.
        Get GevPrimaryApplicationIPAddress feature from device feature.
        Check to match the IPAddress and the GevPrimaryApplicationIPAddress .
        """
        comm_param_ip_address = (
            param_answer_timeout
        ) = self.__device.get_communication_parameter("IPAddress")
        assert comm_param_ip_address.is_available() == False

        self.__device.connect()
        import ipaddress

        logger.debug(
            f"ip_address:{ipaddress.ip_address(comm_param_ip_address.value).exploded}"
        )

        feature_gev_primary_application_ip_address = self.__device.get_feature(
            "GevPrimaryApplicationIPAddress"
        )
        assert (
            comm_param_ip_address.value
            == feature_gev_primary_application_ip_address.value
        )
        logger.debug(
            f"ip_address:{ipaddress.ip_address(feature_gev_primary_application_ip_address.value).exploded}"
        )

    def test_get_all_params(self):
        """Get all communication parameters."""
        comm_parameters = self.__device.get_communication_parameters()
        logger.debug(f"len:{len(comm_parameters)}")
        param = [s for s in comm_parameters if s.name == "AnswerTimeout"]
        assert param != None
        param[0].value

    def test_get_all_params_then_get_invalid_feature(self):
        """Get all communication parameters.
        Get invalid feature from got params.
        """
        comm_parameters = self.__device.get_communication_parameters()
        logger.debug(f"len:{len(comm_parameters)}")

        param = [s for s in comm_parameters if s.name == "Invalid"]
        assert len(param) == 0

    def test_get_all_params_then_get_unavailable_feature(self):
        """Get all communication parameters.
        Get unavailable feature from got params.
        """
        try:
            comm_parameters = self.__device.get_communication_parameters()
            logger.debug(f"len:{len(comm_parameters)}")

            param_ipaddress = [s for s in comm_parameters if s.name == "IPAddress"]
            assert param_ipaddress != None
            ipaddress = param_ipaddress[0]
            ipaddress.value
        except pyjds.PyJdsFeatureException as e:
            logger.debug(f"pyjds.PyJdsFeatureException:{e}")

    def test_get_readonly_param(self):
        """Get readonly communication param.
        Check available and readable for true and wretable for false.
        Check that exceptions are raised when setting values.
        """
        comm_parameter = self.__device.get_communication_parameter(
            "CommandPendingAcknowledges"
        )
        assert comm_parameter.is_available() == True
        assert comm_parameter.is_readable() == True
        assert comm_parameter.is_writable() == False
        logger.debug(f"value:{comm_parameter.value}")
        with pytest.raises(pyjds.PyJdsFeatureException) as einfo:
            logger.debug(f"value:{comm_parameter.value}")
            comm_parameter.value = 2
        logger.debug(f"value:{einfo}")

    def test_get_writable_param(self):
        """Get wraitable communication param.
        Check available and readable for true and writable for false.
        Check that no exceptions are raised when setting values.
        """
        comm_parameter = self.__device.get_communication_parameter("DefaultMCTT")
        assert comm_parameter != None
        assert comm_parameter.is_available() == True
        assert comm_parameter.is_readable() == True
        assert comm_parameter.is_writable() == True
        comm_parameter.value = comm_parameter.value + 10
        logger.debug(f"value:{comm_parameter.value}")

        comm_parameter2 = self.__device.get_communication_parameter("DefaultMCTT")
        logger.debug(f"value:{comm_parameter2.value}")
