from flask import Flask

app = Flask(__name__)


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