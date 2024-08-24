from sympy import *
from sympy.abc import x, a, C
from flaskr.solve.base_solver import BaseEDOSolver, NotImplementError

y = Function('y')(x)


def check(eq: Eq):
    if not isinstance(eq, Eq):
        raise ValueError("The equation must be an instance of Eq")

    eq = eq.subs(Symbol('y'), y)

    # separates the terms involving 𝑦 and 𝑥 without the derivative of 𝑦 with respect to 𝑥.
    isolate_dy = solve(eq, Derivative(y, x))[0]
    isolate_dy = isolate_dy.subs(y, a)

    # Find a value for x and y that is not 0, zoo, or nan
    value = 0
    result = isolate_dy.subs({a: value, x: value})
    while result in [0, zoo, nan]:
        value += 1
        result = isolate_dy.subs({a: value, x: value})

    # Check if the equation is separable
    if simplify((isolate_dy.subs(a, value) * isolate_dy.subs(x, value)) / (result * isolate_dy)) == 1:
        return Eq((1 / isolate_dy.subs(x, value).subs(a, y)), 1 / result * isolate_dy.subs(a, value))

    return None


class Separable(BaseEDOSolver):
    preprocess = staticmethod(check)

    def __init__(self):
        super(Separable, self).__init__()

    def solve(self, eq, y0=None, x0=None):
        separable_equation = self.preprocess(eq)
        if separable_equation is None:
            raise NotImplementError("The equation is not separable")

        # Find the general solution, if the initial conditions are not provided
        # integrate both sides
        solution_general = Eq(integrate(separable_equation.lhs, y), integrate(separable_equation.rhs, x) + C)
        if x0 is None and y0 is None:
            return (separable_equation,
                    Eq(Integral(separable_equation.lhs, y), Integral(separable_equation.rhs)),
                    solution_general)

        replace_initial_conditions = solution_general.subs({x: x0, y: y0})
        clearing_constant = solve(replace_initial_conditions, C)[0]
        if not clearing_constant:
            raise ValueError("Unable to determine the constant of integration with the given initial conditions")

        terms_y = solve(solution_general.subs(C, clearing_constant), y)

        return (separable_equation,
                Eq(Integral(separable_equation.lhs, y), Integral(separable_equation.rhs)),
                solution_general,
                replace_initial_conditions,
                Eq(C, clearing_constant),
                solution_general.subs(C, clearing_constant),
                [latex(Eq(y, factor(i))) for i in terms_y])

    def get_steps(self, eq: Eq, y0=None, x0=None):
        if not isinstance(eq, Eq):
            raise ValueError("The equation must be an instance of Eq")

        resolve = self.solve(eq, y0, x0)
        steps = {
            0: ('Despejando el diferencial', latex(eq)),
            1: ('La ecuacion ecuacion separable es', latex(resolve[0])),
            2: ('Integramos ambos lados de la ecuacion', latex(resolve[1])),
            3: ('Solucion general', latex(resolve[2]))
        }

        if y0 is not None and x0 is not None:
            steps[4] = ('Sustituimos las condiciones iniciales en la solucion general', latex(resolve[3]))
            steps[5] = ('Despejando el valor de la constante', latex(resolve[4]))
            steps[6] = ('Solucion particular', latex(resolve[5]))
            steps[7] = ('Solucion en terminos de y', resolve[6])

        return steps
