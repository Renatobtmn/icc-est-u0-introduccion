# icc-est

A small Python package for estimating an intraclass correlation coefficient (ICC) from repeated-measures/grouped data.

## Example

```python
from icc_est import estimate_icc

data = [
    [1.0, 2.0, 3.0],
    [2.0, 3.0, 4.0],
    [3.0, 4.0, 5.0],
]

score = estimate_icc(data)
print(score)
```

This computes a one-way random-effects ICC for grouped data, which is commonly used to assess reliability across raters or repeated observations.

## Installation

```bash
pip install .
```

## CLI

```bash
python -m icc_est.icc --data "[[1,2,3],[2,3,4],[3,4,5]]"
```
