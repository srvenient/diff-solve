from flask import Blueprint, render_template, request, jsonify
from sympy import latex

from flaskr import services
from flaskr.solve import utils

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/api/get/latex_format', methods=['POST'])
def convert_to_latex():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    eq = data.get('value')
    initial_conditions = data.get('initial_conditions')

    if eq == "":
        return jsonify({'latex': ''})

    try:
        y0, x0 = utils.analyze_initial_conditions(initial_conditions)
        if y0 is None and x0 is None:
            return jsonify({'latex': latex(services.get_as_sympy(eq))})

        return jsonify({'latex': latex(services.get_as_sympy(eq)) + f",\\quad x_{0}={x0},\\quad y({x0}) = {y0}"})
    except ValueError:
        return jsonify({'latex': eq})


@bp.route('/api/get/solve_ode', methods=['POST'])
def solve_ode():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        eq = data.get('value')
        method = data.get('method')
        initial_conditions = data.get('initial_conditions')

        if not eq:
            return jsonify({'error': 'The equation is required'}), 400

        if not method:
            return jsonify({'error': 'The methods is required'}), 400

        y0, x0 = utils.analyze_initial_conditions(initial_conditions)
        steps = services.dsolve(
            services.get_as_sympy(eq),
            method,
            y0,
            x0
        )

        return jsonify({'steps': steps})
    except ValueError as e:
        return jsonify({'error': "A value error occurred: " + str(e)}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")  # Log the error for debugging
        return jsonify({'error': "An unexpected error occurred: " + str(e)}), 500
    except BaseException as e:
        print(f"Unexpected error: {e}")  # Log the error for debugging
