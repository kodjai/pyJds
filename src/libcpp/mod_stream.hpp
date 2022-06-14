/********************************************************************
 * @file   mod_stream.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.29
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once

#include <cstdint>
#include <memory>
#include <vector>

#include "mod_buffer.hpp"
#include "libstatic/feature.hpp"

namespace jaids::core {
    class Stream;
}
namespace pyjds {

    class Buffer;
    class ModStream {
    public:
        ~ModStream();
        std::unique_ptr<ModBuffer> GetBuffer(uint32_t timeout_millsec);
        uint16_t GetChannel() const noexcept;
        std::shared_ptr<jaids::core::Feature> GetFeature(const std::string& feature_name);
        std::vector<std::shared_ptr<jaids::core::Feature>> GetFeatures() noexcept;
        uint32_t GetQueuedBufferCount() const noexcept;
        uint32_t GetQueuedBufferMaximum() const noexcept;

    protected:
        ModStream(std::shared_ptr<jaids::core::Stream>);
        std::shared_ptr<jaids::core::Stream> stream_;
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };
}  // namespace pyjds