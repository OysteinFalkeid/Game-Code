cmake_minimum_required(VERSION 3.27+)
project(MyPythonModule LANGUAGES CXX)

enable_testing()
#include(CTest)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add Pybind11
set(Python_EXECUTABLE "D:/Server/Master/Python/Pygame_skole/.venv/Scripts/python.exe")
find_package(pybind11 REQUIRED PATHS D:/Server/Master/Python/Pygame_skole/.venv/Lib/site-packages/pybind11/share/cmake/pybind11 NO_DEFAULT_PATH)



# Add subdirectories
add_subdirectory(src)
add_subdirectory(python)
# add_subdirectory(tests)