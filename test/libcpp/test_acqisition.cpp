#include <gtest/gtest.h>

#include <chrono>
#include <thread>
#include <map>
#include <string>
#include <fstream>
#include <filesystem>
#include <memory>

#include "jaidslog.hpp"
#include "mod_device_gev.hpp"
#include "mod_device_finder.hpp"
#include "mod_device_info.hpp"
#include "mod_image.hpp"
//#include "mod_host_info.hpp"

#include "jaids/exception_stream.hpp"
#include "libstatic/feature.hpp"
#include "libstatic/feature_enum.hpp"
#include "libstatic/feature_enum_entry.hpp"

class TestAcqusition : public ::testing::Test {
protected:
    // std::unique_ptr<jaids::core::base::pv::CoreVersionImpl> corecersion;
    // データメンバーの初期化
    virtual void SetUp() {
        auto& log = jaids::util::Log::GetInstance("c:\\jaids.conf");
        pyjds::ModDeviceFinder finder;
        auto devices = finder.Find(1500);
        ASSERT_TRUE(devices.size() > 0);
        auto device = pyjds::ModDevice::Create(devices[0]->GetConnectionId(), devices[0]->GetType());
        device_gev_ = std::unique_ptr<pyjds::ModDeviceGEV>(dynamic_cast<pyjds::ModDeviceGEV*>(device.release()));
    }
    virtual void TearDown() {
        // device_gev_->AcquisitionStop();
        device_gev_->DisConnect();
    }
    // データメンバー
    std::unique_ptr<pyjds::ModDeviceGEV> device_gev_;
};


TEST_F(TestAcqusition, Acqusition) {
    device_gev_->Connect();

    auto streams = device_gev_->CreateAndOpenStreams();
    device_gev_->AcquisitionStart();

    auto feature_pixelformats = device_gev_->GetFeature("PixelFormat");
    logger::GetInstance().Info("<<<<<<<<<<<Test>>>>>>>>>>> pixelformat({})", feature_pixelformats->GetName());

    try {
        for (auto& stream : streams) {
            auto s = stream->GetChannel();
            for (auto idx = 0; idx < 1; idx++) {
                auto buff = stream->GetBuffer(1500);
                jaids::util::Log::GetInstance().Debug("[Test] block_id({})", buff->GetBlockID());

                auto image = buff->GetImage("SIMPLE", 1);

                // auto xxx = buff->GetConvertedBuffer();
                // auto xxx1 = xxx->GetImage();
                // auto pp = xxx1->GetPixelFormat();
                // auto m_converted_image = buff->GetImage()->GetConvertedBuffer();
                // auto x1 = m_converted_image->GetImage()->GetPixelFormat();
                // auto m_converted_image = buff->GetImage()->GetConvertedImage();
                // auto xx2 =m_converted_image->GetHeight();
                // auto xx = m_converted_image->GetPixelFormat();
            }
        }
    }
    catch (...) {
        auto xxx = 1;
    }
    device_gev_->AcquisitionStop();
}

TEST_F(TestAcqusition, AcqusitionChunk) {
    device_gev_->Connect();

    auto streams = device_gev_->CreateAndOpenStreams();
    device_gev_->AcquisitionStart();

    try {
        for (auto& stream : streams) {
            auto usermode_data_receiver_thread_priority = stream->GetUserModeDataReceiverThreadPriority();
            for (auto idx = 0; idx < 1; idx++) {
                auto buff = stream->GetBuffer(1500);
                jaids::util::Log::GetInstance().Debug("[Test] block_id({})", buff->GetBlockID());

                auto chunks = buff->GetChunkValues();
            }
        }
    }
    catch (...) {
        auto xxx = 1;
    }
    device_gev_->AcquisitionStop();
}

TEST_F(TestAcqusition, AcqusitionAllPixelFormats) {
    device_gev_->Connect();
    auto streams = device_gev_->CreateAndOpenStreams();

    auto feature_pixelformats = device_gev_->GetFeature("PixelFormat");
    auto entries = std::dynamic_pointer_cast<jaids::core::FeatureEnum>(feature_pixelformats)->GetEntries();
    for (auto& entry : entries) {
        if (!entry->IsAvailable()) {
            logger::GetInstance().Info("<Test> unavailable pixelformat({})", entry->GetName());
            continue;
        }
        logger::GetInstance().Info("<Test> pixelformat({})", entry->GetName());
        feature_pixelformats->FromString(entry->GetName());
        device_gev_->AcquisitionStart();

        try {
            for (auto& stream : streams) {
                auto usermode_data_receiver_thread_priority = stream->GetUserModeDataReceiverThreadPriority();
                for (auto idx = 0; idx < 1; idx++) {
                    auto buff = stream->GetBuffer(1500);
                    jaids::util::Log::GetInstance().Debug("[Test] block_id({})", buff->GetBlockID());

                    auto chunks = buff->GetChunkValues();
                }
            }
        }
        catch (...) {
            device_gev_->AcquisitionStop();
            FAIL() << "Failed acquisition";
            break;
        }
        device_gev_->AcquisitionStop();
    }
}
