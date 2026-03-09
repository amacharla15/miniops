#include "miniops_cpu.h"

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace miniops {

std::vector<double> vector_add(const std::vector<double>& a, const std::vector<double>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("vector_add requires inputs of the same length");
    }

    std::vector<double> result;
    result.reserve(a.size());

    for (std::size_t i = 0; i < a.size(); ++i) {
        result.push_back(a[i] + b[i]);
    }

    return result;
}

std::pair<std::vector<double>, std::vector<std::size_t>> topk(
    const std::vector<double>& x,
    std::size_t k
) {
    if (k == 0) {
        throw std::invalid_argument("k must be greater than 0");
    }

    if (k > x.size()) {
        throw std::invalid_argument("k cannot be greater than input length");
    }

    std::vector<std::pair<std::size_t, double>> indexed;
    indexed.reserve(x.size());

    for (std::size_t i = 0; i < x.size(); ++i) {
        indexed.push_back({i, x[i]});
    }

    std::sort(
        indexed.begin(),
        indexed.end(),
        [](const auto& left, const auto& right) {
            return left.second > right.second;
        }
    );

    std::vector<double> values;
    std::vector<std::size_t> indices;
    values.reserve(k);
    indices.reserve(k);

    for (std::size_t i = 0; i < k; ++i) {
        indices.push_back(indexed[i].first);
        values.push_back(indexed[i].second);
    }

    return {values, indices};
}

std::vector<double> softmax(const std::vector<double>& x) {
    if (x.empty()) {
        throw std::invalid_argument("softmax requires a non-empty input");
    }

    double max_value = x[0];
    for (std::size_t i = 1; i < x.size(); ++i) {
        if (x[i] > max_value) {
            max_value = x[i];
        }
    }

    std::vector<double> exps;
    exps.reserve(x.size());

    double total = 0.0;
    for (std::size_t i = 0; i < x.size(); ++i) {
        double value = std::exp(x[i] - max_value);
        exps.push_back(value);
        total += value;
    }

    std::vector<double> result;
    result.reserve(x.size());

    for (std::size_t i = 0; i < exps.size(); ++i) {
        result.push_back(exps[i] / total);
    }

    return result;
}

}
