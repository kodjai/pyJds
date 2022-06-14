/********************************************************************
 * @file   mod_stream_gev.hpp
 * @brief
 *
 * @author nma
 * @date   2022.02.02
 * @copyright  Copyright(c) 2022.  JAI Corporation
 *********************************************************************/
#pragma once

#include <cstdint>
#include <memory>
#include <vector>

#include "mod_stream.hpp"

namespace jaids::core {
    class StreamGEV;
}
namespace pyjds {
    class ModStreamGEV : public ModStream {
    public:
        ModStreamGEV(std::shared_ptr<jaids::core::Stream>);
        ~ModStreamGEV();

        std::string GetDeviceIPAddress() const noexcept;
        std::string GetLocalIPAddress() const noexcept;
        uint16_t GetLocaPort() const noexcept;
        uint32_t GetUserModeDataReceiverThreadPriority() const noexcept;
        void SetUserModeDataReceiverThreadPriority(uint32_t);

    private:
    };
}  // namespace pyjds