cmake_minimum_required(VERSION 3.15)
project(miniops LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(PYBIND11_FINDPYTHON ON)

find_package(pybind11 CONFIG REQUIRED)

add_library(miniops_cpu STATIC
    src/cpp/miniops_cpu.cpp
)

set_target_properties(miniops_cpu PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

target_include_directories(miniops_cpu PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp
)

add_executable(miniops_smoke
    src/cpp/smoke_test.cpp
)

target_link_libraries(miniops_smoke PRIVATE miniops_cpu)

pybind11_add_module(_miniops
    src/bindings/bindings.cpp
)

target_link_libraries(_miniops PRIVATE miniops_cpu)

install(TARGETS _miniops LIBRARY DESTINATION miniops)
