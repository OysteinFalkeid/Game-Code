#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // For STL containers like std::vector
#include "my_module.h"

namespace py = pybind11;

PYBIND11_MODULE(my_python_module, m) {
    m.doc() = "My custom Python module created with Pybind11"; // Optional docstring
    m.def("add", &add, "", py::arg("numb1"), py::arg("numb2"));  // Bind the add method
    m.def("fib", &fib, "",py::arg("numb")); // Bind Fibonacci method
}
