#include <gtest/gtest.h>

#include <map>
#include <string>
#include <fstream>
#include <filesystem>
#include <memory>

#include "jaidslog.hpp"
#include "mod_device_gev.hpp"
#include "mod_device_finder.hpp"
#include "mod_device_info.hpp"
//#include "mod_host_info.hpp"

#include "libstatic/feature.hpp"
#include "libstatic/parameters.hpp"

class TestDeviceFaeture : public ::testing::Test {
protected:
    // std::unique_ptr<jaids::core::base::pv::CoreVersionImpl> corecersion;
    // データメンバーの初期化
    virtual void SetUp() {
    }
    virtual void TearDown() {
        log.DumpBacktrace();
    }
    // データメンバー
    jaids::util::Log& log= jaids::util::Log::GetInstance("c:\\jaids.conf");
};


TEST_F(TestDeviceFaeture, Width) {
    pyjds::ModDeviceFinder finder;
    auto devices = finder.Find(1500);
    for (auto& device : devices) {
        auto& id = device->GetConnectionId();
        auto device = pyjds::ModDevice::Create(devices[0]->GetConnectionId(), devices[0]->GetType());
        device->Connect();

        auto chunk_image=device->GetFeature("ChunkImage");
        //auto v = feature->GetName();

        //camera.DisConnect();
        device->DisConnect();

    }

}
