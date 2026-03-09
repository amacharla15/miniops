#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "miniops_cpu.h"

namespace py = pybind11;

PYBIND11_MODULE(_miniops, m) {
    m.doc() = "Native C++ backend for miniops";

    m.def("vector_add", &miniops::vector_add, py::arg("a"), py::arg("b"));
    m.def("topk", &miniops::topk, py::arg("x"), py::arg("k"));
    m.def("softmax", &miniops::softmax, py::arg("x"));
}
