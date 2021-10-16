#!/usr/bin/env bash
mkdir build
cd build
cmake ..
make
./test/TestGame
