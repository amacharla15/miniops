import argparse
import csv
import os
import random
import time

import miniops
from miniops import reference


def make_vector(size, seed):
    rng = random.Random(seed)
    values = []
    i = 0
    while i < size:
        values.append(rng.uniform(-10.0, 10.0))
        i += 1
    return values


def time_call(func, args, warmup, repeats):
    i = 0
    while i < warmup:
        func(*args)
        i += 1

    times_ms = []
    i = 0
    while i < repeats:
        start_ns = time.perf_counter_ns()
        func(*args)
        end_ns = time.perf_counter_ns()

        elapsed_ms = (end_ns - start_ns) / 1_000_000.0
        times_ms.append(elapsed_ms)
        i += 1

    total = 0.0
    i = 0
    while i < len(times_ms):
        total += times_ms[i]
        i += 1

    avg_ms = total / len(times_ms)
    min_ms = min(times_ms)
    max_ms = max(times_ms)

    return avg_ms, min_ms, max_ms


def benchmark_vector_add(size, warmup, repeats):
    a = make_vector(size, 1000 + size)
    b = make_vector(size, 2000 + size)

    reference_result = time_call(reference.vector_add, (a, b), warmup, repeats)
    native_result = time_call(miniops.vector_add, (a, b), warmup, repeats)

    rows = []
    rows.append(("vector_add", "reference", size, warmup, repeats, reference_result[0], reference_result[1], reference_result[2]))
    rows.append(("vector_add", "native", size, warmup, repeats, native_result[0], native_result[1], native_result[2]))
    return rows


def benchmark_topk(size, warmup, repeats):
    x = make_vector(size, 3000 + size)
    k = 10
    if size < 10:
        k = size

    reference_result = time_call(reference.topk, (x, k), warmup, repeats)
    native_result = time_call(miniops.topk, (x, k), warmup, repeats)

    rows = []
    rows.append(("topk", "reference", size, warmup, repeats, reference_result[0], reference_result[1], reference_result[2]))
    rows.append(("topk", "native", size, warmup, repeats, native_result[0], native_result[1], native_result[2]))
    return rows


def benchmark_softmax(size, warmup, repeats):
    x = make_vector(size, 4000 + size)

    reference_result = time_call(reference.softmax, (x,), warmup, repeats)
    native_result = time_call(miniops.softmax, (x,), warmup, repeats)

    rows = []
    rows.append(("softmax", "reference", size, warmup, repeats, reference_result[0], reference_result[1], reference_result[2]))
    rows.append(("softmax", "native", size, warmup, repeats, native_result[0], native_result[1], native_result[2]))
    return rows


def write_csv(rows, output_path):
    parent = os.path.dirname(output_path)
    if parent != "":
        os.makedirs(parent, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "operation",
            "backend",
            "size",
            "warmup",
            "repeats",
            "avg_ms",
            "min_ms",
            "max_ms",
        ])

        i = 0
        while i < len(rows):
            writer.writerow(rows[i])
            i += 1


def print_summary(rows):
    print("miniops benchmark summary")
    print("active public backend:", miniops.BACKEND)
    print()

    i = 0
    while i < len(rows):
        row = rows[i]
        operation = row[0]
        backend = row[1]
        size = row[2]
        avg_ms = row[5]
        min_ms = row[6]
        max_ms = row[7]

        print(
            f"op={operation:10s} backend={backend:9s} size={size:6d} "
            f"avg_ms={avg_ms:10.4f} min_ms={min_ms:10.4f} max_ms={max_ms:10.4f}"
        )
        i += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[1000, 10000, 50000],
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/phase6/benchmark_results.csv",
    )
    args = parser.parse_args()

    rows = []

    i = 0
    while i < len(args.sizes):
        size = args.sizes[i]

        vector_rows = benchmark_vector_add(size, args.warmup, args.repeats)
        topk_rows = benchmark_topk(size, args.warmup, args.repeats)
        softmax_rows = benchmark_softmax(size, args.warmup, args.repeats)

        j = 0
        while j < len(vector_rows):
            rows.append(vector_rows[j])
            j += 1

        j = 0
        while j < len(topk_rows):
            rows.append(topk_rows[j])
            j += 1

        j = 0
        while j < len(softmax_rows):
            rows.append(softmax_rows[j])
            j += 1

        i += 1

    write_csv(rows, args.output)
    print_summary(rows)
    print()
    print(f"wrote results to: {args.output}")


if __name__ == "__main__":
    main()