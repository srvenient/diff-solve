import flaskr.solve.better_abc as better_abc

from sympy import Eq


class NotImplementError(Exception):
    """This error will be thrown when an EDO cannot be solved by means of a method"""
    pass


class BaseEDOSolver(metaclass=better_abc.ABCMeta):
    """API for solving ordinary differential equations"""

    preprocess = better_abc.abstract_attribute()

    def __init__(self,
                 **kwargs):
        super(BaseEDOSolver, self).__init__(**kwargs)

    @better_abc.abstract_attribute
    def solve(self, eq: Eq, y0=None, x0=None):
        """Propose a solution for an ordinary differential equation (ODE) by computing
        the derivative of the function y(x) with respect to x.

        Args:
            eq: The ordinary differential equation to solve
            y0: The initial condition for y
            x0: The initial condition for x

        Returns:
            The solution general or particular of the ODE
        """
        raise NotImplementedError("The methods solve must be implemented")

    @better_abc.abstract_attribute
    def get_steps(self, eq: Eq, y0=None, x0=None):
        """Get the steps to solve an ordinary differential equation (ODE) by computing

        Args:
            eq: The ordinary differential equation to solve
            y0: The initial condition for y
            x0: The initial condition for x

        Returns:
            The steps to solve the ODE
        """
        raise NotImplementedError("The methods steps must be implemented")
