# AdFit

Implement the notion of fittable function

## Installation

```bash
pip install adfit
```

## Usage

```python
from adfit import Function
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({"text.usetex": True})  # Needs texlive installed

nsamples = 1000
a = 0.3
b = -10
xstart = 0
xend = 1
noise = 0.01
x = np.linspace(xstart, xend, nsamples)
y = a * x ** 2 + b + np.random.normal(0, noise, nsamples)


def linfunc(xx, aa, bb):
    return xx * aa + bb


def square(xx, aa, bb):
    return xx ** 2 * aa + bb


func = Function(linfunc, "$a \\times p[0] + p[1]$")
func2 = Function(square, "$a^2 \\times p[0] + p[1]$")
params = func.fit(x, y, [0, 0])[0]
rr = func.compute_rsquared(x, y, params)
params2 = func2.fit(x, y, [0, 0])[0]
rr2 = func2.compute_rsquared(x, y, params2)
table = Function.make_table(
    [func, func2], [params, params2], [rr, rr2], caption="Linear and Square fit", path_output="table.pdf"
)
table.compile()
Function.plot(x, [func, func2], [params, params2], y=y, rsquared=[rr, rr2])
plt.gcf().savefig("plot.pdf")
```