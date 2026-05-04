from flask import Flask
from api.analyze import analyze_route

app = Flask(__name__)

app.register_blueprint(analyze_route)

@app.route("/")
def home():
    return "S-CIAX Running"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
