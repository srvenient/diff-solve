
import io
import base64
import sympy as sp
import matplotlib.pyplot as plt
from sympy.plotting import plot


def plot_to_base64(*expr):
    # Genera el gráfico con SymPy
    p = plot(expr, show=False, legend=True, title="Gráfico", xlabel='x', ylabel='f(x)')

    # Usa Matplotlib para crear el gráfico y guardarlo en un buffer
    buf = io.BytesIO()

    # Convertir el gráfico SymPy a un objeto Matplotlib para guardarlo
    for ax in plt.gcf().get_axes():
        ax.grid(True)

    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convertir el buffer a Base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return img_base64


# Ejemplo de uso
if __name__ == "__main__":
    x = sp.symbols('x')
    expr = x ** 2  # Puedes reemplazar esto con tu expresión

    img_base64 = plot_to_base64([-x, x])
    print(f"data:image/png;base64,{img_base64}")
