#pragma once

#include <cstddef>
#include <utility>
#include <vector>

namespace miniops {

std::vector<double> vector_add(const std::vector<double>& a, const std::vector<double>& b);

std::pair<std::vector<double>, std::vector<std::size_t>> topk(
    const std::vector<double>& x,
    std::size_t k
);

std::vector<double> softmax(const std::vector<double>& x);

}
