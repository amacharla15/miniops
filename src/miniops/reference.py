import math


def vector_add(a, b):
    if len(a) != len(b):
        raise ValueError("vector_add requires inputs of the same length")

    result = []
    i = 0
    while i < len(a):
        result.append(float(a[i]) + float(b[i]))
        i += 1
    return result


def topk(x, k):
    n = len(x)
    if k <= 0:
        raise ValueError("k must be greater than 0")
    if k > n:
        raise ValueError("k cannot be greater than input length")

    indexed = []
    i = 0
    while i < n:
        indexed.append((i, float(x[i])))
        i += 1

    indexed.sort(key=lambda item: item[1], reverse=True)

    values = []
    indices = []
    i = 0
    while i < k:
        indices.append(indexed[i][0])
        values.append(indexed[i][1])
        i += 1

    return values, indices


def softmax(x):
    if len(x) == 0:
        raise ValueError("softmax requires a non-empty input")

    max_value = float(x[0])
    i = 1
    while i < len(x):
        current = float(x[i])
        if current > max_value:
            max_value = current
        i += 1

    exps = []
    total = 0.0
    i = 0
    while i < len(x):
        value = math.exp(float(x[i]) - max_value)
        exps.append(value)
        total += value
        i += 1

    result = []
    i = 0
    while i < len(exps):
        result.append(exps[i] / total)
        i += 1

    return result