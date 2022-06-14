
#include "util_converter.hpp"

#include "jaidslog.hpp"


using namespace std;
namespace pyjds {
    UtilConverter::UtilConverter() {}
    UtilConverter::~UtilConverter() {}
    jaids::pixelformat::PixelFormat UtilConverter::GetConvertedPixelFormat(const jaids::pixelformat::PixelFormat& pf) {
        
        if (pf.IsColor()) {
            if (pf.HasAlphaChannel()) {
                // 8bit -> RGBa8, 16bit -> RGBa16
                return pf.GetBitsPerComponent() == 8 ? jaids::pixelformat::PixelFormat::Create(0x02200016)
                                                 : jaids::pixelformat::PixelFormat::Create(0x02400064);
            }
            else {
                // 8bit -> RGB8, 16bit -> RGB16
                return pf.GetBitsPerComponent() == 8 ? jaids::pixelformat::PixelFormat::Create(0x02180014)
                                                 : jaids::pixelformat::PixelFormat::Create(0x02300033);
            }
        }
        else {
            // 8bit -> Mono8, 16bit -> Mono16
            return pf.GetBitsPerComponent() == 8 ? jaids::pixelformat::PixelFormat::Create(0x01080001)
                                             : jaids::pixelformat::PixelFormat::Create(0x01100007);
        }

    }

}  // namespace pyjds