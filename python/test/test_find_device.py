import pytest
from my_logger import Logger
import pyjds

logger = Logger.get_logger()


class TestFeatureFindDevice(object):
    @classmethod
    def setup_class(cls):
        logger.debug("\n@@@ setup_class @@@")

    def setup_method(self, method):
        logger.debug("\n@@@ setup_method @@@")

    def teardown_method(self, method):
        logger.debug("\n@@@ teardown_method @@@")

    def teardown_class(cls):
        logger.debug("\n@@@ teardown_class @@@")

    def test(self):
        finder = pyjds.DeviceFinder()
        found_devices = finder.find()
        logger.debug("number of found device: %s", len(found_devices))

        for item in found_devices:
            logger.debug("connection_id: %s", item.connection_id)
            logger.debug("interface type: %s", item.interface_type)
            logger.debug("manufacture info: %s", item.manufacture_info)
            logger.debug("model name : %s", item.model_name)
            logger.debug("serial number; %s", item.serial_number)
            logger.debug("user id: %s", item.user_id)
            logger.debug("vendor name: %s", item.vendor_name)
            logger.debug("device version: %s", item.device_version)

            host_interface = item.get_host_interface()
            logger.debug(host_interface.display_id)
