from flask import Flask
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db')
print("Database opened successfully")

# name: name of the alert
# currency: e.g. BTC (You should use CoinApi asset ID)
# anchor_price: The price of the operation
# operation: accepts 2 values "above" and "under"
conn.execute('CREATE TABLE alerts (name TEXT, currency TEXT, anchor_price REAL, operation TEXT)')
print("Table created successfully")


# Create crypto alert
@app.post("/alerts")
def create_alert():
    return {"message": "Create alert"}


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