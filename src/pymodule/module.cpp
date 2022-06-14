#include <string>
#include <cstdint>

#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "mod_buffer.hpp"
#include "mod_device.hpp"
#include "mod_device_gev.hpp"
#include "mod_device_u3v.hpp"
#include "mod_image.hpp"
#include "mod_stream.hpp"
#include "mod_stream_gev.hpp"
#include "mod_stream_u3v.hpp"

#include "jaids/pixel_format.hpp"
#include "jaids/exception_acqusition.hpp"
#include "jaids/exception_connect.hpp"
#include "jaids/exception_feature.hpp"
#include "jaids/exception_stream.hpp"
#include "libstatic/buffer.hpp"
#include "libstatic/image.hpp"
#include "libstatic/stream.hpp"

#include "logger.hpp"

namespace py = pybind11;

void init_search_device(py::module_& m);
void init_feature(py::module_& m);
PYBIND11_MODULE(_module, m) {
    // App Initialize
     m.def("init_logger", [](std::string& confpath) {
         jaids::util::Logger logger;
         logger.Init(confpath);
     });

    // Search device
    init_search_device(m);

    init_feature(m);


    // A simple exception translation:
    auto ex_jds = py::register_exception<jaids::CoreException>(m, "PyJdsExp");
    // A slightly more complicated one that declares MyException5_1 as a subclass of MyException5
    py::register_exception<jaids::FeatureException>(m, "PyFeatureExp", ex_jds.ptr());
    py::register_exception<jaids::ConnectException>(m, "PyConnectExp", ex_jds.ptr());
    py::register_exception<jaids::StreamException>(m, "PyJdsStreamExp", ex_jds.ptr());
    py::register_exception<jaids::AcqusitionException>(m, "PyJdsAcqusitionExp", ex_jds.ptr());


    py::class_<pyjds::ModBuffer, std::unique_ptr<pyjds::ModBuffer>>(m, "Buffer")
        .def_property_readonly("block_id", &pyjds::ModBuffer::GetBlockID)
        .def_property_readonly("lost_packet_count", &pyjds::ModBuffer::GetLostPacketCount)
        .def_property_readonly("packet_out_of_order_count", &pyjds::ModBuffer::GetPacketOutOfOrderCount)
        .def_property_readonly("packet_recoverd_count", &pyjds::ModBuffer::GetPacketsRecoveredCount)
        .def_property_readonly("payload_size", &pyjds::ModBuffer::GetPayloadSize)
        .def_property_readonly("reception_time", &pyjds::ModBuffer::GetReceptionTime)
        .def_property_readonly("resend_group_request_count", &pyjds::ModBuffer::GetResendGroupRequestedCount)
        .def_property_readonly("resend_packet_requested_count", &pyjds::ModBuffer::GetResendPacketRequestedCount)
        .def_property_readonly("timestamp", &pyjds::ModBuffer::GetTimestamp)
        .def("get_chunk_values", &pyjds::ModBuffer::GetChunkValues)
        .def("get_image", &pyjds::ModBuffer::GetImage)
        .def("__repr__", [](const pyjds::ModBuffer& a) { return "<module.Buffer"; });


    py::class_<pyjds::ModImage, std::unique_ptr<pyjds::ModImage>>(m, "Image")
        .def_property_readonly("bpc", &pyjds::ModImage::GetBitsPerComponent)
        .def_property_readonly("block_id", &pyjds::ModImage::GetBlockID)
        .def_property_readonly("height", &pyjds::ModImage::GetHeight)
        .def_property_readonly("reception_time", &pyjds::ModImage::GetReceptionTime)
        .def_property_readonly("timestamp", &pyjds::ModImage::GetTimestamp)
        .def_property_readonly("width", &pyjds::ModImage::GetWidth)
        .def("create_ndarray8",
             [](pyjds::ModImage& image) {
                 auto pixelformat = image.GetPixelFormat();
                 auto dim = pixelformat.IsColor() ? 3 : 1;
                 logger::GetInstance().Debug("<{}> pixelformat({})  IsColor({}) IsBayer({})", __FUNCTION__, pixelformat.GetName(),
                                             pixelformat.IsColor(), pixelformat.IsBayer());
                 logger::GetInstance().Debug("<{}> w({})  h({}) dim({})", __FUNCTION__, image.GetWidth(), image.GetHeight(),
                                             dim);

                 py::array_t<uint8_t> array_{ { (int)image.GetHeight(), (int)image.GetWidth(), dim } };
                 py::buffer_info b = array_.request();
                 const unsigned char* ptr = static_cast<unsigned char*>(b.ptr);
                 memcpy((void*)ptr, image.GetConvertedDataPointer(), (int)image.GetHeight() * (int)image.GetWidth() * dim);
                 return array_;
             })
        .def("create_ndarray16",
             [](pyjds::ModImage& image) {
                 auto pixelformat = image.GetPixelFormat();
                 auto dim = pixelformat.IsColor() ? 3 : 1;
                 py::array_t<uint16_t> array_{ { (int)image.GetHeight(), (int)image.GetWidth(), dim } };
                 py::buffer_info b = array_.request();
                 const unsigned char* ptr = static_cast<unsigned char*>(b.ptr);
                 memcpy((void*)ptr, image.GetConvertedDataPointer(), (int)image.GetHeight() * (int)image.GetWidth() * dim * 2);
                 return array_;
             })
        .def("is_image_dropped", &pyjds::ModImage::IsImageDropped)
        .def("__repr__", [](const pyjds::ModImage& a) { return "<module.Image"; });


    py::class_<pyjds::ModStream>(m, "Stream")
        .def("get_buffer", &pyjds::ModStream::GetBuffer)
        .def("get_feature", &pyjds::ModStream::GetFeature)
        .def("get_features", &pyjds::ModStream::GetFeatures)
        .def_property_readonly("channel", &pyjds::ModStream::GetChannel)
        .def_property_readonly("queued_buffer_count", &pyjds::ModStream::GetQueuedBufferCount)
        .def_property_readonly("queued_buffer_maximun", &pyjds::ModStream::GetQueuedBufferMaximum)
        .def("__repr__", [](const pyjds::ModStream& a) { return "<module.Stream"; });

    py::class_<pyjds::ModStreamGEV, pyjds::ModStream>(m, "StreamGEV")
        .def_property_readonly("device_ip_address", &pyjds::ModStreamGEV::GetDeviceIPAddress)
        .def_property_readonly("local_port", &pyjds::ModStreamGEV::GetLocaPort)
        .def_property_readonly("local_ip_address", &pyjds::ModStreamGEV::GetLocalIPAddress)
        .def_property("thread_priority", &pyjds::ModStreamGEV::GetUserModeDataReceiverThreadPriority,
                      &pyjds::ModStreamGEV::SetUserModeDataReceiverThreadPriority)
        .def("__repr__", [](const pyjds::ModStreamGEV& a) { return "<module.StreamGEV"; });

    py::class_<pyjds::ModStreamU3V, pyjds::ModStream>(m, "StreamU3V").def("__repr__", [](const pyjds::ModStreamU3V& a) {
        return "<module.StreamU3V";
    });


    py::enum_<jaids::AccessTypeEnum>(m, "AccessType", py::arithmetic())
        .value("Control", jaids::AccessTypeEnum::Control)
        .value("Exclusive", jaids::AccessTypeEnum::Exclusive)
        .value("ReadOnly", jaids::AccessTypeEnum::ReadOnly);

    py::class_<pyjds::ModDevice>(m, "Device")
        .def("create", &pyjds::ModDevice::Create)
        .def("dis_connect", &pyjds::ModDevice::DisConnect)
        .def("acquisition_start", &pyjds::ModDevice::AcquisitionStart)
        .def("acquisition_stop", &pyjds::ModDevice::AcquisitionStop)
        .def("get_feature", &pyjds::ModDevice::GetFeature)
        .def("get_features", &pyjds::ModDevice::GetFeatures)
        .def("get_communication_parameter", &pyjds::ModDevice::GetCommunicationParameter)
        .def("get_communication_parameters", &pyjds::ModDevice::GetCommunicationParameters)
        .def("is_connected", &pyjds::ModDevice::IsConncted)
        .def_property_readonly("connection_id", &pyjds::ModDevice::GetConnectionId)
        .def_property_readonly("interface_type", &pyjds::ModDevice::GetInterfaceType)
        .def("__repr__", [](const pyjds::ModDevice& a) { return "<module.DeviceGEV named:" + a.GetConnectionId() + " > "; });

    py::class_<pyjds::ModDeviceGEV, pyjds::ModDevice>(m, "DeviceGEV")
        .def("create_gev", &pyjds::ModDeviceGEV::Create)
        .def("connect", static_cast<void (pyjds::ModDeviceGEV::*)(jaids::AccessTypeEnum)>(&pyjds::ModDeviceGEV::Connect))
        .def("create_and_open_streams", &pyjds::ModDeviceGEV::CreateAndOpenStreams)
        .def_property_readonly("ip_address", &pyjds::ModDeviceGEV::GetIPAddress)
        .def_property_readonly("mac_address", &pyjds::ModDeviceGEV::GetMACAddress)
        .def("__repr__",
             [](const pyjds::ModDeviceGEV& a) { return "<module.DeviceGEV named::" + a.GetConnectionId() + " > "; });

    py::class_<pyjds::ModDeviceU3V, pyjds::ModDevice>(m, "DeviceU3V")
        .def("create_u3v", &pyjds::ModDeviceU3V::Create)
        .def("connect", &pyjds::ModDeviceU3V::Connect)
        .def("create_and_open_streams", &pyjds::ModDeviceU3V::CreateAndOpenStreams)
        .def_property_readonly("guid", &pyjds::ModDeviceU3V::GetGUID);
}