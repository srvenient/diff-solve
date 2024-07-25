from flask import Blueprint, jsonify, render_template, request
from differential_equation.utils import latex_chain

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/api/get/latex', methods=['POST'])
def get_latex():
    data = request.get_json()
    text = data['value']
    latex = latex_chain(text)
    return jsonify({"latex": latex})
