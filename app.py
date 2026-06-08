from flask import Flask
from config.database import get_connection

from routes.employees import employees_bp

app = Flask(__name__)

connection = get_connection()


@app.route("/")
def index():
    return "Welcome hone R3dn0 !"


app.register_blueprint(employees_bp)


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
