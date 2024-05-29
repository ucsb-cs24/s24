#include "VoxMap.h"
#include "Errors.h"

#include <fstream>
#include <iostream>
#include <sstream>

// TODO: Make this re-prompt for typos!
Point read_point(const char* prompt, std::istream& stream) {
  std::string line;
  Point point;

  while(true) {
    std::cout << prompt;
    if(!std::getline(stream, line)) {
      std::cout << '\n';
      exit(0);
    }

    std::istringstream coords(line);
    if(coords >> point.x >> point.y >> point.z) {
      return point;
    }

    std::cout << "Couldn't read point.  Try again.\n";
  }
}

int main(int argc, char** argv) {
  if(argc != 2) {
    std::cerr << "USAGE: " << argv[0] << " [map-file]\n";
    return 1;
  }

  std::ifstream stream(argv[1]);
  if(stream.fail()) {
    std::cerr << "ERROR: Could not open file: " << argv[1] << '\n';
    return 1;
  }

  VoxMap map(stream);
  stream.close();

  while(true) {
    Point src = read_point("src> ", std::cin);
    Point dst = read_point("dst> ", std::cin);

    try {
      Route route = map.route(src, dst);
      std::cout << route << '\n';
    }
    catch(const InvalidPoint& err) {
      std::cout << "Invalid point: " << err.point() << '\n';
    }
    catch(const NoRoute& err) {
      std::cout << "No route from " << err.src() << " to " << err.dst() << ".\n";
    }
  }

  return 0;
}
