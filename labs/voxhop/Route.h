#ifndef ROUTE_H
#define ROUTE_H

#include <iostream>
#include <vector>

enum Move: unsigned char {
  NORTH = 0,
  EAST  = 1,
  SOUTH = 2,
  WEST  = 3
};

using Route = std::vector<Move>;

std::ostream& operator << (std::ostream& stream, Move move);
std::ostream& operator << (std::ostream& stream, const Route& route);

#endif
