from flaskr.solve.methods.separable import Separable


def selected(method):
    if method == 'separable':
        return Separable
    else:
        raise ValueError("The method is not valid")
