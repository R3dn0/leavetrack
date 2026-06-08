from datetime import datetime

from flask import Blueprint, jsonify, request

from config.database import get_connection
from repositories.absence_repo import AbsenceRepository
from repositories.absence_type_repo import AbsenceTypeRepository
from repositories.employee_repo import EmployeeRepository
from repositories.leave_balance_repo import LeaveBalanceRepository
from services.absence_service import AbsenceService

absences_bp = Blueprint("absences", __name__)


@absences_bp.route("/absences", methods=["POST"])
def submit_absence():
    data = request.get_json()

    conn = get_connection()
    service = AbsenceService(
        absence_repo=AbsenceRepository(conn),
        absence_type_repo=AbsenceTypeRepository(conn),
        employee_repo=EmployeeRepository(conn),
        leave_balance_repo=LeaveBalanceRepository(conn),
    )

    try:
        absence = service.submit_absence(
            employee_id=data.get("employee_id"),
            type_id=data.get("type_id"),
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            reason=data.get("reason", ""),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(_absence_to_dict(absence)), 201


@absences_bp.route("/absences/<int:absence_id>/approve", methods=["PUT"])
def approve_absence(absence_id: int):
    conn = get_connection()
    service = AbsenceService(
        absence_repo=AbsenceRepository(conn),
        absence_type_repo=AbsenceTypeRepository(conn),
        employee_repo=EmployeeRepository(conn),
        leave_balance_repo=LeaveBalanceRepository(conn),
    )

    try:
        absence = service.approve_absence(absence_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(_absence_to_dict(absence))


@absences_bp.route("/absences/<int:absence_id>/reject", methods=["PUT"])
def reject_absence(absence_id: int):
    conn = get_connection()
    service = AbsenceService(
        absence_repo=AbsenceRepository(conn),
        absence_type_repo=AbsenceTypeRepository(conn),
        employee_repo=EmployeeRepository(conn),
        leave_balance_repo=LeaveBalanceRepository(conn),
    )

    try:
        absence = service.reject_absence(absence_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(_absence_to_dict(absence))


def _absence_to_dict(absence):
    return {
        "id": absence.id,
        "employee_id": absence.employee_id,
        "type_id": absence.type_id,
        "start_date": absence.start_date.isoformat() if absence.start_date else None,
        "end_date": absence.end_date.isoformat() if absence.end_date else None,
        "status": absence.status.value,
        "reason": absence.reason,
    }
