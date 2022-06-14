import sys
import os

__version__ = "0.0.5"


def get_pyjds_path() -> str:
    import site

    for path in site.getsitepackages():
        exist = os.path.exists(path + "\\pyjds")
        if exist == True:
            return path + "\\pyjds"

    # for setup develop
    cwd = os.getcwd()
    exist = os.path.exists(cwd + "\\pyjds")
    if exist == True:
        print("\n")
        print(f"*************************************************************")
        print(f"Develop mode!!!!!  pyjds path:{cwd}\\pyjds")
        print(f"*************************************************************")
        return cwd + "\\pyjds"

    return None


path = get_pyjds_path()
if path:
    sys.path.append(path)

ebus_path = "C:\\Program Files\\Common Files\\Pleora\\eBUS SDK"
exist_ebus = os.path.exists(ebus_path)
if exist_ebus == False:
    assert False, 'Install eBUS SDK for JAI before.'
else:
    os.add_dll_directory(ebus_path)

import _module
from .device_gev import *
from .device_u3v import *
from .device_factory import *
from .buffer import *
from .image import *
from .stream import *
from .stream_gev import *
from .device_finder import *
from .enum_feature_type import *
from .feature_enum_entry import *
from .error_pyjds import *

# Init log conf
_module.init_logger(path+"//pyjds.conf")