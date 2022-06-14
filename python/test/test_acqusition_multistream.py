from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import sys
import os
import pprint
import logging
import asyncio
from xml.dom.minidom import ProcessingInstruction

from PIL import Image
from my_logger import Logger
import pyjds
import numpy as np

logger = Logger.get_logger(logging.DEBUG)


def task(stream, count: int):
    num = 0
    while num < count:
        buffer = stream.get_buffer(1500)
        image = buffer.get_image()
        logger.info(
            f"channel:{stream.channel} block id: {buffer.block_id} w:{image.width} h: {image.height} ts:{buffer.timestamp} ts:{image.timestamp}"
        )
        num = num + 1


class Test(object):
    @classmethod
    def setup_class(cls):
        logger.debug("@@@ setup_class @@@")

    def setup_method(self, method):
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

    def test_acquisition_threadpool(self):
        self.__device.connect()
        streams = self.__device.create_and_open_streams()
        logger.debug(f"number of stream:{len(streams)}")

        self.__device.acquisition_start()

        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="thread") as executor:
            futures = []
            for stream in streams:
                futures.append(executor.submit(task, stream, 5))

            [f.result() for f in futures]

        self.__device.acquisition_stop()
        self.__device.dis_connect()
