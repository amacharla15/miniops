# miniops

```md
![CI](https://github.com/amacharla15/miniops/actions/workflows/ci.yml/badge.svg)
![Wheels](https://github.com/amacharla15/miniops/actions/workflows/wheels.yml/badge.svg)

miniops is a small C++ and Python tensor-ops package built to learn native library design, Python bindings, packaging, testing, and benchmarking.

The project starts with a Python reference implementation, adds a native CPU backend in C++, exposes that backend to Python with `pybind11`, packages the project with CMake and `scikit-build-core`, verifies native/reference parity with tests, and benchmarks the native backend against the Python reference implementation.

## Why this project exists

This project was built to practice the kind of mixed-language developer tooling work that appears in performance-focused library engineering:

- implement correct behavior in a simple reference layer
- move performance-critical logic into native C++
- expose native code cleanly to Python users
- package the project like a real installable library
- verify correctness with parity tests
- measure the actual performance impact of the native backend

## Features

- Python reference backend for `vector_add`, `topk`, and `softmax`
- Native CPU backend in C++
- Python bindings with `pybind11`
- CMake-based native build
- Packaging through `pyproject.toml` and `scikit-build-core`
- Native/reference parity testing
- Benchmark harness with CSV output
- Benchmark analysis with speedup and time reduction summaries

## Distribution and automation

The project now supports multiple distribution and validation paths:

- **Editable/source install** through `pyproject.toml`, `scikit-build-core`, and CMake
- **Cross-platform CI** through GitHub Actions on Linux and Windows
- **Wheel artifact builds** through a dedicated GitHub Actions workflow
- **Conda recipe support** through `conda/recipe/meta.yaml`

### CI

The repository includes automated test workflows that validate the package across:

- Linux
- Windows
- multiple Python versions

This helps catch packaging, native build, and test regressions in clean environments.

### Wheels

A dedicated wheel-building workflow generates downloadable wheel artifacts in GitHub Actions for Linux and Windows.

This proves the package is not only installable from source, but can also be produced as a binary distribution artifact.

### Conda

The repository also includes a Conda recipe:

```text
conda/recipe/meta.yaml

## Architecture

The project has three main layers:

### 1. Python reference layer
The reference implementation lives in `src/miniops/reference.py`.

Its job is to define the intended behavior clearly and act as the correctness oracle for the native backend.

### 2. Native C++ CPU core
The native backend lives in `src/cpp/miniops_cpu.h` and `src/cpp/miniops_cpu.cpp`.

It implements the same operations as the Python reference layer using C++ and STL containers.

### 3. Python binding layer
The binding layer lives in `src/bindings/bindings.cpp`.

It uses `pybind11` to expose the native C++ functions as an internal compiled Python module named `_miniops`.

The public package API remains:

```python
import miniops

miniops.vector_add(a, b)
miniops.topk(x, k)
miniops.softmax(x)

Internally, src/miniops/__init__.py loads the native backend when available and falls back to the Python reference backend otherwise.

Project layout
miniops/
  README.md
  pyproject.toml
  CMakeLists.txt
  src/
    miniops/
      __init__.py
      reference.py
    cpp/
      miniops_cpu.h
      miniops_cpu.cpp
      smoke_test.cpp
    bindings/
      bindings.cpp
  tests/
    test_backend.py
    test_reference.py
    test_parity.py
  benchmarks/
    benchmark_ops.py
    analyze_benchmarks.py
  results/
    phase6/
      benchmark_results.csv
    phase7/
      benchmark_summary.csv
      benchmark_summary.md
Build and install

This project was developed in VS Code using WSL on Ubuntu.

Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
Install system dependencies
sudo apt update
sudo apt install -y build-essential cmake ninja-build gdb python3-dev git
Install Python dependencies
pip install --upgrade pip
pip install numpy pytest pybind11
Install the package in editable mode
pip install -e .
Running the package
python -c "import miniops; print(miniops.BACKEND); print(miniops.vector_add([1, 2], [3, 4]))"

Expected output should show that the active backend is native.

Testing

The project includes three layers of testing:

tests/test_reference.py checks the reference implementation

tests/test_backend.py verifies that the native backend is active

tests/test_parity.py checks that the native backend matches the Python reference implementation across normal cases, numeric cases, and failure cases

Run all tests with:

pytest
Benchmarking

The benchmark harness compares the Python reference backend against the native C++ backend for:

vector_add

topk

softmax

The benchmark uses:

warmup runs

repeated measurements

multiple input sizes

CSV result storage

Run the raw benchmark:

python benchmarks/benchmark_ops.py

This writes raw benchmark results to:

results/phase6/benchmark_results.csv

Run the benchmark analysis:

python benchmarks/analyze_benchmarks.py

This writes:

results/phase7/benchmark_summary.csv
results/phase7/benchmark_summary.md
Benchmark summary

The native backend outperformed the Python reference implementation in every tested case.

operation	size	reference_avg_ms	native_avg_ms	speedup_x	time_reduction_pct
softmax	1000	0.2400	0.0427	5.62x	82.20%
softmax	10000	2.5364	0.2630	9.65x	89.63%
softmax	50000	13.8871	1.3652	10.17x	90.17%
topk	1000	0.1777	0.0235	7.57x	86.79%
topk	10000	2.5262	0.6401	3.95x	74.66%
topk	50000	18.2370	3.5924	5.08x	80.30%
vector_add	1000	0.1244	0.0467	2.66x	62.45%
vector_add	10000	0.8710	0.3318	2.63x	61.91%
vector_add	50000	4.5838	1.9524	2.35x	57.41%
Key findings

The native backend beat the Python reference implementation in every benchmarked case.

The strongest gains appeared in loop-heavy numeric work, especially softmax.

The best result was softmax at input size 50000, where the native backend achieved 10.17x speedup and reduced runtime by 90.17%.

The smallest speedup was vector_add at input size 50000, which still achieved 2.35x speedup.

Simpler elementwise operations benefited from native execution, but more computation-heavy operations showed much larger gains.

What this project demonstrates

This project demonstrates:

mixed-language library design

C++ and Python interoperability

native CPU backend implementation

CMake-based build configuration

modern Python packaging with scikit-build-core

correctness validation through parity testing

benchmark design and result analysis

performance-oriented developer tooling workflow