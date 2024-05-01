#include "AST.h"
#include "Nodes.h"

#include <sstream>

AST* AST::parse(const std::string& expression) {
    std::string token;
    std::istringstream stream(expression);

    while(stream >> token) {
        // ...
    }

    // ...
}
