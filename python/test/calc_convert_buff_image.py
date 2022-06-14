import logging
from my_logger import Logger
import pyjds
import numpy as np

logger = Logger.get_logger(logging.DEBUG)


def get_device():
    found_devices = pyjds.DeviceFinder().find()
    logger.debug("number of found device: %s", len(found_devices))
    if len(found_devices) >= 1:
        return found_devices[0]
    else:
        raise Exception


def create_device(device_info):
    return pyjds.DeviceFactory.create(device_info)


def acquire_convert(stream, feature_pixel_format, N, debayer_method, threadnum):
    num = 0
    count = 0
    while num < N:
        import time

        buffer = stream.get_buffer(1500)
        # logger.info(f"block id: {buffer.block_id}")
        start = time.perf_counter()
        image = buffer.get_image(debayer_method=debayer_method, thread_num=threadnum)
        count = count + time.perf_counter() - start
        num = num + 1
    logger.info(
        f"{feature_pixel_format.value} {N} time conversions:{count*1000}ms, average:{count*1000/N:.6f}ms"
    )


def run():
    camera_info = get_device()
    camera = create_device(camera_info)
    camera.connect()

    feature_pixel_format = camera.get_feature("PixelFormat")
    # logger.debug(f"********* pixelformat{feature_pixel_format} *********")
    entries = feature_pixel_format.entries
    feature_width = camera.get_feature("Width")
    feature_width.value = feature_width.range[1]
    feature_height = camera.get_feature("Height")
    feature_height.value = feature_height.range[1]
    logger.debug(
        f"********* w:{feature_width.value} h:{feature_height.value} *********"
    )

    streams = camera.create_and_open_streams()
    logger.debug(f"number of stream:{len(streams)}")

    logger.info(f"*************** DebayerType.SIMPLE, thread_num=1 ***************")
    for entry in entries:
        feature_pixel_format.value = entry

        camera.acquisition_start()
        acquire_convert(
            streams[0], feature_pixel_format, 3, pyjds.DebayerType.SIMPLE, 1
        )
        camera.acquisition_stop()

    logger.info(f"*************** DebayerType.SIMPLE, thread_num=4 ***************")
    for entry in entries:
        feature_pixel_format.value = entry

        camera.acquisition_start()
        acquire_convert(
            streams[0], feature_pixel_format, 3, pyjds.DebayerType.SIMPLE, 4
        )
        camera.acquisition_stop()

    logger.info(f"*************** DebayerType.SIMPLE, thread_num=8 ***************")
    for entry in entries:
        feature_pixel_format.value = entry

        camera.acquisition_start()
        acquire_convert(
            streams[0], feature_pixel_format, 3, pyjds.DebayerType.SIMPLE, 8
        )
        camera.acquisition_stop()

    logger.info(
        f"*************** DebayerType.INTERPOLATION, thread_num=1 ***************"
    )
    for entry in entries:
        feature_pixel_format.value = entry

        camera.acquisition_start()
        acquire_convert(
            streams[0], feature_pixel_format, 3, pyjds.DebayerType.INTERPOLATION, 1
        )
        camera.acquisition_stop()

    logger.info(
        f"*************** DebayerType.INTERPOLATION, thread_num=4 ***************"
    )
    for entry in entries:
        feature_pixel_format.value = entry

        camera.acquisition_start()
        acquire_convert(
            streams[0], feature_pixel_format, 3, pyjds.DebayerType.INTERPOLATION, 4
        )
        camera.acquisition_stop()

    logger.info(
        f"*************** DebayerType.INTERPOLATION, thread_num=8 ***************"
    )
    for entry in entries:
        feature_pixel_format.value = entry

        camera.acquisition_start()
        acquire_convert(
            streams[0], feature_pixel_format, 3, pyjds.DebayerType.INTERPOLATION, 8
        )
        camera.acquisition_stop()

    camera.dis_connect()


if __name__ == "__main__":
    run()
