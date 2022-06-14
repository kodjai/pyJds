/********************************************************************
 * @file   mod_stream.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.29
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#include "mod_stream.hpp"

#include <cassert>
#include <chrono>

#include "jaidslog.hpp"
#include "libstatic/buffer.hpp"
#include "libstatic/image.hpp"
#include "libstatic/parameters.hpp"
#include "libstatic/stream.hpp"

#include "mod_buffer.hpp"

using namespace std;
namespace pyjds {
    ModStream::ModStream(std::shared_ptr<jaids::core::Stream> stream) : stream_(stream) {}

    ModStream::~ModStream() {
#ifdef CHECK_LEAKED_MEMORY
        logger::GetInstance().Debug("{} class_id_ ({})", __FUNCTION__, cid_);
#endif
    }

    std::unique_ptr<ModBuffer> ModStream::GetBuffer(uint32_t timeout_millsec) {
        assert(stream_);
        auto ibuffer = stream_->RetrieveBuffer(timeout_millsec);
        auto buffer = std::make_unique<ModBuffer>(ibuffer);
        return buffer;
    }

    uint16_t ModStream::GetChannel() const noexcept {
        return stream_->GetChannel();
    }

    std::shared_ptr<jaids::core::Feature> ModStream::GetFeature(const std::string& feature_name) {
        return stream_->GetParameters()->GetFeature(feature_name);
    }

    std::vector<std::shared_ptr<jaids::core::Feature>> ModStream::GetFeatures() noexcept {
        auto params = stream_->GetParameters()->GetAll();
        return params;
    }

    uint32_t ModStream::GetQueuedBufferCount() const noexcept {
        return stream_->GetQueuedBufferCount();
    }

    uint32_t ModStream::GetQueuedBufferMaximum() const noexcept {
        return stream_->GetQueuedBufferMaximum();
    }
}  // namespace pyjds