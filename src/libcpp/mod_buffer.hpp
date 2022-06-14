/********************************************************************
 * @file   mod_buffer.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.2
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/
#pragma once
#include <cstdint>
#include <memory>
#include <map>

#include "mod_image.hpp"
namespace jaids::core {
    class Buffer;
}
namespace pyjds {
    // class ModImage;
    class ModBuffer {
    public:
        ModBuffer(std::unique_ptr<jaids::core::Buffer>&);
        ~ModBuffer();
        uint64_t GetBlockID() const noexcept;
        std::map<std::string, std::string> GetChunkValues() const noexcept;
        uint32_t GetIgnoredPacketCount() const noexcept;
        std::unique_ptr<ModImage> GetImage(const std::string& conv_type, const uint16_t conv_thread_num);
        uint32_t GetLostPacketCount() const noexcept;
        uint32_t GetPacketOutOfOrderCount() const noexcept;
        uint32_t GetPacketsRecoveredCount() const noexcept;
        uint32_t GetPayloadSize() const noexcept;
        uint64_t GetReceptionTime() const noexcept;
        uint32_t GetResendGroupRequestedCount() const noexcept;
        uint32_t GetResendPacketRequestedCount() const noexcept;
        uint64_t GetTimestamp() const noexcept;

    private:
        std::unique_ptr<jaids::core::Buffer> core_buffer_;
        uint8_t* ndarray_ = nullptr;
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };

}  // namespace pyjds
