/********************************************************************
 * @file   mod_host_info.hpp
 * @brief  
 * 
 * @author nma
 * @date   2021.11.4
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace jaids::core {
    class HostInfo;
}
namespace pyjds {
    class ModHostInfo {
    public:
        ModHostInfo(std::unique_ptr<jaids::core::HostInfo>& host_info);
        ~ModHostInfo();
        std::wstring GetDisplayId() const noexcept;
        std::string GetIPAddress() const noexcept;
        std::string GetMacAddress() const noexcept;

    private:
        std::unique_ptr<jaids::core::HostInfo> host_info_;
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };

}