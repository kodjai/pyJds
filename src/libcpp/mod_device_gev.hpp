/********************************************************************
 * @file   mod_device_gev.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.10
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once

#include "mod_device.hpp"

#include "jaids/type/access_type.hpp"
#include "libstatic/device_gev.hpp"

#include "mod_stream_gev.hpp"

namespace pyjds {

    class ModDeviceGEV : public ModDevice {
    public:
        ModDeviceGEV(const std::shared_ptr<jaids::core::DeviceGEV>& device);
        void Connect() override;
        void Connect(jaids::AccessTypeEnum access_type);
        std::vector<std::unique_ptr<ModStreamGEV>> CreateAndOpenStreams(
            int16_t usermode_data_receiver_thread_priority=-1);
        std::string GetIPAddress() const noexcept;
        std::string GetMACAddress() const noexcept;
        static std::unique_ptr<ModDeviceGEV> Create(const std::string&) noexcept;

    private:
        std::string name = "CameraGEV";
    };
}  // namespace pyjds