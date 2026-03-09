#include "miniops_cpu.h"

#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    {
        std::vector<double> a = {1.0, 2.0};
        std::vector<double> b = {3.0, 4.0};
        std::vector<double> result = miniops::vector_add(a, b);

        if (result.size() != 2 || result[0] != 4.0 || result[1] != 6.0) {
            throw std::runtime_error("vector_add smoke test failed");
        }
    }

    {
        std::vector<double> x = {1.0, 5.0, 3.0, 4.0};
        auto result = miniops::topk(x, 2);

        const std::vector<double>& values = result.first;
        const std::vector<std::size_t>& indices = result.second;

        if (values.size() != 2 || indices.size() != 2) {
            throw std::runtime_error("topk smoke test failed: wrong output size");
        }

        if (values[0] != 5.0 || values[1] != 4.0 || indices[0] != 1 || indices[1] != 3) {
            throw std::runtime_error("topk smoke test failed: wrong values or indices");
        }
    }

    {
        std::vector<double> x = {1.0, 2.0, 3.0};
        std::vector<double> result = miniops::softmax(x);

        if (result.size() != 3) {
            throw std::runtime_error("softmax smoke test failed: wrong output size");
        }

        double total = result[0] + result[1] + result[2];
        if (std::fabs(total - 1.0) > 1e-9) {
            throw std::runtime_error("softmax smoke test failed: probabilities do not sum to 1");
        }

        if (!(result[2] > result[1] && result[1] > result[0])) {
            throw std::runtime_error("softmax smoke test failed: ordering mismatch");
        }
    }

    std::cout << "All C++ smoke tests passed.\n";
    return 0;
}
