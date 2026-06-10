from flask import Flask
from config import get_connection
from routes import absences_bp, employees_bp, reports_bp

app = Flask(__name__)

connection = get_connection()


@app.route("/")
def index():
    return "Welcome home R3dn0 !"


app.register_blueprint(employees_bp)
app.register_blueprint(absences_bp)
app.register_blueprint(reports_bp)


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
