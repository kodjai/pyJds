/********************************************************************
 * @file   mod_stream_u3v.hpp
 * @brief
 *
 * @author nma
 * @date   2022.02.02
 * @copyright  Copyright(c) 2022.  JAI Corporation
 *********************************************************************/
#pragma once

#include <cstdint>
#include <memory>
#include <vector>

#include "mod_stream.hpp"

namespace pyjds {
    class ModStreamU3V : public ModStream {
    public:
        ModStreamU3V(std::shared_ptr<jaids::core::Stream>);
        ~ModStreamU3V();

    private:
    };
}  // namespace pyjds