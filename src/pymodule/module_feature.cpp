
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "libstatic/feature_integer.hpp"
#include "libstatic/feature_float.hpp"
#include "libstatic/feature_boolean.hpp"
#include "libstatic/feature_command.hpp"
#include "libstatic/feature_enum.hpp"
#include "libstatic/feature_enum_entry.hpp"
#include "libstatic/feature_register.hpp"
#include "libstatic/feature_string.hpp"

#include "jaids/exception_feature.hpp"
#include "jaids/type/feature_type.hpp"
#include "jaids/type/visibility_type.hpp"
#include "jaids/type/representation_type.hpp"

#include "mod_device.hpp"


namespace py = pybind11;
void init_feature(py::module_& m) {
    py::enum_<jaids::FeatureTypeEnum>(m, "FeatureType", py::arithmetic())
        .value("BOOLEAN", jaids::FeatureTypeEnum::Boolean)
        .value("COMMAND", jaids::FeatureTypeEnum::Command)
        .value("ENUMERATION", jaids::FeatureTypeEnum::Enumeration)
        .value("FLOAT", jaids::FeatureTypeEnum::Float)
        .value("INTEGER", jaids::FeatureTypeEnum::Integer)
        .value("REGISTER", jaids::FeatureTypeEnum::Register)
        .value("STRING", jaids::FeatureTypeEnum::String)
        .value("UNDEFINED", jaids::FeatureTypeEnum::Undefined);

    py::enum_<jaids::VisibilityTypeEnum>(m, "Visibility", py::arithmetic())
        .value("BEGINNER", jaids::VisibilityTypeEnum::Beginner)
        .value("EXPERT", jaids::VisibilityTypeEnum::Expert)
        .value("GURU", jaids::VisibilityTypeEnum::Guru)
        .value("INVISIBLE", jaids::VisibilityTypeEnum::Invisible)
        .value("UNDEFINED", jaids::VisibilityTypeEnum::Undefined);

    py::class_<jaids::core::Feature, std::shared_ptr<jaids::core::Feature>>(m, "Feature")
        .def_property_readonly("name", &jaids::core::Feature::GetName)
        .def_property_readonly("category", &jaids::core::Feature::GetCategory)
        .def_property_readonly("description", &jaids::core::Feature::GetDescription)
        .def_property_readonly("display_name", &jaids::core::Feature::GetDisplayName)
        .def_property_readonly("tool_tip", &jaids::core::Feature::GetToolTip)
        .def_property_readonly("feature_type", &jaids::core::Feature::GetType)
        .def_property_readonly("visibility", &jaids::core::Feature::GetVisibility)
        .def("is_available", &jaids::core::Feature::IsAvailable)
        .def("is_implemented", &jaids::core::Feature::IsImplemented)
        .def("is_readable", &jaids::core::Feature::IsReadable)
        .def("is_selector", &jaids::core::Feature::IsSelector)
        .def("is_streamable", &jaids::core::Feature::IsStreamable)
        .def("is_writable", &jaids::core::Feature::IsWritable)
        .def("from_string", &jaids::core::Feature::FromString);

    py::enum_<jaids::RepresentationTypeEnum>(m, "RepresentationType", py::arithmetic())
        .value("BOOLEAN", jaids::RepresentationTypeEnum::Boolean)
        .value("HEXNUMBER", jaids::RepresentationTypeEnum::HexNumber)
        .value("LINEAR", jaids::RepresentationTypeEnum::Linear)
        .value("LOGARITHMIC", jaids::RepresentationTypeEnum::Logarithmic)
        .value("PURENUMBER", jaids::RepresentationTypeEnum::PureNumber)
        .value("UNDEFINED", jaids::RepresentationTypeEnum::Undefined);

    py::class_<jaids::core::FeatureInteger, jaids::core::Feature, std::shared_ptr<jaids::core::FeatureInteger>>(
        m, "FeatureInteger")
        .def_property_readonly("increment", &jaids::core::FeatureInteger::GetIncrement)
        .def_property_readonly("range", &jaids::core::FeatureInteger::GetRange)
        .def_property_readonly("unit", &jaids::core::FeatureInteger::GetUnit)
        .def_property("value", &jaids::core::FeatureInteger::GetValue, &jaids::core::FeatureInteger::SetValue)
        .def_property_readonly("representation_type", &jaids::core::FeatureInteger::GetRepresentationType);

    py::class_<jaids::core::FeatureFloat, jaids::core::Feature, std::shared_ptr<jaids::core::FeatureFloat>>(m, "FeatureFloat")
        .def_property_readonly("range", &jaids::core::FeatureFloat::GetRange)
        .def_property_readonly("unit", &jaids::core::FeatureFloat::GetUnit)
        .def_property("value", &jaids::core::FeatureFloat::GetValue, &jaids::core::FeatureFloat::SetValue)
        .def_property_readonly("representation_type", &jaids::core::FeatureFloat::GetRepresentationType);

    py::class_<jaids::core::FeatureBoolean, jaids::core::Feature, std::shared_ptr<jaids::core::FeatureBoolean>>(m,
                                                                                                                "FeatureBool")
        .def_property("value", &jaids::core::FeatureBoolean::GetValue, &jaids::core::FeatureBoolean::SetValue);

    py::class_<jaids::core::FeatureCommand, jaids::core::Feature, std::shared_ptr<jaids::core::FeatureCommand>>(
        m, "FeatureCommand")
        .def("execute", &jaids::core::FeatureCommand::Execute)
        .def("is_done", &jaids::core::FeatureCommand::IsDone);

    py::class_<jaids::core::FeatureRegister, jaids::core::Feature, std::shared_ptr<jaids::core::FeatureRegister>>(
        m, "FeatureRegister");


    py::class_<jaids::core::FeatureEnumEntry, std::unique_ptr<jaids::core::FeatureEnumEntry>>(m, "FeatureEnumEntry")
        .def("is_available", &jaids::core::FeatureEnumEntry::IsAvailable)
        .def_property_readonly("name", &jaids::core::FeatureEnumEntry::GetName)
        .def_property_readonly("description", &jaids::core::FeatureEnumEntry::GetDescription)
        .def_property_readonly("display_name", &jaids::core::FeatureEnumEntry::GetDisplayName)
        .def_property_readonly("tool_tip", &jaids::core::FeatureEnumEntry::GetToolTip)
        .def_property_readonly("visibility", &jaids::core::FeatureEnumEntry::GetVisibility)
        .def_property_readonly("value", &jaids::core::FeatureEnumEntry::GetValue);

    py::class_<jaids::core::FeatureEnum, jaids::core::Feature, std::shared_ptr<jaids::core::FeatureEnum>>(m, "FeatureEnum")
        .def("get_entries", &jaids::core::FeatureEnum::GetEntries)
        .def_property("value", &jaids::core::FeatureEnum::GetValueAsInt64,
                      py::overload_cast<const uint64_t>(&jaids::core::FeatureEnum::SetValue))
        .def_property("value_as_string", &jaids::core::FeatureEnum::GetValueAsString,
                      py::overload_cast<const std::string&>(&jaids::core::FeatureEnum::SetValue));

    py::class_<jaids::core::FeatureString, jaids::core::Feature, std::shared_ptr<jaids::core::FeatureString>>(m,
                                                                                                              "FeatureString")
        .def_property_readonly("max_length", &jaids::core::FeatureString::GetMaxLength)
        .def_property("value", &jaids::core::FeatureString::GetValue, &jaids::core::FeatureString::SetValue);
}
