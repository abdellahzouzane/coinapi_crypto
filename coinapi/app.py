from flask import Flask, request
import sqlite3

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
    return {"message": "Get alerts"}


# Update crypto alert
@app.post("/alerts/<currency_id>")
def update_alert(currency_id):
    return {"message": "Update alerts"}


# Delete a crypto alert
@app.delete("/alerts/<currency_id>")
def delete_alert(currency_id):
    return {"message": "Delete alert"}