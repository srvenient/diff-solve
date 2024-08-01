import abc

from sympy import *
from sympy.abc import x, y, C

function_y = Function('y')(x)


class DummyAttribute:
    pass


def abstract_attribute(obj=None):
    if obj is None:
        obj = DummyAttribute()
    obj.__is_abstract_attribute__ = True
    return obj


class ABCMeta(abc.ABCMeta):
    def __call__(cls, *args, **kwargs):
        instance = super(ABCMeta, cls).__call__(*args, **kwargs)
        abstract_attributes = {
            name
            for name in dir(instance)
            if getattr(getattr(instance, name), '__is_abstract_attribute__', False)
        }
        if abstract_attributes:
            raise NotImplementedError(
                "Can't instantiate abstract class {} with"
                " abstract attributes: {}".format(
                    cls.__name__,
                    ', '.join(abstract_attributes)
                )
            )
        return instance


class AbstractBaseClass(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        super(AbstractBaseClass, self).__init__(**kwargs)

    @abc.abstractmethod
    def solve(self, eq, y0, x0):
        raise NotImplementedError("The method solve must be implemented")

    @abc.abstractmethod
    def steps(self, eq, y0=0, x0=0):
        raise NotImplementedError("The method steps must be implemented")


class Separable(AbstractBaseClass):
    def __init__(self):
        super(Separable, self).__init__()

    @staticmethod
    def is_separable(eq):
        dy_dx = solve(eq, Derivative(y, x))[0]  # Separate dy/dx

        count = 0
        aux = dy_dx.subs({y: count, x: count})
        while aux == 0 or aux == zoo or aux == nan:
            count += 1
            aux = dy_dx.subs({y: count, x: count})

        f_x, f_y = dy_dx.subs({y: count}), dy_dx.subs({x: count})
        if simplify((aux * dy_dx) / (f_x * f_y)) == 1:
            return True, Eq((1 / f_y.subs(y, function_y)) * Derivative(function_y, x),
                            1 / aux * f_x)
        else:
            raise False

    def solve(self, eq, y0, x0):
        if not isinstance(eq, Eq):
            raise ValueError("The equation must be an instance of Eq")

        if not self.is_separable(eq)[0]:
            raise ValueError("The equation is not separable")

        eq_separable = self.is_separable(eq)[1]

        # integrate both sides
        solution_general = Eq(
            integrate(eq_separable.lhs),
            integrate(eq_separable.rhs, x) + C
        )

        if y0 == 0 and x0 == 0:
            return (eq_separable,
                    Eq(Integral(eq_separable.lhs, y), Integral(eq_separable.rhs, x)),
                    simplify(solution_general))

        # substitute the initial conditions
        subs = solution_general.subs({x: x0, function_y: y0})
        c = solve(subs, C)[0]
        solution_specific = solution_general.subs(C, c)
        terms_y = solve(solution_specific, function_y)

        return (eq_separable,
                Eq(Integral(eq_separable.lhs, y), Integral(eq_separable.rhs, x)),
                simplify(solution_general),
                subs,
                Eq(C, c),
                solution_specific,
                [latex(Eq(function_y, factor(i))) for i in terms_y])

    def steps(self, eq, y0=0, x0=0):
        if not isinstance(eq, Eq):
            raise ValueError("The equation must be an instance of Eq")

        resolve = self.solve(eq, y0, x0)
        steps = {
            0: ('Despejando el diferencial', latex(eq)),
            1: ('La ecuacion ecuacion separable es', latex(resolve[0])),
            2: ('Integramos ambos lados de la ecuacion', latex(resolve[1])),
            3: ('Solucion general', latex(resolve[2]))
        }

        if not (y0 == 0 and x0 == 0):
            steps[4] = ('Sustituimos las condiciones iniciales en la solucion general', latex(resolve[3]))
            steps[5] = ('Despejando el valor de la constante', latex(resolve[4]))
            steps[6] = ('Solución particular', latex(resolve[5]))
            steps[7] = ('Solución en términos de y', resolve[6])

        return steps


class Homogeneous(AbstractBaseClass):
    def __init__(self):
        super(Homogeneous, self).__init__()

    def solve(self, eq, y0, x0):
        pass

    def steps(self, eq, y0=0, x0=0):
        pass
