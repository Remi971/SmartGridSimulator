# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(SmartGridSimulator)

set(CMAKE_CXX_STANDARD 17)

# Créer la librairie partagée
add_library(smart_grid SHARED "${CMAKE_CURRENT_SOURCE_DIR}/src/smart_grid.cpp")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include/json.hpp"/include)
target_include_directories(smart_grid PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/build")
