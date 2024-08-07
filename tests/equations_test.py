from sympy import *
from sympy.abc import x, a
from flaskr.solve.methods.separable import Separable

y = Function('y')(x)


def _separate_variables(eq: Eq):
    if not isinstance(eq, Eq):
        raise ValueError("The equation must be an instance of Eq")

    # separates the terms involving 𝑦 and 𝑥 without the derivative of 𝑦 with respect to 𝑥.
    isolate_dy = solve(eq, Derivative(y))[0]
    isolate_dy = isolate_dy.subs(y, a)

    # Find a value for x and y that is not 0, zoo, or nan
    value = 0
    result = isolate_dy.subs({a: value, x: value})
    while result in [0, zoo, nan]:
        value += 1
        result = isolate_dy.subs({a: value, x: value})

    if simplify((isolate_dy.subs(a, value) * isolate_dy.subs(x, value)) / (result * isolate_dy)) == 1:
        return Eq((1 / isolate_dy.subs(x, value).subs(a, y)), 1 / result * isolate_dy.subs(a, value))

    return None


# Ejemplo de uso
if __name__ == "__main__":
    pprint(Eq(Derivative(y, x), cos(x + y) + sin(x)*sin(y)))
    pprint(_separate_variables(Eq(Derivative(y, x), cos(x + y) + sin(x)*sin(y))))
