#include <gtest/gtest.h>

#include <map>
#include <string>
#include <fstream>
#include <filesystem>
#include <memory>

#include "jaidslog.hpp"
#include "jaids/type/access_type.hpp"

#include "mod_device.hpp"
#include "mod_device_gev.hpp"
#include "mod_device_finder.hpp"
#include "mod_device_info.hpp"
//#include "mod_host_info.hpp"

#include "libstatic/feature.hpp"

class TestDeviceCreate : public ::testing::Test {
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


TEST_F(TestDeviceCreate, GigE) {
    pyjds::ModDeviceFinder finder;
    auto devices = finder.Find(1500);
    for (auto& device : devices) {
        auto id = device->GetConnectionId();
        auto camera = pyjds::ModDevice::Create(device->GetConnectionId(), device->GetType());
        auto camera_gev = std::unique_ptr<pyjds::ModDeviceGEV>(dynamic_cast<pyjds::ModDeviceGEV*>(camera.release()));
        camera_gev->Connect(jaids::AccessTypeEnum::Control);
        auto iftype = camera->GetInterfaceType();

        //auto type = camera->get
        auto feature = camera->GetFeature("Width");
        auto v = feature->GetName();

        camera->DisConnect();

    }

}
