#include "mod_image.hpp"

#include <chrono>

#include "jaidslog.hpp"
#include "jaids/resultcode.hpp"

#include "jaids/exception_pixelconvert.hpp"
#include "libstatic/buffer.hpp"
#include "libstatic/buffer_converter.hpp"
#include "libstatic/image.hpp"
#include "util_converter.hpp"

#include <iostream>

using namespace std;
namespace pyjds {
    ModImage::ModImage(std::unique_ptr<jaids::core::Buffer>& core_buffer, const uint16_t conv_thread_num)
        : core_image_(move(core_buffer->GetImage())) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif

        // core_image_はcore_bufferが削除されると消えてしまう。またcore_bufferは開放しないと画像取得が止まる
        // したがってBufferを解放後もImageの情報にアクセスさせるためコピーする
        block_id_ = core_image_->GetBlockID();
        image_size_ = core_image_->GetImageSize();
        image_droped_ = core_image_->IsImageDropped();
        reception_time_ = core_image_->GetReceptionTime();
        timestamp_ = core_image_->GetTimestamp();
        width_ = core_image_->GetWidth();
        height_ = core_image_->GetHeight();

        auto src_pf = core_image_->GetPixelFormat();
        // ndarray_は非圧縮8bitもしくは16bitだけ有効, mod_image_pf_にndarrayに入るPixelFormatをセット
        mod_image_pf_ = UtilConverter::GetConvertedPixelFormat(src_pf);

        logger::GetInstance().Debug("<{}> src_pixelformat({}), to_pixelformat({})", __FUNCTION__, src_pf.GetName(),
                                    mod_image_pf_.GetName());
        logger::GetInstance().Debug("<{}> width({}) height({}) is bayer({}) is packed({})", __FUNCTION__, width_, height_,
                                    src_pf.IsBayer(), src_pf.IsPacked());

        // In the case of uncompressed RGB or Mono, the same address as RAW data
        if (IsAvailableWithoutConvert(src_pf)) {
            // ndarray_はデストラクタでdelete
            ndarray_ = new uint8_t[core_image_->GetImageSize()];
            memcpy(ndarray_, core_image_->GetDataPointer(), core_image_->GetImageSize());
        }
        else {
            auto component_bytes = mod_image_pf_.GetBitsPerComponent() == 8 ? 1 : 2;
            auto dim = mod_image_pf_.IsColor() ? 3 : 1;
            // ndarray_はデストラクタでdelete
            ndarray_ = new uint8_t[width_ * height_ * dim * component_bytes];
            try {
                auto converter = jaids::core::BufferConverter::CreateConverter(conv_thread_num);
                converter->Convert(ndarray_, core_buffer->GetData(), mod_image_pf_, src_pf, width_, height_);
            }
            catch (const jaids::PixelConvertException& ex) {
                logger::GetInstance().Error("<{}> Failed to convert. Descrition({})", __FUNCTION__, ex.GetErrorMessage());
                delete ndarray_;
                ndarray_ = nullptr;
            }
            catch (const std::exception& ex) {
                logger::GetInstance().Error("<{}> Failed to convert. ({})", __FUNCTION__, ex.what());
                delete ndarray_;
                ndarray_ = nullptr;
            }
        }
    }

    ModImage::ModImage(ModImage&& image) noexcept {
        logger::GetInstance().Debug("~~~>>>>>>>>>>><{}> ndarray_({})", __FUNCTION__, fmt::ptr(ndarray_));
    }

    ModImage::~ModImage() {
#ifdef CHECK_LEAKED_MEMORY
        logger::GetInstance().Debug("<{}> cid_({})", __FUNCTION__, cid_);
#endif
        if (ndarray_) {
            delete ndarray_;
        }
    }

    uint64_t ModImage::GetBlockID() const noexcept {
        return block_id_;
    }

    uint16_t ModImage::GetBitsPerComponent() const noexcept {
        return mod_image_pf_.GetBitsPerComponent();
    }

    uint8_t* ModImage::GetConvertedDataPointer() const {
        if (!ndarray_) {
            logger::GetInstance().Error("<{}> Failed to convert. ({})", __FUNCTION__, "buffer is nullptr");
            throw jaids::PixelConvertException(jaids::ErrCodeDetail::FailedConvert);
        }
        return ndarray_;
    }

    uint32_t ModImage::GetHeight() const noexcept {
        return height_;
    }

    jaids::pixelformat::PixelFormat ModImage::GetPixelFormat() const noexcept {
        return mod_image_pf_;
    }

    uint64_t ModImage::GetReceptionTime() const noexcept {
        return reception_time_;
    }

    uint64_t ModImage::GetTimestamp() const noexcept {
        return timestamp_;
    }

    uint32_t ModImage::GetWidth() const noexcept {
        return width_;
    }

    bool ModImage::IsImageDropped() const noexcept {
        return image_droped_;
    }

    bool ModImage::IsAvailableWithoutConvert(const jaids::pixelformat::PixelFormat& pixelformat) const noexcept {
        if (pixelformat.IsBayer()) return false;
        if (pixelformat.IsPacked()) return false;
        if ((pixelformat.GetBitsPerComponent() != 8) && (pixelformat.GetBitsPerComponent() != 16)) return false;
        return true;
    }
}  // namespace pyjds