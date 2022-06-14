#include "mod_buffer.hpp"

#include <chrono>
#include <memory>

#include "jaidslog.hpp"
#include "libstatic/buffer.hpp"

using namespace std;
namespace pyjds {
    ModBuffer::ModBuffer(std::unique_ptr<jaids::core::Buffer>& buffer) : core_buffer_(move(buffer)) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }

    ModBuffer::~ModBuffer() {
#ifdef CHECK_LEAKED_MEMORY
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
    }

    uint64_t ModBuffer::GetBlockID() const noexcept {
        return core_buffer_->GetBlockID();
    }

    std::map<std::string, std::string> ModBuffer::GetChunkValues() const noexcept {
        logger::GetInstance().Debug("<{}>", __FUNCTION__);
        std::map<std::string, std::string> ret;

        auto chunks = core_buffer_->GetChunkValues();
        for (auto& chunk : chunks) {
            ret.emplace(chunk.first, chunk.second);
        }
        logger::GetInstance().Debug("<{}> chunk count({})", __FUNCTION__,ret.size());
        return ret;
    }

    uint32_t ModBuffer::GetIgnoredPacketCount() const noexcept {
        return core_buffer_->GetIgnoredPacketCount();
    }

    uint64_t ModBuffer::GetReceptionTime() const noexcept {
        return core_buffer_->GetReceptionTime();
    }

    uint32_t ModBuffer::GetResendGroupRequestedCount() const noexcept {
        return core_buffer_->GetResendGroupRequestedCount();
    }

    uint32_t ModBuffer::GetResendPacketRequestedCount() const noexcept {
        return core_buffer_->GetResendPacketRequestedCount();
    }

    uint64_t ModBuffer::GetTimestamp() const noexcept {
        return core_buffer_->GetTimestamp();
    }

    std::unique_ptr<ModImage> ModBuffer::GetImage(const std::string& conv_type, const uint16_t conv_thread_num) {
        logger::GetInstance().Debug("<{}> conv_type({}) conv_thread_num({})", __FUNCTION__, conv_type, conv_thread_num);
        return std::make_unique<ModImage>(core_buffer_, conv_thread_num);
    }

    uint32_t ModBuffer::GetLostPacketCount() const noexcept {
        return core_buffer_->GetLostPacketCount();
    }

    uint32_t ModBuffer::GetPacketOutOfOrderCount() const noexcept {
        return core_buffer_->GetPacketOutOfOrderCount();
    }

    uint32_t ModBuffer::GetPacketsRecoveredCount() const noexcept {
        return core_buffer_->GetPacketsRecoveredCount();
    }

    uint32_t ModBuffer::GetPayloadSize() const noexcept {
        return core_buffer_->GetPayloadSize();
    }
}  // namespace pyjds