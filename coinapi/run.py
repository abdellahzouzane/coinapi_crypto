from flask import Flask
from app.routes import alerts_bp
from scheduler import check_alerts
import threading

app = Flask(__name__)

app.register_blueprint(alerts_bp)

check_alerts_thread = threading.Thread(target=check_alerts)
check_alerts_thread.daemon = True
check_alerts_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
