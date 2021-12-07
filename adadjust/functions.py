from typing import Callable, Union
from scipy.optimize import leastsq
import logging
import numpy as np
import tablewriter
import pandas as pd
import matplotlib.pyplot as plt
from colorstylecycler import Cycler

logger = logging.getLogger(__name__)


class Function:
    def __init__(self, method: Callable, equation: str):
        self.method = method
        self.equation = equation

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)

    def make_result_equation(self, params, r=None) -> str:
        s = self.equation
        for iparam in range(len(params)):
            param = params[iparam]
            if param < 0:
                s = s.replace(f"+ p[{iparam}]", format_x(param))
                s = s.replace(f"+p[{iparam}]", format_x(param))
                s = s.replace(f"- p[{iparam}]", format_x(float(str(param).replace("-", ""))))
                s = s.replace(f"-p[{iparam}]", format_x(float(str(param).replace("-", ""))))
                s = s.replace(f"p[{iparam}]", f"({format_x(param)})")
            else:
                s = s.replace(f"p[{iparam}]", f"{format_x(param)}")
        if r is not None:
            s = f"{s}\\\\$r^2={r}$"
        s = "".join(["\\setlength{\\parindent}{0cm}", s])
        return s

    def fit(self, x, y, init, yerrup=None, yerrdown=None):
        def my_error(args):
            yfit = self(x, *args)
            weight = np.ones_like(yfit)
            if yerrdown is None:
                if yerrup is None:
                    return (yfit - y) ** 2
                weight[yfit > y] = yerrup[yfit > y]
            weight[yfit <= y] = yerrdown[yfit <= y]
            return (yfit - y) ** 2 / weight ** 2

        if len(x) < len(init):
            logger.warning("Can not fit a function with less observations than parameters")
            return None
        if len(x) == len(init):
            logger.warning("Fitting a function with the same number of observations than parameters")
        params = leastsq(my_error, init)
        return params

    def predict(self, x, params, **kwargs):
        """same as calling self(x, *params, **kwargs)"""
        return self.method(x, *params, **kwargs)

    def compute_rsquared(self, x, y, params):
        rss = np.sum((y - self(x, *params)) ** 2)
        tss = np.sum((y - np.mean(y)) ** 2)
        rr = round(1 - (rss / tss), 3)
        return rr

    @staticmethod
    def make_table(functions, params, rsuared=None, **table_kwargs) -> tablewriter.TableWriter:
        nparams = max([len(par) for par in params])
        data = [
            [format_x(params[if_][ip], True) if ip < nparams else np.nan for ip in range(len(params[if_]))]
            for if_ in range(len(functions))
        ]

        table_g = pd.DataFrame(
            columns=[f"param {i}" for i in range(nparams)], index=[f.equation for f in functions], data=data
        )
        if rsuared is not None:
            s = pd.DataFrame(index=table_g.index, data=rsuared, columns=["$r^2$"])
            table_g = pd.concat([table_g, s], axis=1)

        return tablewriter.TableWriter(data=table_g, **table_kwargs)

    @staticmethod
    def plot(
        x,
        functions,
        params,
        y=None,
        ax=None,
        yerr=None,
        xerr=None,
        ms=10,
        lw=5,
        marker="o",
        ylabel="data",
        xshow=None,
        rsquared=None,
        **kwargs
    ):
        if ax is None:
            ax = plt.gca()
        if rsquared is None:
            rsquared = [None for _ in functions]

        nitems = len(functions)

        cycler = Cycler(ncurves=nitems, color_start="darkred", color_end="darkblue")
        plt.rc("axes", prop_cycle=cycler.cycler)
        if y is not None:
            if yerr is None and xerr is None:
                ax.scatter(x=x, y=y, c="black", s=ms, marker=marker, label=ylabel)
            else:
                ax.errorbar(x=x, y=y, yerr=yerr, xerr=xerr, c="black", s=ms, fmt=marker, label=ylabel)

        if xshow is not None:
            x = xshow
        for function, param, r in zip(functions, params, rsquared):
            ax.plot(x, function(x, *param, **kwargs), label=function.make_result_equation(param, r), lw=lw)
        ax.legend()
        return ax


def format_x(s: Union[float, int], with_dollar: bool = False) -> str:
    """For a given number, will put it in scientific notation if lower than 0.01, using LaTex synthax.

    In addition, if the value is lower than alpha, will change set the color of the value to green.
    """
    if 1000 > s > 0.01:
        xstr = str(round(s, 2))
    else:
        xstr = "{:.4E}".format(s)
        if "E-" in xstr:
            lead, tail = xstr.split("E-")
            middle = "-"
        else:
            lead, tail = xstr.split("E")
            middle = ""
        lead = round(float(lead), 2)
        tail = round(float(tail), 2)
        if with_dollar:
            xstr = ("$\\cdot 10^{" + middle).join([str(lead), str(tail)]) + "}$"
        else:
            xstr = ("\\cdot 10^{" + middle).join([str(lead), str(tail)]) + "}"
    return xstr
