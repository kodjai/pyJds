"""Buffer class acquired from camera

Buffer data and attribute information can be retrieved

.. note::
    Do not hold the buffer for long periods of time.
    User applications should not keep buffers in containers, e.g. lists,
    otherwise image acquisition will fail when there are no more buffers available.   
    If you want to keep the image data, please hold the Image class.


.. seealso::
    The number of buffers can be specified in
    :py:meth:`pyjds.device.Device.acquisition_start`
"""
from typing import Dict
from logging import getLogger, DEBUG, NullHandler, StreamHandler
import _module
from .feature import *
from .enum_debayer_type import *
from .image import *
import numpy


class Buffer:
    """BUffer class."""

    def __init__(self, buffer):
        assert isinstance(buffer, _module.Buffer)
        self.__buffer = buffer
        self.__logger = getLogger(__name__)
        self.__logger.addHandler(NullHandler())
        self.__logger.propagate = True
        self.__image = None

    def __repr__(self) -> str:
        return f"<repr>{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"<str>{self.__class__.__name__}"

    @property
    def block_id(self) -> int:
        """Get block id.

        Returns
        -------
        int
            block id
        """
        return self.__buffer.block_id

    @property
    def lost_packet_count(self) -> int:
        """Get lost packet count.

        Returns
        -------
        int
            lost packet count
        """
        return self.__buffer.lost_packet_count

    @property
    def packet_out_of_order_count(self) -> int:
        """Get packet out of order count.

        Returns
        -------
        int
            packet out of order count
        """
        return self.__buffer.packet_out_of_order_count

    @property
    def packet_recoverd_count(self) -> int:
        """Get packet recoverd count.

        Returns
        -------
        int
            packet recoverd count
        """
        return self.__buffer.packet_recoverd_count

    @property
    def payload_size(self) -> int:
        """Get payload size.

        Returns
        -------
        int
            payload size
        """
        return self.__buffer.payload_size

    @property
    def reception_time(self) -> int:
        """Get reception time.

        Returns
        -------
        int
            reception time
        """
        return self.__buffer.reception_time

    @property
    def resend_group_request_count(self) -> int:
        """Get resend group request count.

        Returns
        -------
        int
            resend group request count
        """
        return self.__buffer.resend_group_request_count

    @property
    def resend_packet_requested_count(self) -> int:
        """Get resend packet requested count.

        Returns
        -------
        int
            resend packet requested count
        """
        return self.__buffer.resend_packet_requested_count

    @property
    def timestamp(self) -> int:
        """Get timestamp

        Returns
        -------
        int
            timestamp
        """
        return self.__buffer.timestamp

    def get_chunk_values(self) -> Dict[str, str]:
        """Get chunk data

        Returns
        -------
        Dict[chunk_name, chunk_value]  chunk_vales

        """
        return self.__buffer.get_chunk_values()

    def get_image(
        self, debayer_method: DebayerType = DebayerType.SIMPLE, thread_num: int = 1
    ):
        """Get image

            Automatically converts the image to Numpy ndarray format.
            If the PixelFormat is Packed, the unpacked result can be obtained;
            if the PixelFormat is 10bit or more, 16bit data will be generated.
            If PixelFormat is Bayer, the specified debayer_method is used;
            if NOPROCESS is specified, the image is output as a Bayer array.
            However, if the PixelFormat is Packed, unpack processing is performed.

        Parameters
        ----------
        debayer_method : DebayerType, optional
            , by default DebayerType.SIMPLE
        thread_num : Number of threads used for the RAW to ndarray conversion process

        Returns
        -------
        Image
            image data
        """

        convert_method = ""
        if debayer_method == DebayerType.SIMPLE:
            convert_method = "SIMPLE"
        elif debayer_method == DebayerType.INTERPOLATION:
            convert_method = "INTERPOLATION"
        elif debayer_method == DebayerType.NOBAYERPROCESS:
            convert_method = "NOBAYERPROCESS"
        else:
            raise AttributeError("Invalid debayer method")

        image = self.__buffer.get_image(convert_method, thread_num)
        return Image(image)
