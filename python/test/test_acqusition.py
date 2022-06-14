import sys
import os
import pprint

from PIL import Image
import logging
from my_logger import Logger
import pyjds
import numpy as np
import cv2 as cv
import imageio

logger = Logger.get_logger(logging.INFO)


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

    def test_acquisition(self):
        self.__device.connect()
        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

        streams = self.__device.create_and_open_streams()
        logger.debug(f"number of stream:{len(streams)}")

        self.__device.acquisition_start()
        num = 0
        while num < 1:
            buffer = streams[0].get_buffer(1500)
            logger.info(f"block id: {buffer.block_id}")
            chunks = buffer.get_chunk_values()
            logger.info(f"chunk size: {len(chunks)} {chunks}")
            num = num + 1

        self.__device.acquisition_stop()
        self.__device.dis_connect()

    def test_acquisition_getimage(self):
        self.__device.connect()
        logger.debug(f"device ({type(self.__device)})")
        logger.debug(f"interface type({self.__device.interface_type})")

        streams = self.__device.create_and_open_streams()
        logger.debug(f"number of stream:{len(streams)}")

        self.__device.acquisition_start()
        l_buffer = []
        num = 0
        while num < 2:
            buffer = streams[0].get_buffer(1500)
            logger.info(f"block id: {buffer.block_id}")
            image = buffer.get_image(
                debayer_method=pyjds.DebayerType.INTERPOLATION, thread_num=1
            )
            logger.info(f"height: {image.height}")
            data = image.get_data()
            logger.debug(f"ndarray :{type(data)}")
            logger.debug(
                f"ndarray shape:{data.shape} dtype:{data.dtype} dim:{data.ndim} size:{data.size} bytes:{data.nbytes}"
            )
            l_buffer.append(image)
            num = num + 1

        for im in l_buffer:
            logger.info(
                f"type:{type(im)} block_id:{im.block_id} width:{im.width} heihght:{im.height} "
            )
        l_buffer.clear()

        self.__device.acquisition_stop()
        self.__device.dis_connect()

    def test_acquisition_pixelformats(self):
        """acquire image from camera.

        Raises:
            Exception: [description]
        """
        self.__device.connect()
        logger.debug(f"device ({type(self.__device)})")
        logger.info(f"interface type({self.__device.interface_type})")

        streams = self.__device.create_and_open_streams()
        logger.info(f"number of stream:{len(streams)}")

        fearure_pixelformat = self.__device.get_feature("PixelFormat")
        available_pixelformats = fearure_pixelformat.entries
        logger.debug(f"available_pixelformats:{available_pixelformats}")

        for pixelformat in available_pixelformats:
            logger.info(f"pixelformats:{pixelformat}")
            logger.info(f"is_available:{pixelformat.is_available()}")
            logger.debug(f"type pixelformats:{type(pixelformat)}")
            fearure_pixelformat.value = pixelformat

            self.__device.acquisition_start()
            logger.debug("stream channel: %s", streams[0].channel)
            num = 0
            while num < 1:
                buffer = streams[0].get_buffer(1500)
                logger.info(f"block id@buffer:{buffer.block_id}")
                logger.info(
                    f"lost_packet_count:{buffer.lost_packet_count} packet_out_of_order_count:{buffer.packet_out_of_order_count}"
                )
                logger.info(
                    f"packet_recoverd_count:{buffer.packet_recoverd_count} payload_size:{buffer.payload_size}"
                )
                logger.info(
                    f"reception_time:{buffer.reception_time} resend_group_request_count:{buffer.resend_group_request_count}"
                )
                logger.info(
                    f"resend_packet_requested_count:{buffer.resend_packet_requested_count} timestamp:{buffer.timestamp}"
                )
                logger.info(f"********************{pixelformat}********************")
                image = buffer.get_image()
                logger.info(
                    f"block id@image:{image.block_id} width:{image.width} height:{image.height}"
                )
                logger.info(
                    f"reception_time:{image.reception_time} timestamp:{image.timestamp} is_image_dropped:{image.is_image_dropped()}"
                )
                data = image.get_data()
                logger.info(f"ndarray shape:{data.shape} dtype:{data.dtype}")
                num = num + 1

            self.__device.acquisition_stop()
        self.__device.dis_connect()

    def test_acquisition_pixelformats_store_tif(self):
        """acquire image from camera and store tiff image.

        Raises:
            Exception: [description]
        """
        self.__device.connect()
        logger.debug(f"device ({type(self.__device)})")
        logger.info(f"interface type({self.__device.interface_type})")

        # self.__set_image_size_max()
        # self.__set_test_pattern()

        streams = self.__device.create_and_open_streams()
        logger.info(f"number of stream:{len(streams)}")

        fearure_pixelformat = self.__device.get_feature("PixelFormat")
        available_pixelformats = fearure_pixelformat.entries
        logger.info(f"available_pixelformats:{available_pixelformats}")

        if len(streams) > 1:
            feature_source_selector = self.__device.get_feature("SourceSelector")
            logger.info(f"feature_source_selector:{feature_source_selector.value}")
            feature_source_selector.value ="Source0"

        for pixelformat in available_pixelformats:
            logger.info(f"pixelformats:{pixelformat}, is_available:{pixelformat.is_available()}")
            if pixelformat.is_available() == False:
                continue
            fearure_pixelformat.value = pixelformat

            self.__device.acquisition_start()
            logger.debug(f"stream channel: {streams[0].channel}")
            num = 0
            while num < 1:
                data = streams[0].get_buffer(1500).get_image().get_data()
                logger.info(f"shape:{data.shape}")
                num = num + 1
                fname = f'{pixelformat.name}_{num}.tif'
                if data.dtype == np.uint16:
                    imageio.imwrite(fname,data.astype(np.uint16)) 
                else:
                    imageio.imwrite(fname,data) 
            self.__device.acquisition_stop()

        self.__device.dis_connect()


    def test_acquisition_pixelformats_verify_colorbar(self):
        """acquire image from camera and store tiff image.

        Raises:
            Exception: [description]
        """
        self.__device.connect()
        logger.debug(f"device ({type(self.__device)})")
        logger.info(f"interface type({self.__device.interface_type})")

        self.__set_image_size_max()
        self.__set_test_pattern()

        streams = self.__device.create_and_open_streams()
        logger.info(f"number of stream:{len(streams)}")

        fearure_pixelformat = self.__device.get_feature("PixelFormat")
        available_pixelformats = fearure_pixelformat.entries
        logger.info(f"available_pixelformats:{available_pixelformats}")

        for pixelformat in available_pixelformats:
            logger.info(f"pixelformats:{pixelformat}")
            fearure_pixelformat.value = pixelformat

            self.__device.acquisition_start()
            logger.debug(f"stream channel: {streams[0].channel}")
            num = 0
            while num < 1:
                buffer = streams[0].get_buffer(1500)
                image = buffer.get_image()
                data = image.get_data()
                num = num + 1


                verify = VerifyImage(data)
                verify.done()

            self.__device.acquisition_stop()

        self.__device.dis_connect()

    def __set_test_pattern(self):
        feature_test_pattern = self.__device.get_feature("TestPattern")
        if feature_test_pattern == None:
            return
        logger.debug(f"current TestPattern:{feature_test_pattern.value_as_str}")

        entries = feature_test_pattern.entries
        logger.debug(f"len:{len(entries)}")
        is_color = False
        for entry in entries:
            if entry.name == "HorizontalColorBar":
                is_color = True
                break

        if is_color == True:
            feature_test_pattern.from_string("HorizontalColorBar")
        else:
            feature_test_pattern.from_string("GreyHorizontalRamp")

    def __set_image_size_max(self):
        feature_width = self.__device.get_feature("Width")
        assert feature_width != None
        feature_width.value = feature_width.range[1]
        feature_height = self.__device.get_feature("Height")
        assert feature_height != None
        feature_height.value = feature_height.range[1]


