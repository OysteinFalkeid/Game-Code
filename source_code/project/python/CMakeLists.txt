# Create a shared library for the Python module
pybind11_add_module(my_python_module bindings.cpp)

target_link_libraries(my_python_module PRIVATE my_core)

# Output directory for the .pyd file
set(PYTHON_MODULE_OUTPUT_DIR ${CMAKE_BINARY_DIR}/python/Release)

set(stubgen_EXECUTABLE "D:/Server/Master/Python/Pygame_skole/.venv/Scripts/stubgen.exe")

# Custom command to generate .pyi file
add_custom_command(
    TARGET my_python_module POST_BUILD
    COMMAND ${stubgen_EXECUTABLE} --include-docstrings -m my_python_module -o ${PYTHON_MODULE_OUTPUT_DIR}
    WORKING_DIRECTORY ${PYTHON_MODULE_OUTPUT_DIR}
    COMMENT "Generating .pyi file for my_python_module"
)
