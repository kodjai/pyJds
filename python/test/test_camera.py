import sys
import os
import pprint

import pytest
import logging
from my_logger import Logger
import pyjds
from pyjds.device_gev import DeviceGEV
from pyjds.enum_visibility_type import VisibilityType

logger = Logger.get_logger()


class Test(object):
    @classmethod
    def setup_class(cls):
        logger.debug("@@@ setup_class @@@")

    def setup_method(self, method):
        # logger.debug("@@@ setup_method @@@")
        found_devices = pyjds.DeviceFinder().find()
        logger.debug("number of found device: %s", len(found_devices))

        self.__found_device = None
        if len(found_devices) >= 1:
            self.__found_device = found_devices[0]
            logger.debug(f"connect to {found_devices[0].connection_id}")
            self.__device = pyjds.DeviceFactory.create(found_devices[0])
        else:
            raise Exception

    def teardown_method(self, method):
        logger.debug("@@@ teardown_method @@@")
        if self.__device.is_connected():
            self.__device.dis_connect()

    @classmethod
    def teardown_class(cls):
        logger.debug("@@@ teardown_class @@@")

    def test(self):
        finder = pyjds.DeviceFinder()
        found_devices = finder.find()
        logger.debug("number of found device: %s", len(found_devices))

        for item in found_devices:
            self.__device.connect()
            logger.debug(f"device ({type(self.__device)})")
            logger.debug(f"interface type({self.__device.interface_type})")
            feature_device_tl = self.__device.get_feature("DeviceTLType")
            # feature_device_tl is feature_enum
            if item.interface_type == pyjds.InterfaceType.GigEVision:
                interface_type_value = "GigEVision"
                logger.debug(f"ip_addr({self.__device.ip_address})")
                logger.debug(f"mac_addr({self.__device.mac_address})")
            else:
                interface_type_value = "USB3Vision"
                logger.debug(f"GUID({self.__device.guid})")
            assert feature_device_tl.value_as_str == interface_type_value

            feature = self.__device.get_feature("DeviceManufacturerInfo")
            assert feature.value == item.manufacture_info
            feature = self.__device.get_feature("DeviceModelName")
            assert feature.value == item.model_name
            feature = self.__device.get_feature("DeviceSerialNumber")
            assert feature.value == item.serial_number
            feature = self.__device.get_feature("DeviceUserID")
            assert feature.value == item.user_id
            feature = self.__device.get_feature("DeviceVendorName")
            assert feature.value == item.vendor_name
            feature = self.__device.get_feature("DeviceVersion")
            assert feature.value == item.device_version

            self.__device.dis_connect()

    def test_create_gev_using_connection_id(self):
        if self.__found_device == None:
            return

        camera = pyjds.DeviceGEV.create(self.__found_device.connection_id)
        camera.connect()
        feature = camera.get_feature("DeviceModelName")
        logger.info(f"DeviceModelName({feature.value})")

    def test_create_gev_using_user_id(self):
        if self.__found_device == None:
            return

        if not self.__found_device.user_id:
            return

        camera = pyjds.DeviceGEV.create(self.__found_device.user_id)
        camera.connect()
        feature = camera.get_feature("DeviceModelName")
        logger.info(f"DeviceModelName({feature.value})")
