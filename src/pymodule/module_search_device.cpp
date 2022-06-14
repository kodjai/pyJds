
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "mod_device_finder.hpp"
#include "mod_device_info.hpp"
#include "mod_host_info.hpp"

#include "jaids/type/device_type.hpp"

namespace py = pybind11;
void init_search_device(py::module_& m) {
    // Search device
    py::enum_<jaids::DeviceInterfaceTypeEnum>(m, "DeviceInterfaceType", py::arithmetic())
        .value("GigEVision", jaids::DeviceInterfaceTypeEnum::GigEVision)
        .value("USB3Vision", jaids::DeviceInterfaceTypeEnum::USB3Vision);

    py::class_<pyjds::ModHostInfo, std::unique_ptr<pyjds::ModHostInfo>>(m, "HostInterface")
        .def_property_readonly("display_id", &pyjds::ModHostInfo::GetDisplayId)
        .def_property_readonly("ip_address", &pyjds::ModHostInfo::GetIPAddress)
        .def_property_readonly("mac_address", &pyjds::ModHostInfo::GetMacAddress);

    py::class_<pyjds::ModDeviceInfo, std::unique_ptr<pyjds::ModDeviceInfo>>(m, "DeviceInfo")
        .def_property_readonly("connection_id", &pyjds::ModDeviceInfo::GetConnectionId)
        .def_property_readonly("manufacture_info", &pyjds::ModDeviceInfo::GetManufactureInfo)
        .def_property_readonly("model_name", &pyjds::ModDeviceInfo::GetModelName)
        .def_property_readonly("serial_number", &pyjds::ModDeviceInfo::GetSerialNumber)
        .def_property_readonly("iftype", &pyjds::ModDeviceInfo::GetType)
        .def_property_readonly("unique_id", &pyjds::ModDeviceInfo::GetUniqueId)
        .def_property_readonly("user_define_name", &pyjds::ModDeviceInfo::GetUserDefinedName)
        .def_property_readonly("vendor_name", &pyjds::ModDeviceInfo::GetVenderName)
        .def_property_readonly("version", &pyjds::ModDeviceInfo::GetVersion)
        .def("get_host_interface", &pyjds::ModDeviceInfo::GetHostInterface);

    py::class_<pyjds::ModDeviceFinder>(m, "DeviceFinder")
        .def(py::init<>())
        .def("find", &pyjds::ModDeviceFinder::Find);
}
