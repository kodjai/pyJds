/********************************************************************
 * @file   mod_exception.hpp
 * @brief
 *
 * @author nma
 * @date   2021.11.9
 * @copyright  Copyright(c) 2021.  JAI Corporation
 *********************************************************************/

#include <stdexcept>
#include <string>

namespace pyjds {
    enum class ModExceptKind {
        InvalidConnectionID,
    };

    class ModException : public std::exception {
    public:
        ModException(ModExceptKind kind, const std::string& msg) :kind_(kind), msg_(msg){}

    private:
        ModExceptKind kind_;
        std::string msg_;
    };
}  // namespace pyjds
