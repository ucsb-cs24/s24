#ifndef ERRORS_H
#define ERRORS_H

#include "Point.h"

class InvalidPoint {
  Point mPoint;
public:
  InvalidPoint(Point point): mPoint(point) {}
  const Point& point() const {return mPoint;}
};

class NoRoute {
  Point mSrc;
  Point mDst;
public:
  NoRoute(Point src, Point dst): mSrc(src), mDst(dst) {}
  const Point& src() const {return mSrc;}
  const Point& dst() const {return mDst;}
};

#endif