class VerifyImage:
    def __init__(self, data: np.ndarray) -> None:
        self.__data = data
        logger.debug(f">>>>>>>>>>>>>>>>>>>>>{data.shape}")
        if data.shape[2] == 1:
            self.__w = data.shape[1] / 512
            self.__is_color = False
        elif data.shape[2] == 3:
            self.__w = data.shape[1] / 16
            self.__is_color = True

    def done(self):
        # Mono
        if self.__is_color == False:
            if self.__data.dtype == np.uint8:
                self.gray_horizontalramp_value8()
            else:
                self.gray_horizontalramp_value16()
        # Color
        else:
            if self.__data.dtype == np.uint8:
                self.colorbar_value8()
            else:
                self.colorbar_value16()

    def gray_horizontalramp_value8(self):
        assert True == np.array_equal(self.__data[0][0], [0])

    def gray_horizontalramp_value16(self):
        assert True == np.array_equal(self.__data[0][0], [0])

    def colorbar_value8(self):
        assert True == np.array_equal(self.__data[0][int(self.__w)], [0xDE, 0xDE, 0xDE])
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 3)], [0xDE, 0xDE, 0x08]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 5)], [0x08, 0xDE, 0xDE]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 7)], [0x08, 0xDE, 0x08]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 9)], [0xDE, 0x08, 0xDE]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 11)], [0xDE, 0x08, 0x08]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 13)], [0x08, 0x08, 0xDE]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 15)], [0x08, 0x08, 0x08]
        )

    def colorbar_value16(self):
        assert True == np.array_equal(
            self.__data[0][int(self.__w)], [0xDE00, 0xDE00, 0xDE00]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 3)], [0xDE00, 0xDE00, 0x0800]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 5)], [0x0800, 0xDE00, 0xDE00]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 7)], [0x0800, 0xDE00, 0x0800]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 9)], [0xDE00, 0x0800, 0xDE00]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 11)], [0xDE00, 0x0800, 0x0800]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 13)], [0x0800, 0x0800, 0xDE00]
        )
        assert True == np.array_equal(
            self.__data[0][int(self.__w * 15)], [0x0800, 0x0800, 0x0800]
        )
