#include <gtest/gtest.h>

#include <map>
#include <string>
#include <fstream>
#include <filesystem>
#include <memory>

#include "jaidslog.hpp"
#include "util_converter.hpp"
#include "mod_image.hpp"

#include "jaids/pixel_format.hpp"
#include "feature.hpp"

class TestUTConverter : public ::testing::Test {
protected:
    // std::unique_ptr<jaids::core::base::pv::CoreVersionImpl> corecersion;
    // データメンバーの初期化
    virtual void SetUp() {}
    virtual void TearDown() {
        log.DumpBacktrace();
    }
    // データメンバー
    jaids::util::Log& log = jaids::util::Log::GetInstance("c:\\jaids.conf");
};


TEST_F(TestUTConverter, ConvertPf) {
    auto pf = jaids::pixelformat::PixelFormat::Create(0x01080001);  // Mono8
    auto cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "Mono8");

    pf = jaids::pixelformat::PixelFormat::Create(0x01100003);  // Mono10
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "Mono16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010A0046);  // Mono10p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "Mono16");

    pf = jaids::pixelformat::PixelFormat::Create(0x01100005);  // Mono12
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "Mono16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0047);  // Mono12p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "Mono16");


    pf = jaids::pixelformat::PixelFormat::Create(0x0108000B);  // BayerBG8
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB8");

    pf = jaids::pixelformat::PixelFormat::Create(0x0110000F);  // BayerBG10
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010A0052);  // BayerBG10p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x01100013);  // BayerBG12
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0053);  // BayerBG12p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x0108000A);  // BayerGB8
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB8");

    pf = jaids::pixelformat::PixelFormat::Create(0x0110000E);  // BayerGB10
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010A0054);  // BayerGB10p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x01100012);  // BayerGB12
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0055);  // BayerGB12p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x01080008);  // BayerGR8
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB8");

    pf = jaids::pixelformat::PixelFormat::Create(0x0110000C);  // BayerGR10
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010A0056);  // BayerGR10p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x01100010);  // BayerGR12
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0057);  // BayerGR12p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x01080009);  // BayerRG8
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB8");

    pf = jaids::pixelformat::PixelFormat::Create(0x0110000D);  // BayerRG10
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010A0058);  // BayerRG10p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x01100011);  // BayerRG12
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0059);  // BayerRG12p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x02200016);  // RGBa8
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGBa8");

    pf = jaids::pixelformat::PixelFormat::Create(0x0240005F);  // RGBa10
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGBa16");

    pf = jaids::pixelformat::PixelFormat::Create(0x02280060);  // RGBa10p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGBa16");

    pf = jaids::pixelformat::PixelFormat::Create(0x02400061);  // RGBa12
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGBa16");

    pf = jaids::pixelformat::PixelFormat::Create(0x02300062);  // RGBa12p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGBa16");

    pf = jaids::pixelformat::PixelFormat::Create(0x02180014);  // RGB8
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB8");

    pf = jaids::pixelformat::PixelFormat::Create(0x02300018);  // RGB10
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x021E005C);  // RGB10p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x0220001D);  // RGB10p32
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x0230001A);  // RGB12
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x0224005D);  // RGB12p
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0004);  // Mono10Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "Mono16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0006);  // Mono12Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "Mono16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0029);  // BayerBG10Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C002D);  // BayerBG12Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0028);  // BayerGB10Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C002C);  // BayerGB12Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0026);  // BayerGR10Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C002A);  // BayerGR12Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C0027);  // BayerRG10Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x010C002B);  // BayerRG12Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x0220001C);  // RGB10V1Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");

    pf = jaids::pixelformat::PixelFormat::Create(0x02240034);  // RGB12V1Packed
    cpf = pyjds::UtilConverter::GetConvertedPixelFormat(pf);
    EXPECT_EQ(cpf.GetName(), "RGB16");
}
