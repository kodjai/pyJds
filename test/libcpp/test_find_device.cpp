#include <gtest/gtest.h>

#include <map>
#include <string>
#include <fstream>
#include <filesystem>
#include <memory>

#include "jaidslog.hpp"
#include "mod_device_finder.hpp"
#include "mod_device_info.hpp"
#include "mod_host_info.hpp"

class TestFindDevice : public ::testing::Test {
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


TEST_F(TestFindDevice, FindAll) {
    pyjds::ModDeviceFinder finder;
    auto devices = finder.Find(1500);
    for (auto& device : devices) {
        //auto ip = device->GetHostInterface()->GetIPAddress();
    }

}
