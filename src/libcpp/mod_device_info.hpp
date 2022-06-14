/********************************************************************
 * @file   mod_device_info.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.1
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once

#include <cstdint>
#include <memory>
#include <string>

#include "jaids/type/device_type.hpp"
#include "libstatic/found_device_info.hpp"
namespace pyjds {
    class ModHostInfo;
    class ModDeviceInfo {
    public:
        ModDeviceInfo(std::unique_ptr<jaids::core::FoundDeviceInfo>& device_info);
        ~ModDeviceInfo();
        std::string GetConnectionId() const noexcept;
        std::string GetDisplayId() const noexcept;
        std::string GetManufactureInfo() const noexcept;
        std::string GetModelName() const noexcept;
        std::string GetSerialNumber() const noexcept;
        jaids::DeviceInterfaceTypeEnum GetType() const noexcept;
        std::string GetUniqueId() const noexcept;
        std::string GetUserDefinedName() const noexcept;
        std::string GetVenderName() const noexcept;
        std::string GetVersion() const noexcept;
        std::unique_ptr<ModHostInfo> GetHostInterface() const noexcept;

    private:
        std::unique_ptr<jaids::core::FoundDeviceInfo> device_info_;
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };

};  // namespace pyjds