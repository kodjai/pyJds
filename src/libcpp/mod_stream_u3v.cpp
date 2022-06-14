/********************************************************************
 * @file   mod_stream_u3v.hpp
 * @brief
 *
 * @author nma
 * @date   2022.02.02
 * @copyright  Copyright(c) 2022.  JAI Corporation
 *********************************************************************/
#include "mod_stream_u3v.hpp"

#include "jaidslog.hpp"
#include "libstatic/stream_u3v.hpp"


using namespace std;
namespace pyjds {
    ModStreamU3V::ModStreamU3V(std::shared_ptr<jaids::core::Stream> stream) : ModStream(stream) {
#ifdef CHECK_LEAKED_MEMORY
        cid_ = chrono::duration_cast<chrono::microseconds>(chrono::system_clock::now().time_since_epoch()).count();
        logger::GetInstance().Debug("{} class_id_ ({})", __FUNCTION__, cid_);
#endif
    }
    ModStreamU3V::~ModStreamU3V() {}

}  // namespace pyjds