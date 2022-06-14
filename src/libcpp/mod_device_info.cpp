/********************************************************************
 * @file   mod_device_info.cpp
 * @brief
 *
 * @author nma
 * @date   2021.11.1
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_device_info.hpp"

#include <chrono>

#include "jaidslog.hpp"
#include "libstatic/found_device_info.hpp"

#include "mod_host_info.hpp"

using namespace std;
namespace pyjds {
    ModDeviceInfo::ModDeviceInfo(std::unique_ptr<jaids::core::FoundDeviceInfo>& device_info)
        : device_info_(move(device_info)) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }

    ModDeviceInfo::~ModDeviceInfo() {
#ifdef CHECK_LEAKED_MEMORY
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }
    std::string ModDeviceInfo::GetConnectionId() const noexcept {
        return device_info_->GetConnectionId();
    }
    std::string ModDeviceInfo::GetDisplayId() const noexcept {
        return device_info_->GetDisplayId();
    }
    std::string ModDeviceInfo::GetManufactureInfo() const noexcept {
        return device_info_->GetManufactureInfo();
    }
    std::string ModDeviceInfo::GetModelName() const noexcept {
        return device_info_->GetModelName();
    }
    std::string ModDeviceInfo::GetSerialNumber() const noexcept {
        return device_info_->GetSerialNumber();
    }
    jaids::DeviceInterfaceTypeEnum ModDeviceInfo::GetType() const noexcept {
        return device_info_->GetDeviceType();
    }
    std::string ModDeviceInfo::GetUniqueId() const noexcept {
        return device_info_->GetUniqueId();
    }
    std::string ModDeviceInfo::GetUserDefinedName() const noexcept {
        return device_info_->GetUserDefinedName();
    }
    std::string ModDeviceInfo::GetVenderName() const noexcept {
        return device_info_->GetVenderName();
    }
    std::string ModDeviceInfo::GetVersion() const noexcept {
        return device_info_->GetVersion();
    }

    std::unique_ptr<ModHostInfo> ModDeviceInfo::GetHostInterface() const noexcept {
        auto ret_value = make_unique<ModHostInfo>(device_info_->GetHostInfo());
        return ret_value;
    }
}  // namespace pyjds