from __future__ import annotations

import argparse
import json
from typing import Iterable, Sequence


def _group_mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def icc_one_way(data: Sequence[Sequence[float]]) -> float:
    """Compute the one-way random-effects ICC (absolute agreement, single-measurement)."""
    rows = [list(map(float, row)) for row in data]

    if not rows:
        raise ValueError("Data must contain at least one group.")

    group_size = len(rows[0])
    if group_size < 2:
        raise ValueError("Each group must contain at least two observations.")

    if any(len(row) != group_size for row in rows):
        raise ValueError("All groups must have the same number of observations.")

    group_count = len(rows)
    if group_count < 2:
        return 1.0

    grand_mean = sum(sum(group) for group in rows) / (group_count * group_size)

    ss_within = 0.0
    ss_between = 0.0
    for group in rows:
        mean_group = _group_mean(group)
        ss_within += sum((value - mean_group) ** 2 for value in group)
        ss_between += group_size * (mean_group - grand_mean) ** 2

    if ss_within == 0:
        return 1.0

    ms_between = ss_between / (group_count - 1)
    ms_within = ss_within / (group_count * (group_size - 1))

    if ms_between <= 0:
        return 0.0

    icc = (ms_between - ms_within) / (ms_between + (group_size - 1) * ms_within)
    return max(0.0, min(1.0, icc))


def estimate_icc(data: Sequence[Sequence[float]]) -> float:
    """Convenience wrapper for ICC estimation."""
    return icc_one_way(data)


def _parse_cli_data(raw: str) -> list[list[float]]:
    parsed = json.loads(raw)
    if not isinstance(parsed, list) or not all(isinstance(item, list) for item in parsed):
        raise ValueError("Expected JSON like [[1.0,2.0],[3.0,4.0]].")
    return [list(map(float, row)) for row in parsed]


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate an ICC from grouped data.")
    parser.add_argument("--data", required=True, help="JSON array of rows, e.g. [[1,2,3],[2,3,4]].")
    args = parser.parse_args()
    result = estimate_icc(_parse_cli_data(args.data))
    print(f"{result:.6f}")


if __name__ == "__main__":
    main()
