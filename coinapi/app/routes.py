from flask import Blueprint, request
import sqlite3
import json
from .utils import verify_inputs

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route("/alerts", methods=["POST"])
def create_alert():
    args = request.json

    valid_input, error_message = verify_inputs(args)

    if not valid_input:
        return {
            "data": {
                "message": error_message
            }
        }

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO alerts (name,currency,quote_currency,anchor_price, operation) VALUES(?, ?, ?, ?, ?)",
                (args.get('name'), args.get('currency'), args.get('quote_currency'), args.get('anchor_price'),
                 args.get('operation'))
            )
            con.commit()
    except Exception as e:
        con.rollback()
        return {
            "data": {
                "message": "Error while creating alert.",
                "errorMessage": repr(e),
            }
        }
    finally:
        con.close()
        return {
            "data": {
                "message": "Alert created successfully!",
                "alert": args
            }
        }


@alerts_bp.route("/alerts", methods=["GET"])
def get_alerts():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from alerts")
    rows = cur.fetchall()

    string_json = json.dumps([dict(ix) for ix in rows])
    parsed_json = json.loads(string_json)

    return {
        "data": {
            "alerts": parsed_json
        }
    }


@alerts_bp.route("/alerts/<int:alert_id>", methods=["PUT"])
def update_alert(alert_id):
    args = request.json

    valid_input, error_message = verify_inputs(args)

    if not valid_input:
        return {
            "data": {
                "message": error_message
            }
        }

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE alerts SET name=?, currency=?, quote_currency=?, anchor_price=?, operation=? WHERE id=?",
                (args.get('name'), args.get('currency'), args.get('quote_currency'), args.get('anchor_price'),
                 args.get('operation'), alert_id)
            )
            con.commit()
    except Exception as e:
        con.rollback()
        return {
            "data": {
                "message": "Error while updating alert.",
                "errorMessage": repr(e),
            }
        }
    finally:
        con.close()
        return {
            "data": {
                "message": "Alert updated successfully!",
                "alert_id": alert_id,
                "updated_values": args
            }
        }


@alerts_bp.route("/alerts/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id):
    is_alert_exists = False

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM alerts WHERE id=?", (alert_id,))
            alert = cur.fetchone()

            if not alert:
                is_alert_exists = True

            cur.execute("DELETE FROM alerts WHERE id=?", (alert_id,))
            con.commit()
    except Exception as e:
        con.rollback()
        return {
            "data": {
                "message": "Error while deleting alert.",
                "errorMessage": repr(e),
            }
        }
    finally:
        con.close()
        if is_alert_exists:
            return {
                "data": {
                    "message": "Alert not found.",
                    "alert_id": alert_id
                }
            }
        else:
            return {
                "data": {
                    "message": "Alert deleted successfully!",
                    "alert_id": alert_id
                }
            }


@alerts_bp.route("/alerts/<int:alert_id>", methods=["GET"])
def get_alert(alert_id):
    is_alert_exists = False

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM alerts WHERE id=?", (alert_id,))
            alert = cur.fetchone()
            if not alert:
                is_alert_exists = True

    except Exception as e:
        return {
            "data": {
                "message": "Error while retrieving alert.",
                "errorMessage": repr(e),
            }
        }
    finally:
        con.close()
        if is_alert_exists:
            return {
                "data": {
                    "message": "Alert not found.",
                    "alert_id": alert_id
                }
            }
        else:
            return {
                "data": {
                    "message": "Alert retrieved successfully!",
                    "alert": {
                        "id": alert[0],
                        "name": alert[1],
                        "currency": alert[2],
                        "quote_currency": alert[3],
                        "anchor_price": alert[4],
                        "operation": alert[5]
                    }
                }
            }