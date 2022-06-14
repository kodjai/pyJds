/********************************************************************
 * @file   mod_device.cpp
 * @brief
 *
 * @author nma
 * @date   2021.11.10
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_device.hpp"
//
#include <stdexcept>
#include <iostream>
#include <memory>

#include "jaids/type/device_type.hpp"
#include "libstatic/found_device_info.hpp"
#include "libstatic/device.hpp"
#include "libstatic/parameters.hpp"
#include "libstatic/stream.hpp"

#include "mod_device_info.hpp"
#include "mod_device_gev.hpp"
#include "mod_device_u3v.hpp"
#include "mod_exception.hpp"
#include "mod_stream.hpp"


using namespace std;
namespace pyjds {
    ModDevice::ModDevice(const std::shared_ptr<jaids::core::Device>& device) : device_(device) {}

    ModDevice::~ModDevice() {
#ifdef CHECK_LEAKED_MEMORY
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }

    void ModDevice::Connect() {}

    void ModDevice::DisConnect() {
        device_->DisConnect();
    }

    const std::string& ModDevice::GetConnectionId() const noexcept {
        return connection_id_;
    }

    jaids::DeviceInterfaceTypeEnum ModDevice::GetInterfaceType() const noexcept {
        return device_->GetInterfaceType();
    }

    bool ModDevice::IsConncted() const noexcept {
        return device_->IsConnected();
    }

    std::unique_ptr<ModDevice> ModDevice::Create(const std::string& connection_id, jaids::DeviceInterfaceTypeEnum type) {
        auto device_info = make_unique<jaids::core::FoundDeviceInfo>(connection_id, type);
        try {
            auto device = jaids::core::Device::Create(device_info);
            if (device->GetInterfaceType() == jaids::DeviceInterfaceTypeEnum::GigEVision) {
                return make_unique<ModDeviceGEV>(dynamic_pointer_cast<jaids::core::DeviceGEV>(device));
            }
            else if (device->GetInterfaceType() == jaids::DeviceInterfaceTypeEnum::USB3Vision) {
                return make_unique<ModDeviceU3V>(dynamic_pointer_cast<jaids::core::DeviceU3V>(device));
            }
            else {
                throw ModException(ModExceptKind::InvalidConnectionID, device_info->GetConnectionId());
            }
        }
        catch (const ModException&) {
            throw;
        }
        catch (const std::exception&) {
            throw ModException(ModExceptKind::InvalidConnectionID, device_info->GetConnectionId());
        }
    }

    std::shared_ptr<jaids::core::CommunicationParameter> ModDevice::GetCommunicationParameter(
        const std::string& parameter_name) noexcept {
        return device_->GetCommunicationParameters()->GetFeature(parameter_name);
    }

    std::vector<std::shared_ptr<jaids::core::CommunicationParameter>> ModDevice::GetCommunicationParameters() noexcept {
        auto params = device_->GetCommunicationParameters()->GetAll();
        return params;
    }

    std::shared_ptr<jaids::core::Feature> ModDevice::GetFeature(const std::string& feature_name) {
        return device_->GetFeatures()->GetFeature(feature_name);
    }

    std::vector<std::shared_ptr<jaids::core::CommunicationParameter>> ModDevice::GetFeatures() noexcept {
        auto params = device_->GetFeatures()->GetAll();
        return params;
    }

    void ModDevice::AcquisitionStart() {
        device_->AcquisitionStart();
    }

    void ModDevice::AcquisitionStop() {
        device_->AcquisitionStop();
    }


}  // namespace pyjds