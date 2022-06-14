import sys
import os
import pprint
import logging
import asyncio

from PIL import Image
from my_logger import Logger
import pyjds
import numpy as np

logger = Logger.get_logger()


async def coroutine_acqusition(stream, count: int):
    num = 0
    while num < count:
        buffer = stream.get_buffer(1500)
        logger.info(f"channel:{stream.channel} block id: {buffer.block_id}")
        image = buffer.get_image()
        logger.info(f"w:{image.width} h: {image.height}")
        await asyncio.sleep(1 / 10000)
        num = num + 1


async def coroutine_run(streams):
    tasks = []
    for stream in streams:
        task = asyncio.create_task(coroutine_acqusition(stream, 5))
        tasks.append(task)

    for task in tasks:
        await task


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

    def test_acquisition_task(self):
        self.__device.connect()
        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

        streams = self.__device.create_and_open_streams()
        logger.debug(f"number of stream:{len(streams)}")

        self.__device.acquisition_start()
        asyncio.run(coroutine_run(streams))
        self.__device.acquisition_stop()
        self.__device.dis_connect()
