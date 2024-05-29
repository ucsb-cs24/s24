#include "Point.h"

std::istream& operator >> (std::istream& stream, Point& point) {
  return stream >> point.x >> point.y >> point.z;
}

std::ostream& operator << (std::ostream& stream, const Point& point) {
  return stream << '(' << point.x << ", " << point.y << ", " << point.z << ')';
}
