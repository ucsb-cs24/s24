#include "Nodes.h"

#include <sstream>
#include <string>

// This creates the number format the autograder expects:
std::string format(double number) {
  std::ostringstream stream;
  stream << number;
  return stream.str();
}


// Implement your AST subclasses' member functions here.
