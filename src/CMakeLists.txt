
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")

##################################################################################
# 3rd-party OSS library
##################################################################################
include(FetchContent)
if(PYJAIDS_MASTER_PROJECT)
  message("RUNON_CI:${RUN_CI}")
  if (RUN_CI EQUAL 1)
      FetchContent_Declare(
        jaidsloglib
        GIT_REPOSITORY        https://nmajai:$ENV{GITHUB_TOKEN}@github.com/jai-rd/jai-developer-suite-liblog
        GIT_TAG        develop
      )
  else()
      FetchContent_Declare(
        jaidsloglib
        GIT_REPOSITORY        https://github.com/jai-rd/jaids-utils
        GIT_TAG        v0.0.4
      )
  endif()
  FetchContent_GetProperties(jaidsloglib)
  if(NOT jaidsliblog_POPULATED)
    message("Cloning jaidsloglib")
    FetchContent_Populate(jaidsloglib)
    add_subdirectory(
      ${jaidsloglib_SOURCE_DIR}
      ${jaidsloglib_BINARY_DIR})
  endif()

  FetchContent_Declare(
    jaids-common
    GIT_REPOSITORY        https://github.com/jai-rd/jaids-common
    GIT_TAG        v0.0.7
  )
  FetchContent_GetProperties(jaids-common)
  if(NOT jaids-common_POPULATED)
    message("Cloning jaids-common")
    FetchContent_Populate(jaids-common)
    add_subdirectory(
      ${jaids-common_SOURCE_DIR}
      ${jaids-common_BINARY_DIR})
  endif()

  FetchContent_Declare(
    sdkadaptor
    GIT_REPOSITORY       https://github.com/jai-rd/jaids-sdk-adaptor
    GIT_TAG                   v0.0.8
  )
  FetchContent_GetProperties(sdkadaptor)
  if(NOT sdkadaptor_POPULATED)
    message("Cloning sdkadaptor")
    FetchContent_Populate(sdkadaptor)
    add_subdirectory(
      ${sdkadaptor_SOURCE_DIR}
      ${sdkadaptor_BINARY_DIR})
  endif()

  FetchContent_Declare(
    jaidscore
    GIT_REPOSITORY       https://github.com/jai-rd/jaids-core
    GIT_TAG                   v2.1.2
  )
  FetchContent_GetProperties(jaidscore)
  if(NOT jaidscore_POPULATED)
    message("Cloning jaidscore")
    FetchContent_Populate(jaidscore)
    add_subdirectory(
      ${jaidscore_SOURCE_DIR}
      ${jaidscore_BINARY_DIR})
  endif()

  FetchContent_Declare(
    pybind11
    GIT_REPOSITORY        https://github.com/pybind/pybind11       
    GIT_TAG               v2.8.1
  )
  FetchContent_GetProperties(pybind11)
  if(NOT pybind11_POPULATED)
    message("Cloning pybind11")
    FetchContent_Populate(pybind11)
    add_subdirectory(
      ${pybind11_SOURCE_DIR}
      ${pybind11_BINARY_DIR})
  endif()

endif()

##################################################################################
#sub-dir
##################################################################################
add_subdirectory(libcpp)
add_subdirectory(pymodule)

