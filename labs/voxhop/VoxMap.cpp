#include "VoxMap.h"
#include "Errors.h"

VoxMap::VoxMap(std::istream& stream) {

}

VoxMap::~VoxMap() {

}

Route VoxMap::route(Point src, Point dst) {
  throw NoRoute(src, dst);
}
