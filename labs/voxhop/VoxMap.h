#ifndef VOXMAP_H
#define VOXMAP_H

#include <istream>
#include <vector>

#include "Point.h"
#include "Route.h"

class VoxMap {
  // Member Variables


  // Helper Functions


public:
  VoxMap(std::istream& stream);
  ~VoxMap();

  Route route(Point src, Point dst);
};

#endif
