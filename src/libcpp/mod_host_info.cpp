/********************************************************************
 * @file   mod_host_info.cpp
 * @brief  
 * 
 * @author nma
 * @date   2021.11.4
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_host_info.hpp"

#include "jaidslog.hpp"
#include "libstatic/host_info.hpp"

using namespace std;
namespace pyjds {
    ModHostInfo::ModHostInfo(std::unique_ptr<jaids::core::HostInfo>& host_info) : host_info_(move(host_info)) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }
    ModHostInfo::~ModHostInfo() {
#ifdef CHECK_LEAKED_MEMORY
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }
    std::wstring ModHostInfo::GetDisplayId() const noexcept {
        return host_info_->GetDisplayId();
    }
    std::string ModHostInfo::GetIPAddress() const noexcept {
        return host_info_->GetIPAddress();
    }
    std::string ModHostInfo::GetMacAddress() const noexcept {
        return host_info_->GetMacAddress();
    };

}  // namespace pyjds