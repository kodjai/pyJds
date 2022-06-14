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

#include "jaids/exception_feature.hpp"
#include "libstatic/feature.hpp"
#include "libstatic/feature_boolean.hpp"
#include "libstatic/feature_command.hpp"
#include "libstatic/feature_enum.hpp"
#include "libstatic/feature_float.hpp"
#include "libstatic/feature_integer.hpp"
#include "libstatic/feature_string.hpp"



class TestCommParams : public ::testing::Test {
protected:
    // std::unique_ptr<jaids::core::base::pv::CoreVersionImpl> corecersion;
    // データメンバーの初期化
    virtual void SetUp() {}
    virtual void TearDown() {}
    // データメンバー
    jaids::util::Log& log = jaids::util::Log::GetInstance("c:\\jaids.conf");
};


TEST_F(TestCommParams, BeforeConnectGEV) {
    pyjds::ModDeviceFinder finder;
    auto devices = finder.Find(1500);
    ASSERT_TRUE(devices.size() > 0);
    auto camera = pyjds::ModDevice::Create(devices[0]->GetConnectionId(), devices[0]->GetType());

    auto comm_param = camera->GetCommunicationParameter("PreferredTransport");
    EXPECT_EQ(jaids::FeatureTypeEnum::Enumeration, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Expert, comm_param->GetVisibility());
    auto comm_param2 = std::dynamic_pointer_cast<jaids::core::FeatureEnum>(comm_param);
    EXPECT_STREQ("UDP", comm_param->GetValueAsString().c_str());

    comm_param = camera->GetCommunicationParameter("AnswerTimeout");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Beginner, comm_param->GetVisibility());
    auto comm_param_int = std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param);
    EXPECT_EQ(1000, comm_param_int->GetValue());

    comm_param = camera->GetCommunicationParameter("CommandRetryCount");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Beginner, comm_param->GetVisibility());
    comm_param_int = std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param);
    EXPECT_EQ(3, comm_param_int->GetValue());

    comm_param = camera->GetCommunicationParameter("DefaultMCTT");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Beginner, comm_param->GetVisibility());
    comm_param_int = std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param);
    EXPECT_EQ(400, comm_param_int->GetValue());

    comm_param = camera->GetCommunicationParameter("DefaultMCRC");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Beginner, comm_param->GetVisibility());
    comm_param_int = std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param);
    EXPECT_EQ(3, comm_param_int->GetValue());

    comm_param = camera->GetCommunicationParameter("ReadMemPacketSize");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Expert, comm_param->GetVisibility());
    comm_param_int = std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param);
    EXPECT_EQ(552, comm_param_int->GetValue());

    comm_param = camera->GetCommunicationParameter("ReadMemPacketSize");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Expert, comm_param->GetVisibility());
    comm_param_int = std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param);
    EXPECT_EQ(552, comm_param_int->GetValue());

    comm_param = camera->GetCommunicationParameter("IPAddress");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Beginner, comm_param->GetVisibility());
    EXPECT_FALSE(comm_param->IsAvailable());
    EXPECT_THROW(std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param)->GetValue(),
                 jaids::FeatureException);

    comm_param = camera->GetCommunicationParameter("CommandTransport");
    EXPECT_EQ(jaids::FeatureTypeEnum::Enumeration, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Expert, comm_param->GetVisibility());
    EXPECT_FALSE(comm_param->IsAvailable());

    comm_param = camera->GetCommunicationParameter("CommandPort");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Beginner, comm_param->GetVisibility());
    EXPECT_FALSE(comm_param->IsAvailable());

    comm_param = camera->GetCommunicationParameter("MessagingTransport");
    EXPECT_EQ(jaids::FeatureTypeEnum::Enumeration, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Expert, comm_param->GetVisibility());
    EXPECT_FALSE(comm_param->IsAvailable());

    comm_param = camera->GetCommunicationParameter("MessagingPort");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Beginner, comm_param->GetVisibility());
    EXPECT_FALSE(comm_param->IsAvailable());

    comm_param = camera->GetCommunicationParameter("ForcedCommandPortEnabled");
    EXPECT_EQ(jaids::FeatureTypeEnum::Boolean, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Guru, comm_param->GetVisibility());
    auto comm_param_bool = std::dynamic_pointer_cast<jaids::core::FeatureBoolean>(comm_param);
    EXPECT_FALSE(comm_param_bool->GetValue());

    comm_param = camera->GetCommunicationParameter("ForcedMessagingPort");
    EXPECT_EQ(jaids::FeatureTypeEnum::Integer, comm_param->GetType());
    EXPECT_EQ(jaids::VisibilityTypeEnum::Guru, comm_param->GetVisibility());
    EXPECT_FALSE(comm_param->IsAvailable());

    // auto comm_params = camera->GetCommunicationParameters();
    // for (auto& param : comm_params) {
    //    log.Debug("[Test] Comm param name({})", param->GetName());
    //    auto comm_param = camera->GetCommunicationParameter(param->GetName());
    //}
}

TEST_F(TestCommParams, ConnectGEV) {
    pyjds::ModDeviceFinder finder;
    auto devices = finder.Find(1500);
    ASSERT_TRUE(devices.size() > 0);
    auto camera = pyjds::ModDevice::Create(devices[0]->GetConnectionId(), devices[0]->GetType());
    if (camera->GetInterfaceType() != jaids::DeviceInterfaceTypeEnum::GigEVision) return;

    try {
        camera->Connect();
        auto comm_param = camera->GetCommunicationParameter("IPAddress");
        auto comm_param_int = std::dynamic_pointer_cast<jaids::core::FeatureInteger>(comm_param);
        auto v = comm_param_int->GetValue();
        EXPECT_TRUE(comm_param->IsAvailable());
    }
    catch (const std::exception&) {
        camera->DisConnect();
    }
}
