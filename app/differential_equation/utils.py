def latex_chain(a: str) -> str:
    try:
        from sympy import sympify, latex
        expr = sympify(a)
        return latex(expr)
    except Exception as e:
        print("Error al convertir a LaTeX:", e)
        return "Error en la conversión a LaTeX"

