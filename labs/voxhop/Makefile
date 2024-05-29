CXXFLAGS = -g -Wall -Wextra -Werror -std=c++17 -Wno-unused-parameter
CXX      = g++

.PHONY: all clean

test: test.o Point.o Route.o VoxMap.o
	$(CXX) $(CXXFLAGS) -o $@ $+

main: main.o Point.o Route.o VoxMap.o
	$(CXX) $(CXXFLAGS) -o $@ $+


all: main test


main.o: main.cpp Errors.h Route.h VoxMap.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

test.o: test.cpp Errors.h Route.h VoxMap.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<


Point.o: Point.cpp VoxMap.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

Route.o: Route.cpp Route.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

VoxMap.o: VoxMap.cpp VoxMap.h Errors.h Route.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f main test *.o
