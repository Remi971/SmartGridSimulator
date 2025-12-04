# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(SmartGridSimulator)

set(CMAKE_CXX_STANDARD 17)

# Créer la librairie partagée
add_library(smart_grid SHARED "/Users/remi.bhagalou/Documents/Remi/projets/SmartGridSimulator/src/smart_grid.cpp")
include_directories("/Users/remi.bhagalou/Documents/Remi/projets/SmartGridSimulator/include/json.hpp"/include)
target_include_directories(smart_grid PUBLIC "/Users/remi.bhagalou/Documents/Remi/projets/SmartGridSimulator/build")
