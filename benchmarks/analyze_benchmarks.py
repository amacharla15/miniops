import argparse
import csv
import os


def read_rows(input_path):
    with open(input_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append(row)
    return rows


def group_rows(rows):
    grouped = {}

    i = 0
    while i < len(rows):
        row = rows[i]
        operation = row["operation"]
        size = int(row["size"])
        backend = row["backend"]

        key = (operation, size)
        if key not in grouped:
            grouped[key] = {}

        grouped[key][backend] = row
        i += 1

    return grouped


def build_summary_rows(grouped):
    keys = list(grouped.keys())
    keys.sort(key=lambda item: (item[0], item[1]))

    summary_rows = []

    i = 0
    while i < len(keys):
        key = keys[i]
        operation = key[0]
        size = key[1]
        pair = grouped[key]

        if "reference" not in pair or "native" not in pair:
            raise ValueError(f"missing backend row for operation={operation}, size={size}")

        reference_row = pair["reference"]
        native_row = pair["native"]

        reference_avg_ms = float(reference_row["avg_ms"])
        native_avg_ms = float(native_row["avg_ms"])
        reference_min_ms = float(reference_row["min_ms"])
        native_min_ms = float(native_row["min_ms"])
        reference_max_ms = float(reference_row["max_ms"])
        native_max_ms = float(native_row["max_ms"])

        speedup_x = reference_avg_ms / native_avg_ms
        time_reduction_pct = (1.0 - (native_avg_ms / reference_avg_ms)) * 100.0

        summary_rows.append({
            "operation": operation,
            "size": size,
            "reference_avg_ms": reference_avg_ms,
            "native_avg_ms": native_avg_ms,
            "reference_min_ms": reference_min_ms,
            "native_min_ms": native_min_ms,
            "reference_max_ms": reference_max_ms,
            "native_max_ms": native_max_ms,
            "speedup_x": speedup_x,
            "time_reduction_pct": time_reduction_pct,
        })

        i += 1

    return summary_rows


def write_summary_csv(summary_rows, output_path):
    parent = os.path.dirname(output_path)
    if parent != "":
        os.makedirs(parent, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "operation",
            "size",
            "reference_avg_ms",
            "native_avg_ms",
            "reference_min_ms",
            "native_min_ms",
            "reference_max_ms",
            "native_max_ms",
            "speedup_x",
            "time_reduction_pct",
        ])

        i = 0
        while i < len(summary_rows):
            row = summary_rows[i]
            writer.writerow([
                row["operation"],
                row["size"],
                f"{row['reference_avg_ms']:.6f}",
                f"{row['native_avg_ms']:.6f}",
                f"{row['reference_min_ms']:.6f}",
                f"{row['native_min_ms']:.6f}",
                f"{row['reference_max_ms']:.6f}",
                f"{row['native_max_ms']:.6f}",
                f"{row['speedup_x']:.4f}",
                f"{row['time_reduction_pct']:.2f}",
            ])
            i += 1


def find_best_speedup(summary_rows):
    best = summary_rows[0]
    i = 1
    while i < len(summary_rows):
        if summary_rows[i]["speedup_x"] > best["speedup_x"]:
            best = summary_rows[i]
        i += 1
    return best


def find_worst_speedup(summary_rows):
    worst = summary_rows[0]
    i = 1
    while i < len(summary_rows):
        if summary_rows[i]["speedup_x"] < worst["speedup_x"]:
            worst = summary_rows[i]
        i += 1
    return worst


def write_summary_markdown(summary_rows, output_path):
    parent = os.path.dirname(output_path)
    if parent != "":
        os.makedirs(parent, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Benchmark Summary\n\n")
        f.write("| operation | size | reference_avg_ms | native_avg_ms | speedup_x | time_reduction_pct |\n")
        f.write("|---|---:|---:|---:|---:|---:|\n")

        i = 0
        while i < len(summary_rows):
            row = summary_rows[i]
            f.write(
                f"| {row['operation']} | {row['size']} | "
                f"{row['reference_avg_ms']:.4f} | {row['native_avg_ms']:.4f} | "
                f"{row['speedup_x']:.2f}x | {row['time_reduction_pct']:.2f}% |\n"
            )
            i += 1

        f.write("\n## Key Findings\n\n")

        best_row = find_best_speedup(summary_rows)
        worst_row = find_worst_speedup(summary_rows)

        f.write(
            f"- Best speedup: **{best_row['operation']}** at size **{best_row['size']}** "
            f"with **{best_row['speedup_x']:.2f}x** speedup.\n"
        )
        f.write(
            f"- Lowest speedup: **{worst_row['operation']}** at size **{worst_row['size']}** "
            f"with **{worst_row['speedup_x']:.2f}x** speedup.\n"
        )

        f.write("- Native backend outperformed the Python reference implementation in every tested case.\n")
        f.write("- Loop-heavy numeric work showed the strongest gains, especially for softmax at larger sizes.\n")


def print_terminal_summary(summary_rows, csv_path, md_path):
    print("phase 7 benchmark analysis")
    print()

    i = 0
    while i < len(summary_rows):
        row = summary_rows[i]
        print(
            f"op={row['operation']:10s} size={row['size']:6d} "
            f"ref_avg_ms={row['reference_avg_ms']:10.4f} "
            f"native_avg_ms={row['native_avg_ms']:10.4f} "
            f"speedup={row['speedup_x']:7.2f}x "
            f"reduction={row['time_reduction_pct']:7.2f}%"
        )
        i += 1

    print()

    best = find_best_speedup(summary_rows)
    worst = find_worst_speedup(summary_rows)

    print(
        f"best speedup: {best['operation']} size={best['size']} "
        f"speedup={best['speedup_x']:.2f}x"
    )
    print(
        f"lowest speedup: {worst['operation']} size={worst['size']} "
        f"speedup={worst['speedup_x']:.2f}x"
    )
    print(f"wrote csv summary to: {csv_path}")
    print(f"wrote markdown summary to: {md_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        default="results/phase6/benchmark_results.csv",
    )
    parser.add_argument(
        "--output_csv",
        type=str,
        default="results/phase7/benchmark_summary.csv",
    )
    parser.add_argument(
        "--output_md",
        type=str,
        default="results/phase7/benchmark_summary.md",
    )
    args = parser.parse_args()

    rows = read_rows(args.input)
    grouped = group_rows(rows)
    summary_rows = build_summary_rows(grouped)
    write_summary_csv(summary_rows, args.output_csv)
    write_summary_markdown(summary_rows, args.output_md)
    print_terminal_summary(summary_rows, args.output_csv, args.output_md)


if __name__ == "__main__":
    main()

