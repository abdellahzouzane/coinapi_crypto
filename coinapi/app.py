from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)

conn = sqlite3.connect('database.db')
print("Database opened successfully")

# name: name of the alert
# currency: e.g. BTC (You should use CoinApi asset ID) - Base currency
# quote_currency: e.g. USD (You should use CoinApi asset ID) - Quote currency
# anchor_price: The price of the operation
# operation: accepts 2 values "above" and "under"
conn.execute(
    'CREATE TABLE IF NOT EXISTS alerts (name TEXT, currency TEXT, quote_currency TEXT, anchor_price REAL, operation TEXT)')
print("Table created successfully")

conn.close()


# Create crypto alert
@app.post("/alerts")
def create_alert():
    args = request.json
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


# Get crypto alerts
@app.get("/alerts")
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


# Update crypto alert
@app.put("/alerts/<currency_id>")
def update_alert(currency_id):
    args = request.json

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()

        cur.execute("SELECT * FROM alerts WHERE id=?", (currency_id,))
        alert = cur.fetchone()

        if 'name' in args and not isinstance(args['name'], str):
            return ("The 'name' field must be a string.")
        if 'currency' in args and not isinstance(args['currency'], str):
            return ("The 'currency' field must be a string.")
        if 'quote_currency' in args and not isinstance(args['quote_currency'], str):
            return ("The 'quote_currency' field must be a string.")
        if 'anchor_price' in args and not isinstance(args['anchor_price'], (int, float)):
            return ("'anchor_price' field must be a number (int or float).")
        if 'operation' in args and not isinstance(args['operation'], str):
            return ("The 'operation' field must be a string.")

        cur.execute(
            """
            UPDATE alerts
            SET name=?, currency=?, quote_currency=?, anchor_price=?, operation=?,
            WHERE id=?
            """,
            (
                args.get('name', alert['name']),
                args.get('currency', alert['currency']),
                args.get('quote_currency', alert['quote_currency']),
                args.get('anchor_price', alert['anchor_price']),
                args.get('operation', alert['operation']),
                currency_id
            )
        )

        con.commit() 

    return jsonify({"message": "Alert successfully updated!"})


# Delete a crypto alert
@app.delete("/alerts/<currency_id>")
def delete_alert(currency_id):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()

        cur.execute("SELECT * FROM alerts WHERE id=?", (currency_id,))
        alert = cur.fetchone()

        cur.execute("DELETE FROM alerts WHERE id=?", (currency_id,))
        con.commit()

    return jsonify({"message": "Alert successfully deleted!"})


if __name__ == "__main__":
    app.run()