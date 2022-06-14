/********************************************************************
 * @file   mod_device_finder.hpp
 * @brief  
 * 
 * @author nma
 * @date   2021.11.1
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once

#include <cstdint>
#include <memory>
#include <vector>

namespace pyjds {
    class ModDeviceInfo;
    class ModDeviceFinder {
    public:
        ModDeviceFinder();
        ~ModDeviceFinder();
        /// <summary>
        /// Search devicees
        /// </summary>
        /// <param name="directed_broadcast">If true using directed broadcast else using limited broadcast</param>
        /// <returns></returns>
        std::vector<std::unique_ptr<ModDeviceInfo>> Find(uint32_t timeout_ms,bool directed_broadcast = true);

    private:
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };
};  // namespace pyjds