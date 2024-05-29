#ifndef POINT_H
#define POINT_H

#include <iostream>

struct Point {
  int x;
  int y;
  int z;

  Point() {}
  Point(int x, int y, int z): x(x), y(y), z(z) {}
};

std::istream& operator >> (std::istream& stream, Point& point);
std::ostream& operator << (std::ostream& stream, const Point& point);

#endif
