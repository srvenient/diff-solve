from sympy import *
from sympy.abc import x, t, v, a, C

from flaskr.solve.base_solver import BaseEDOSolver, NotImplementError
from flaskr.solve.methods.separable import Separable

y = Function('y')(x)


def check(eq: Eq):
    fxy = solve(eq, Derivative(y, x))[0]
    ft = fxy.subs({x: x * t}, {y: y * t})

    h1 = factor(fxy)
    h2 = factor(ft)

    if diff(simplify(h2 / h1), x) == 0:
        return True
    else:
        return False


class Homogeneous(BaseEDOSolver):
    preprocess = staticmethod(check)

    def __init__(self):
        super(Homogeneous, self).__init__()

    def solve(self, eq, y0=None, x0=None):
        if not isinstance(eq, Eq):
            raise ValueError("The equation must be an instance of Eq")

        if check(eq):
            y_expr = x * v
            dy_expr = v * diff(x, y) + x * diff(v, y)

            trans_equation = eq.subs({y: y_expr, diff(y, x): dy_expr})
            eq_reducible = trans_equation / diff(x)

            return eq_reducible, Separable().solve(trans_equation)
        else:
            raise NotImplementError("The equation is not homogeneous")

    def get_steps(self, eq: Eq, y0=None, x0=None):
        pass

