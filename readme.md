# Python support library

## Purpose of this software
This is a library for controlling the JAI camera using Python. The eBUS SDK is used for direct control of the camera; while this library provides an interface for Python as an upper layer of eBUS SDK.

**Note**: JAI Python Support Library is not a pure Wrapper function of eBUS SDK. It provides a more abstract API.

**Caution**: This project is offered with no technical suport by JAI. You are welcome to post any questions or issues on Github (https://github.com/JAI-public/pyJds/issues).
### Supported Operating System
- Windows 10
## Getting Started
### 1. Download and intall the following: 
- **eBUS SDK for JAI** (https://www.jai.com/support-software/jai-software)
- **Python with pip** (https://www.python.org/downloads/)
  
  **Note**: Python 3.8 and 3.9 are tested with sample codes.

## How to install
Currently it is able to install from only local file.
### Install step
1. Download the whl file from https://github.com/JAI-public/pyJds/releases

2. `pip install ./pyjds-0.0.4-py3-none-win_amd64.whl`
## Start Development

**Note**: Pull requests to JAI pyJds are welcome!
1. Copy your module file “_module.cp38-win_amd64.pyd” into the project. The module file can be found in the following directory: C:¥Users¥yourname¥AppData¥Roaming¥Python¥Python39¥site-packages¥pyjds.

    **Note**: If you use python 3.8, use “_module.cp39-win_amd64.pyd”.
    **Note**: Use following command to find position of site-packages:
              python -c "import site; print (site.getsitepackages())"

2. Link the local pyjds source directory into your python installation.
## Sample Codes
Sample codes are available here: `xxx`

## API Reference

https://github.com/jai-rd/pyJds/releases

## Known Issues
You can find known issues here: https://github.com/JAI-public/pyJds/issues
