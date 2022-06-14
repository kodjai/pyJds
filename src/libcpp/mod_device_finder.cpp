/********************************************************************
 * @file   mod_device_finder.cpp
 * @brief
 *
 * @author nma
 * @date   2021.11.1
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_device_finder.hpp"

#include <chrono>

#include "libstatic/device_finder.hpp"
#include "mod_device_info.hpp"
#include "logger.hpp"

using namespace std;
namespace pyjds {
    ModDeviceFinder::ModDeviceFinder() {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }
    ModDeviceFinder::~ModDeviceFinder() {
#ifdef CHECK_LEAKED_MEMORY
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }
    std::vector<unique_ptr<ModDeviceInfo>> ModDeviceFinder::Find(uint32_t timeout_ms, bool directed_broadcast) {
        auto finder = jaids::core::DeviceFinder();
        finder.SetSubnetBroadcastEnabled(!directed_broadcast);
        auto cameras = finder.Find(timeout_ms);

        logger::GetInstance().Debug("found camera number({})", cameras.size());
        vector<unique_ptr<ModDeviceInfo>> ret_value;
        for (auto& camera : cameras) {
            auto device_info = make_unique<ModDeviceInfo>(camera);
            ret_value.push_back(move(device_info));
        }
        return ret_value;
    };
}  // namespace pyjds