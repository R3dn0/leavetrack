from dataclasses import asdict
from datetime import datetime
from flask import Blueprint, jsonify, request
from config import get_connection
from services import ReportService

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/balance", methods=["GET"])
def balance():
    conn = get_connection()
    service = ReportService(conn)
    try:
        reports = service.remaining_balance_per_employee()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify([asdict(r) for r in reports])


@reports_bp.route("/reports/understaffing", methods=["GET"])
def understaffing():
    threshold = request.args.get("threshold", 2, type=int)
    raw_start = request.args.get("start_date")
    raw_end = request.args.get("end_date")

    try:
        start_date: datetime | None = (
            datetime.fromisoformat(raw_start) if raw_start else None
        )
        end_date: datetime | None = datetime.fromisoformat(raw_end) if raw_end else None
    except ValueError:
        return jsonify({"error": "Invalid date format, use ISO 8601"}), 400

    conn = get_connection()
    service = ReportService(conn)
    try:
        reports = service.understaffing_alert(
            threshold=threshold,
            start_date=start_date,
            end_date=end_date,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify([asdict(r) for r in reports])


@reports_bp.route("/reports/rolling", methods=["GET"])
def rolling():
    raw = request.args.get("reference_date")
    try:
        reference_date: datetime | None = datetime.fromisoformat(raw) if raw else None
    except ValueError:
        return jsonify({"error": "Invalid date format, use ISO 8601"}), 400

    conn = get_connection()
    service = ReportService(conn)
    try:
        reports = service.rolling_12_months(reference_date=reference_date)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify([asdict(r) for r in reports])
