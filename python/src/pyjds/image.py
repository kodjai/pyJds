"""Image class acquired from camera

Image data and attribute information can be retrieved
The image data is represented as a Numpy ndarray type,
which is converted into the appropriate form according to the camera's PixelFormat.
If the PixelFormat is 8bit, the image data will be 8bit; if the PixelFormat is 10 or 12bit,
the image data will be 16bit.
"""
from logging import getLogger, DEBUG, NullHandler, StreamHandler
import _module
from .feature import *
from .enum_debayer_type import *
import numpy


class Image:
    """Image class."""

    def __init__(self, image):
        assert isinstance(image, _module.Image)
        self.__image = image
        self.__logger = getLogger(__name__)
        self.__logger.addHandler(NullHandler())
        self.__logger.propagate = True
        self.__data = None

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
        return self.__image.block_id

    @property
    def height(self) -> int:
        """Get image height.

        Returns
        -------
        int
            height
        """
        return self.__image.height

    @property
    def reception_time(self) -> int:
        """Get reception_time.

        Returns
        -------
        int
            reception_time
        """
        return self.__image.reception_time

    @property
    def timestamp(self) -> int:
        """Get timestamp.

        Returns
        -------
        int
            timestamp
        """
        return self.__image.timestamp

    @property
    def width(self) -> int:
        """Get image width.

        Returns
        -------
        int
            width
        """
        return self.__image.width

    def get_data(self) -> numpy.ndarray:
        """Get image as ndarray.

        Returns
        -------
        numpy.ndarray
            image data as ndarray
        """
        self.__logger.debug(
            f"isinstance numpy.ndarray?:{isinstance(self.__data,numpy.ndarray)}"
        )

        if isinstance(self.__data, numpy.ndarray) == False:
            if self.__image.bpc == 8:
                self.__data = self.__image.create_ndarray8()
            else:
                self.__data = self.__image.create_ndarray16()

        return self.__data

    def is_image_dropped(self) -> bool:
        """Image dropped status.

        Returns
        -------
        True
            the previous frame was dropped.
        False
            otherwise
        """

        return self.__image.is_image_dropped()
