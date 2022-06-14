/********************************************************************
 * @file   mod_stream_gev.hpp
 * @brief
 *
 * @author nma
 * @date   2022.2.2
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_stream_gev.hpp"

#include <cassert>
#include <chrono>

#include "jaidslog.hpp"
#include "libstatic/buffer.hpp"
#include "libstatic/image.hpp"
#include "libstatic/stream_gev.hpp"

#include "mod_buffer.hpp"


using namespace std;
namespace pyjds {

    ModStreamGEV::ModStreamGEV(std::shared_ptr<jaids::core::Stream> stream) : ModStream(stream) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("{} class_id_ ({})", __FUNCTION__, cid_);
#endif
    }
    ModStreamGEV::~ModStreamGEV() {}

    std::string ModStreamGEV::GetDeviceIPAddress() const noexcept {
        return dynamic_pointer_cast<jaids::core::StreamGEV>(stream_)->GetDeviceIPAddress();
    }

    std::string ModStreamGEV::GetLocalIPAddress() const noexcept {
        return dynamic_pointer_cast<jaids::core::StreamGEV>(stream_)->GetLocalIPAddress();
    }

    uint16_t ModStreamGEV::GetLocaPort() const noexcept {
        return dynamic_pointer_cast<jaids::core::StreamGEV>(stream_)->GetLocaPort();
    }

    uint32_t ModStreamGEV::GetUserModeDataReceiverThreadPriority() const noexcept {
        return dynamic_pointer_cast<jaids::core::StreamGEV>(stream_)->GetUserModeDataReceiverThreadPriority();
    }

    void ModStreamGEV::SetUserModeDataReceiverThreadPriority(uint32_t priority) {
        dynamic_pointer_cast<jaids::core::StreamGEV>(stream_)->SetUserModeDataReceiverThreadPriority(priority);
    }

}  // namespace pyjds