from flask import Blueprint, jsonify, render_template, request
from differential_equation.utils import get_as_equation
from sympy import latex

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/api/get/latex', methods=['POST'])
def get_latex_format():
    data = request.get_json()
    value = data['value']
    if value == "":
        return jsonify({"latex": ""})
    eq = get_as_equation(value)
    return jsonify({"latex": latex(eq)})
