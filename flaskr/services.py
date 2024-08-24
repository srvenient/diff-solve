from sympy import Eq, sympify

from flaskr.solve import utils
from flaskr.solve.base_solver import NotImplementError
from flaskr.solve.methods import separable


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

    try:
        if method == "separable":
            return separable.Separable().get_steps(eq, y0, x0)
        else:
            raise ValueError("The method is not valid")
    except NotImplementError:
        print("The equation is not separable")
    except Exception as e:
        print("An error occurred: ", e)
