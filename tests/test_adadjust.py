from adadjust import Function
import numpy as np
import matplotlib.pyplot as plt

# plt.rcParams.update({"text.usetex": True})

nsamples = 10
a = 0.3
b = -10
xstart = 0
xend = 1
noise = 0.01
x = np.linspace(xstart, xend, nsamples)
y = a * x ** 2 + b + np.random.normal(0, noise, nsamples)


# x12 = np.array([
#     (1, 1),
#     (1, 2),
#     (1, 3),
#     (1, 4),
#     ()
# ])


def linfunc(xx, p0, p1, p2=1):
    return p2 * (xx * p0 + p1)


# def linfunc2d(xx, aa1, bb1, aa2, bb2):
#     return xx[0] * aa1 + bb1 + xx[1] * aa2 + bb2


def square(xx, p0, p1):
    return 2 * (xx ** 2 * p0 + p1)


def test_fit():
    yerr = np.array([0.02, 0.03, 0.12, 0.01, 0.087, 0.013, 0.02, 0.016, 0.024, 0.01])
    func = Function(linfunc, "$p2 \\times (p0 \\times x + p1$)")
    func2 = Function(square, "$p0 \\times x^2 + p1$")
    params = func.fit(x, y, yerr=yerr)
    rr = round(func.compute_rsquared(x, y, *params), 3)
    params2 = func2.fit(x, y, yerr=yerr)
    rr2 = round(func2.compute_rsquared(x, y, *params2), 3)
    _ = Function.make_table(
        [func, func2], [params, params2], [rr, rr2], caption="Linear and Square fit", path_output="tests/data/table.pdf"
    )
    Function.fit_new(x=x, y=y, yerr=yerr, params=[params, params2], functions=[func, func2], rsquared=[rr, rr2])
    print(params)
    plt.gcf().savefig("tests/data/plot6.png")

# def test_fit_2d(): func = Function(linfunc, "$a \\times p[0] + p[1]$") func2 = Function(square, "$a^2 \\times p[0]
# + p[1]$") params = func.fit(x, y, np.array([0, 0]))[0] rr = func.compute_rsquared(x, y, params) params2 =
# func2.fit(x, y, np.array([0, 0]))[0] rr2 = func2.compute_rsquared(x, y, params2) _ = Function.make_table( [func,
# func2], [params, params2], [rr, rr2], caption="Linear and Square fit", path_output="tests/data/table.pdf" ) #
# table.compile() Function.plot(x, [func, func2], [params, params2], y=y, rsquared=[rr, rr2]) plt.gcf().savefig(
# "tests/data/plot.pdf")
