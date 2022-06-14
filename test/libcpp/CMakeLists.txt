
set(TARGET_NAME "testlibcpp")
# C++17利用
cmake_policy(SET CMP0091 NEW)

##################################################################################
# target
##################################################################################
add_executable(${TARGET_NAME})
target_compile_features(${TARGET_NAME} PUBLIC cxx_std_17)
target_sources(${TARGET_NAME}
  PRIVATE
	testmain.cpp
    test_acqisition.cpp
    test_comm_params.cpp
    test_find_device.cpp
    test_device_feature.cpp
    test_device_create.cpp
)

target_link_libraries(${TARGET_NAME} PRIVATE
    pyjaids::libcpp
    jaids::sdkadaptor
	gtest_main
    jaids::libcommon
    jaids::util
    jaids::libstatic
#    C:/Users/nma/AppData/Local/Programs/Python/Python38/libs/python38.lib
)

# except public inteface
target_include_directories(${TARGET_NAME} PRIVATE
    ${PROJECT_SOURCE_DIR}/src
)


##################################################################################
# 3rd-party OSS library
##################################################################################
include(FetchContent)
FetchContent_Declare(
  googletest
  # Specify the commit you depend on and update it regularly.
  URL https://github.com/google/googletest/archive/refs/tags/release-1.11.0.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt On CACHE BOOL "" FORCE)
if(NOT googletest_POPULATED)
  message("Cloning googletest")
  FetchContent_Populate(googletest)
  add_subdirectory(
    ${googletest_SOURCE_DIR}
    ${googletest_BINARY_DIR})
endif()

##################################################################################
# eBUS SDK
##################################################################################
if(MSVC)
target_link_directories(${TARGET_NAME} PRIVATE $ENV{PUREGEV_ROOT}/Libraries)
else()
target_link_directories(${TARGET_NAME} PRIVATE $ENV{PUREGEV_ROOT}/lib)
endif()

include(GoogleTest)
#add_test(NAME run_test COMMAND ${TARGET_NAME})
#gtest_add_tests(TARGET ${TARGET_NAME})
gtest_discover_tests(${TARGET_NAME})