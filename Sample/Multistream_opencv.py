'''
The purpose of this code is to shows how to connect to a JAI multi channel camera and show the images from the different channels through opencv

'''

import pyjds
import numpy as np
import cv2 as cv

# multi channel
#Find Camera
camera=pyjds.DeviceFinder().find()
print("number of cameras : ", len(camera))
print(camera[0].connection_id)

# Connect to camera
test_connect=pyjds.DeviceFactory.create(camera[0])
test_connect.connect()


#set autowhitebalance, feature module, enum and enum entry
feature_white=test_connect.get_feature("BalanceWhiteAuto")
print("white visibility = ", feature_white.visibility)
print("white = ", feature_white.description)
print("white = ", feature_white.entries)
print("white available= ", feature_white.is_available())
print("white = ", feature_white.value_as_str)

# Open stream
streams=test_connect.create_and_open_streams()
print("number of streams : ", len(streams))
stream_RGB_fps=streams[0].get_parameter("AcquisitionRate")
stream_NIR_fps=streams[1].get_parameter("AcquisitionRate")

#Start acquisition
test_connect.acquisition_start()


while True:
    # Get image data from the two channels
    RGB = streams[0].get_buffer().get_image().get_data()
    cv.imshow("RGB", RGB)
    #NIR = streams[1].get_buffer().get_image().get_data()
    #cv.imshow("NIR", NIR)

    # Print frames for the two channels
    print("RGB fps : ", stream_RGB_fps.value)
    #print("NIR fps : ", stream_NIR_fps.value)

    # Wait for the user to press 'q' key to stop the recording
    cv.waitKey(1)
    if cv.waitKey(1) == ord('q'):
        break

#cleanup and stop acquisition
cv.destroyAllWindows()
del RGB
del NIR

test_connect.acquisition_stop()
test_connect.dis_connect()

