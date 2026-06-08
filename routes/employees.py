from flask import Blueprint, jsonify
from config.database import get_connection
from repositories.employee_repo import EmployeeRepository
from dataclasses import asdict

employees_bp = Blueprint("employees", __name__)


@employees_bp.route("/employees", methods=["GET"])
def get_employees():
    conn = get_connection()
    repo = EmployeeRepository(conn)
    employees = repo.find_all()
    return jsonify([asdict(e) for e in employees])
