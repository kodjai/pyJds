import sys
import os
import pprint
import ipaddress

import pytest
from PIL import Image
import logging
from my_logger import Logger
import pyjds
from pyjds import stream
from pyjds.error_pyjds import PyJdsStreamException

logger = Logger.get_logger(logging.DEBUG)


class Test(object):
    @classmethod
    def setup_class(cls):
        logger.debug("@@@ setup_class @@@")

    def setup_method(self, method):
        # logger.debug("@@@ setup_method @@@")
        found_devices = pyjds.DeviceFinder().find()
        logger.debug("number of found device: %s", len(found_devices))

        if len(found_devices) >= 1:
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

    def test_stream(self):
        self.__device.connect()

        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

        streams = self.__device.create_and_open_streams()
        self.__device.acquisition_start()

        feature = streams[0].get_parameter("RequestTimeout")
        logger.debug(f"RequestTimeout:{feature.value}")
        assert feature.value != 0

        feature = streams[0].get_parameter("LocalIPAddress")
        logger.debug(f"LocalIPAddress:{feature.value}")
        assert (
            ipaddress.IPv4Address(feature.value).exploded == streams[0].local_ip_address
        )

        feature = streams[0].get_parameter("DeviceIPAddress")
        logger.debug(f"DeviceIPAddress:{feature.value}")
        assert (
            ipaddress.IPv4Address(feature.value).exploded == streams[0].device_ip_adress
        )

        feature = streams[0].get_parameter("DataPort")
        logger.debug(f"DataPort:{feature.value}")
        assert feature.value == streams[0].local_port

        feature = streams[0].get_parameter("Channel")
        logger.debug(f"Channel:{feature.value}")
        assert feature.value == streams[0].channel

        logger.debug(
            f"user_mode_data_receiver_thread_priority:{streams[0].user_mode_data_receiver_thread_priority}"
        )
        assert streams[0].user_mode_data_receiver_thread_priority > 0

        self.__device.acquisition_stop()
        self.__device.dis_connect()

    def test_streams(self):
        self.__device.connect()

        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

        streams = self.__device.create_and_open_streams()
        self.__device.acquisition_start()

        parameters = streams[0].get_parameters()

        assert len(parameters) > 0

        local_ip_address = [s for s in parameters if s.name == "LocalIPAddress"]
        assert (
            ipaddress.IPv4Address(local_ip_address[0].value).exploded
            == streams[0].local_ip_address
        )

        self.__device.acquisition_stop()
        self.__device.dis_connect()

    def test_streams_usermode_data_receiver_thread_priority(self):
        self.__device.connect()

        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

        streams = self.__device.create_and_open_streams(2)
        for stream in streams:
            assert stream.user_mode_data_receiver_thread_priority == 2
        self.__device.dis_connect()

    def test_streams_invalid_usermode_data_receiver_thread_priority(self):
        self.__device.connect()

        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

        with pytest.raises(PyJdsStreamException):
            streams = self.__device.create_and_open_streams(10)
        self.__device.dis_connect()
