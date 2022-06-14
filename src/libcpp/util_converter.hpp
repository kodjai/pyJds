/**
 * @file util_converter.hpp
 * @author nma (nma@jai.com)
 * @brief
 * @version 0.1
 * @date 2022-2-07
 *
 * @copyright Copyright (c) 2022 JAI Corporation
 *
 */

#pragma once

#include <cstdint>
#include <memory>

#include "jaids/pixel_format.hpp"

namespace pyjds {
    class UtilConverter {
    public:
        UtilConverter();
        ~UtilConverter();
        /// <summary>
        /// 変換するPixelFormatを取得
        /// Monoの8bit系ならMono8 or Monoa8、Mono10-16bit系ならMono16 or Monoa16
        /// Colorの8bit系ならRGB8 or RGBa8、Mono10-16bit系ならRGB16 or RGBa16
        /// </summary>
        /// <param name="pf"></param>
        /// <returns></returns>
        static jaids::pixelformat::PixelFormat GetConvertedPixelFormat(const jaids::pixelformat::PixelFormat& pf);
    private:
#ifdef CHECK_LEAKED_MEMORY
        long long cid_;
#endif
    };

}  // namespace pyjds