/********************************************************************
 * @file   mod_image.hpp
 * @brief
 *
 * @author nma
 * @date   2022.2.4
 * @copyright  Copyright(c) 2022.  JAI Corporation
 *********************************************************************/
#pragma once
#include <cstdint>
#include <memory>
#include <vector>

#include "libstatic/buffer.hpp"
#include "libstatic/image.hpp"

#include "jaids/pixel_format.hpp"

namespace pyjds {
    class ModImage {
    public:
        /// <summary>
        ///
        /// </summary>
        /// <param name=""></param>
        ModImage(std::unique_ptr<jaids::core::Buffer>&, const uint16_t conv_thread_num);
        ModImage(ModImage&& image) noexcept;
        ~ModImage();
        uint64_t GetBlockID() const noexcept;
        uint16_t GetBitsPerComponent() const noexcept;
        /// <summary>
        /// Data pointer which was converted from RAW.
        /// This pointer is used for ndarray.
        /// </summary>
        /// <returns></returns>
        uint8_t* GetConvertedDataPointer() const;
        /// <summary>
        /// Get the image's height
        /// </summary>
        /// <returns></returns>
        uint32_t GetHeight() const noexcept;
        /// <summary>
        ///
        /// </summary>
        /// <returns></returns>
        jaids::pixelformat::PixelFormat GetPixelFormat() const noexcept;
        uint64_t GetReceptionTime() const noexcept;
        uint64_t GetTimestamp() const noexcept;
        /// <summary>
        /// Get the image's width
        /// </summary>
        /// <returns></returns>
        uint32_t GetWidth() const noexcept;
        bool IsImageDropped() const noexcept;

    private:
        uint8_t* ndarray_ = nullptr;
        // core_image_: eBUSで取得したImage->PvImage相当
        std::unique_ptr<jaids::core::Image> core_image_;
        uint64_t block_id_ = 0;
        uint32_t height_ = 0;
        uint32_t image_size_ = 0;
        bool image_droped_ = false;
        uint64_t reception_time_ = 0;
        uint64_t timestamp_ = 0;
        uint32_t width_ = 0;
        // 0x01080001=Mono8は暫定値, 初期化用の値があった方がbetter
        jaids::pixelformat::PixelFormat mod_image_pf_ = jaids::pixelformat::PixelFormat::Create(0x01080001);
        /// <summary>
        /// ImageConvertなしで利用できるPixelFormatであるか判定
        /// RGB8,RGB16,Mono8,Mono16など8,16bit画像かつPackedでもBayerでもない
        /// Mono10,12はPCとカメラでは表現違うので変換必要
        /// </summary>
        /// <returns></returns>
        bool IsAvailableWithoutConvert(const jaids::pixelformat::PixelFormat& pixelformat) const noexcept;
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };

}  // namespace pyjds
