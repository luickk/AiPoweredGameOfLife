cmake_minimum_required (VERSION 3.8)

project(GameOfLife)

add_library(GameOfLife STATIC gameOfLife.c gameOfLife.h)
