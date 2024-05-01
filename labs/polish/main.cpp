#include <iostream>
#include "AST.h"

// This file provides an interactive read-evaluate-print loop.
// You can change it if you want, but you shouldn't need to.
// You can also write test code in test.cpp.

int main(int argc, char** argv) {
    if(argc > 2) {
        std::cerr << "USAGE: " << argv[0] << " [output-format]\n";
        return 1;
    }

    std::string oformat = (argc == 2)? argv[1] : "value";
    if(oformat != "prefix" && oformat != "postfix" && oformat != "value") {
        std::cerr << "Output format must be prefix, postfix, or value.\n";
        return 1;
    }

    std::cout << "> ";
    std::string line;
    while(std::getline(std::cin, line)) {
        AST* ast = nullptr;

        try {
            ast = AST::parse(line);
        }
        catch(const std::runtime_error& error) {
            std::cout << "Parse error: " << error.what() << "\n> ";
            continue;
        }

        if(ast == nullptr) {
            std::cout << "Parse error: Null AST pointer.\n> ";
            continue;
        }

        try {
            if(oformat == "prefix") {
                std::string result = ast->prefix();
                std::cout << result << '\n';
            }
            else if(oformat == "postfix") {
                std::string result = ast->postfix();
                std::cout << result << '\n';
            }
            else {
                double result = ast->value();
                std::cout << result << '\n';
            }
        }
        catch(const std::runtime_error& error) {
            std::cout << "Runtime error: " << error.what() << '\n';
        }

        delete ast;
        std::cout << "> ";
    }

    return 0;
}
