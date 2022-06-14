# Additional explanation of SRS support status

## 3.1	General requirements
### Req 1.0
Need disucussion

### Req 1.1
Restricted by MAC address or USB GUID
However, it can only be determined after the connection is made, so once connected, it will exit as an unsupported device.

### Req 2.0
Support Python3.8 and 3.9.

### Req 2.1
Basically, it can use pyjds by importing only pyjds.
But if it wants to use another library, for exsample numpy, it is necessary to import.
https://github.com/jai-rd/pyJds/blob/e4cc8765a3ff4a731e6a40dbc51818330b3e6449/python/test/test_acqusition.py#L8-L9

### Req 2.2
The pyjds can install using pip from local whl file currently.
It will be upload as Ver1.0 at PyPI repository after the QA evaluation discussion is complete.


## 3.2	Connect and stream
### Req 3.0
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.device_factory.DeviceFactory

#### sample
https://github.com/jai-rd/pyJds/blob/4eb2fb53bde85a29e49ce7223006d1c2029cccf7/python/test/test_acqusition.py#L32-L41

### Req 3.1
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.device_finder.DeviceFinder

### Req 3.2
https://d2ezksrziasiu7.cloudfront.net/v0/003/_build/pyjds.html#pyjds.device_gev.DeviceGEV.create

### Req 3.3
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.device_gev.DeviceGEV.connect

### Req 3.4
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.device_gev.DeviceGEV.connect

### Req 3.5
https://d2ezksrziasiu7.cloudfront.net/v0/003/_build/pyjds.html#pyjds.device_u3v.DeviceU3V.create

### Req 3.6
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.error_pyjds.PyJdsError
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.error_connect.PyJdsConnectError
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.error_visivility.PyJdsVisilityError

### Req 4.0
This library uses only PvStream.
The buffer size will be automatically decide when start acqusition.

### Req 4.1
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.device.Device.create_streams

https://github.com/jai-rd/pyJds/blob/e4cc8765a3ff4a731e6a40dbc51818330b3e6449/python/test/test_acqusition_multistream.py#L52-L67


### Req 4.2
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.device.Device.acquisition_start

### Req 4.3
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.stream.Stream

## 3.3	Access to GenIcam features (parameters and commands)
### Req 5.0, 5.1
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature_bool
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature_enum
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature_enum_entry
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature_float
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature_integer
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature_string

#### sample
https://github.com/jai-rd/pyJds/blob/4eb2fb53bde85a29e49ce7223006d1c2029cccf7/python/test/test_device_feature_bool.py#L30-L49

### Req 5.2
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#module-pyjds.feature_command

### Req 5.3
The eBUS SDK can't access factory parameters.

## 3.4	Access to communication and stream parameters
### Req 6.0, 6.1
It will be similar the GenICam feature access method.
https://d2ezksrziasiu7.cloudfront.net/v0/003/_build/pyjds.html#pyjds.device.Device.get_communication_parameter

## 3.5	Retrieve images and data
### Req 7.0, 7.1
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.stream.Stream.get_image
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.image.Image.data

#### sample
https://github.com/jai-rd/pyJds/blob/4eb2fb53bde85a29e49ce7223006d1c2029cccf7/python/test/test_acqusition.py#L55-L62

### Req 7.2
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.image.Image.data

### Req 7.3
https://d2ezksrziasiu7.cloudfront.net/v0/002/_build/pyjds.html#pyjds.image.Image.chunks

### Req 7.5, 7.6
Not support
It is preferable to use other Python libraries.

## 3.6	GigE Vision specific requirements
Next version.






