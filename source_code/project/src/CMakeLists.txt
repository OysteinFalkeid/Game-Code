

# Add library for the core module
add_library(my_core STATIC my_module.cpp)

target_include_directories(my_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../include)
