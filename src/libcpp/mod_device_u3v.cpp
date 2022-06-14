/********************************************************************
 * @file   mod_device_u3v.cpp
 * @brief
 *
 * @author nma
 * @date   2021.11.9
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_device_u3v.hpp"

#include <cassert>

#include "jaidslog.hpp"
#include "libstatic/device_u3v.hpp"

#include "mod_stream_u3v.hpp"

using namespace std;
namespace pyjds {

    ModDeviceU3V::ModDeviceU3V(const std::shared_ptr<jaids::core::DeviceU3V>& device) : ModDevice(device) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }

    void ModDeviceU3V::Connect() {
        dynamic_pointer_cast<jaids::core::DeviceU3V>(device_)->Connect();
    }

    std::vector<std::unique_ptr<ModStreamU3V>> ModDeviceU3V::CreateAndOpenStreams() noexcept {
        std::vector<std::unique_ptr<ModStreamU3V>> streams;
        auto core_streams = dynamic_pointer_cast<jaids::core::DeviceU3V>(device_)->CreateAndOpenStreams();
        for (auto& core_stream : core_streams) {
            auto mod_stream = make_unique<ModStreamU3V>(core_stream);
            streams.push_back(move(mod_stream));
        }
        return streams;
    }

    std::string ModDeviceU3V::GetGUID() const noexcept {
        return dynamic_pointer_cast<jaids::core::DeviceU3V>(device_)->GetUUID();
    }

    std::unique_ptr<ModDeviceU3V> ModDeviceU3V::Create(const std::string& connection_id) noexcept {
        auto device = make_shared<jaids::core::DeviceU3V>(connection_id);
        return make_unique<ModDeviceU3V>(dynamic_pointer_cast<jaids::core::DeviceU3V>(device));
    }
}  // namespace pyjds