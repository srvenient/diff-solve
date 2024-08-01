from sympy import Eq, sympify

import flaskr.ode as ode
from flaskr import utils

METHODS = {
    "separable": ode.Separable
}


def get_as_sympy(eq: str) -> Eq:
    """ Convert the string to a sympy equation

    :param eq:
    :return: The sympy equation
    """
    if "=" not in eq:
        raise ValueError("The equation must contain an equals sign")

    lhs, rhs = eq.split("=")
    if not rhs or not lhs:
        raise ValueError("The equation must contain a left and right side")

    try:
        return Eq(sympify(utils.replace_character(lhs)), sympify(utils.replace_character(rhs)))
    except Exception as e:
        raise ValueError("Invalid mathematical expression") from e


def dsolve(eq, method, y0, x0):
    if not isinstance(eq, Eq):
        raise ValueError("The equation must be an instance of Eq")

    if method == "automatic":
        if ode.Separable.is_separable(eq)[0]:
            if x0 == 0 and y0 == 0:
                return ode.Separable().steps(eq)

            return ode.Separable().steps(eq, y0, x0)

    if method not in METHODS:
        raise ValueError("The method is not valid")

    if x0 == 0 and y0 == 0:
        return METHODS[method]().steps(eq)

    return METHODS[method]().steps(eq, y0, x0)
