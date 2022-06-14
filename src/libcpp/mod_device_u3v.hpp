/********************************************************************
 * @file   mod_device_u3v.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.9
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once

#include "mod_device.hpp"
#include "libstatic/device_u3v.hpp"

#include "mod_stream_u3v.hpp"

namespace pyjds {

    class ModDeviceU3V : public ModDevice {
    public:
        ModDeviceU3V(const std::shared_ptr<jaids::core::DeviceU3V>& camera);
        void Connect() override;
        std::vector<std::unique_ptr<ModStreamU3V>> CreateAndOpenStreams() noexcept;
        std::string GetGUID() const noexcept;
        static std::unique_ptr<ModDeviceU3V> Create(const std::string& connection_id) noexcept;
    private:
        //std::shared_ptr<core::DeviceU3V> device_u3v_;
        std::string name = "CameraU3V";
    };
}  // namespace pyjds