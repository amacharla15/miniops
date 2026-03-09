# Benchmark Summary

| operation | size | reference_avg_ms | native_avg_ms | speedup_x | time_reduction_pct |
|---|---:|---:|---:|---:|---:|
| softmax | 1000 | 0.2400 | 0.0427 | 5.62x | 82.20% |
| softmax | 10000 | 2.5364 | 0.2630 | 9.65x | 89.63% |
| softmax | 50000 | 13.8871 | 1.3652 | 10.17x | 90.17% |
| topk | 1000 | 0.1777 | 0.0235 | 7.57x | 86.79% |
| topk | 10000 | 2.5262 | 0.6401 | 3.95x | 74.66% |
| topk | 50000 | 18.2370 | 3.5924 | 5.08x | 80.30% |
| vector_add | 1000 | 0.1244 | 0.0467 | 2.66x | 62.45% |
| vector_add | 10000 | 0.8710 | 0.3318 | 2.63x | 61.91% |
| vector_add | 50000 | 4.5838 | 1.9524 | 2.35x | 57.41% |

## Key Findings

- Best speedup: **softmax** at size **50000** with **10.17x** speedup.
- Lowest speedup: **vector_add** at size **50000** with **2.35x** speedup.
- Native backend outperformed the Python reference implementation in every tested case.
- Loop-heavy numeric work showed the strongest gains, especially for softmax at larger sizes.
