/********************************************************************
 * @file   mod_device_gev.cpp
 * @brief
 *
 * @author nma
 * @date   2021.11.10
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_device_gev.hpp"

#include "jaids/exception_stream.hpp"
#include "jaidslog.hpp"

using namespace std;
namespace pyjds {
    ModDeviceGEV::ModDeviceGEV(const std::shared_ptr<jaids::core::DeviceGEV>& device) : ModDevice(device) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }

    void ModDeviceGEV::Connect() {
        dynamic_pointer_cast<jaids::core::DeviceGEV>(device_)->Connect(jaids::AccessTypeEnum::Control);
    }

    void ModDeviceGEV::Connect(jaids::AccessTypeEnum access_type) {
        dynamic_pointer_cast<jaids::core::DeviceGEV>(device_)->Connect(access_type);
    }

    std::vector<std::unique_ptr<ModStreamGEV>> ModDeviceGEV::CreateAndOpenStreams(
        int16_t usermode_data_receiver_thread_priority) {
        std::vector<std::unique_ptr<ModStreamGEV>> streams;
        auto core_streams =
            dynamic_pointer_cast<jaids::core::DeviceGEV>(device_)->CreateAndOpenStreams(usermode_data_receiver_thread_priority);
        for (auto& core_stream : core_streams) {
            auto mod_stream = make_unique<ModStreamGEV>(core_stream);
            streams.push_back(move(mod_stream));
        }
        return streams;
    }

    std::string ModDeviceGEV::GetIPAddress() const noexcept {
        return dynamic_pointer_cast<jaids::core::DeviceGEV>(device_)->GetIPAddress();
    }

    std::string ModDeviceGEV::GetMACAddress() const noexcept {
        return dynamic_pointer_cast<jaids::core::DeviceGEV>(device_)->GetMACAddress();
    }


    std::unique_ptr<ModDeviceGEV> ModDeviceGEV::Create(const std::string& connection_id) noexcept {
        auto device = make_shared<jaids::core::DeviceGEV>(connection_id);
        return make_unique<ModDeviceGEV>(dynamic_pointer_cast<jaids::core::DeviceGEV>(device));
    }

}  // namespace pyjds