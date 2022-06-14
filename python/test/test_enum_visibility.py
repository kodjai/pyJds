import sys

import pytest
from my_logger import Logger
import pyjds
from pyjds.enum_visibility_type import VisibilityType

logger = Logger.get_instance().root_logger("c:\\temp\\a.log")


class TestEnumVisivility(object):
    @classmethod
    def setup_class(cls):
        # logger.debug("@@@ setup_class @@@")
        pass

    def setup_method(self, method):
        # logger.debug("@@@ setup_method @@@")
        pass

    def teardown_method(self, method):
        pass

    @classmethod
    def teardown_class(cls):
        # logger.debug("@@@ teardown_class @@@")
        pass

    # def test_lt_(self):
    #     logger.debug(f"<<<<< {sys._getframe().f_code.co_name} >>>>>")
    #     VisibilityType.from_int(0)

    #     assert VisibilityType.BEGINNER == 0
