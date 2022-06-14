
/********************************************************************
 * @file   mod_device.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.29
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once
#include <string>
#include <memory>
#include <vector>

#include "jaids/type/device_type.hpp"
#include "libstatic/device.hpp"
#include "libstatic/feature.hpp"

#include "mod_device_info.hpp"

namespace pyjds {
    class ModStream;
    class ModDevice {
    public:
        virtual ~ModDevice();
        void DisConnect();
        void AcquisitionStart();
        void AcquisitionStop();
        virtual void Connect();
        std::shared_ptr<jaids::core::CommunicationParameter> GetCommunicationParameter(
            const std::string& parameter_name) noexcept;
        std::vector<std::shared_ptr<jaids::core::CommunicationParameter>> GetCommunicationParameters() noexcept;
        std::shared_ptr<jaids::core::Feature> GetFeature(const std::string& feature_name);
        std::vector<std::shared_ptr<jaids::core::CommunicationParameter>> GetFeatures() noexcept;
        const std::string& GetConnectionId() const noexcept;
        jaids::DeviceInterfaceTypeEnum GetInterfaceType() const noexcept;
        bool IsConncted() const noexcept;
        static std::unique_ptr<ModDevice> Create(const std::string&, jaids::DeviceInterfaceTypeEnum);

    protected:
        ModDevice(const std::shared_ptr<jaids::core::Device>& camera);
        const std::shared_ptr<jaids::core::Device> device_;
        const std::string connection_id_;
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };

}  // namespace pyjds
