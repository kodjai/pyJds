'''
The purpose of this sample is to show how to find a USB or GigE device, connect and change variables.


'''


import pyjds
import numpy as np
import cv2 as cv



# Auto find cameras
camera=pyjds.DeviceFinder().find()
print("number of cameras : ", len(camera))

# Create device 
test_connect=pyjds.DeviceFactory.create(camera[0])

# Connect 
test_connect.connect()
print("Is connected : ", test_connect.is_connected())

# Get Pixel value
feature_pixel=test_connect.get_feature("PixelFormat")
print(feature_pixel.value_as_str)

# Get and set width of image
feature_width=test_connect.get_feature("Width")
print("original width = ", feature_width.value)
feature_width.value=800
print("new width = ", feature_width.value)

# 0=single mode, 1=multi, 2=continuous
feature_mode=test_connect.get_feature("AcquisitionMode")
feature_mode.value=2
print("mode = ", feature_mode.value)

# create stream  and start acquisition
streams=test_connect.create_and_open_streams()
print("number of stream: ", len(streams))
test_connect.acquisition_start()


# Get parameter node
stream_param=streams[0].get_parameter("Bandwidth")
stream_fps=streams[0].get_parameter("AcquisitionRate")

loop=0

# Get buffer and parameter values while running
while loop <= 10:
    buffer = streams[0].get_buffer()
    print("Block ID ", buffer.block_id)
    loop = loop+1
    print("Bandwidth : ", stream_param.value)
    print("Fps : ", stream_fps.value)

# Cleamup and stop acquisition
del buffer
test_connect.acquisition_stop()
test_connect.dis_connect()
print("End of program")