from flask import Flask
from api.analyze import analyze_route
import os

app = Flask(__name__)
app.register_blueprint(analyze_route)

@app.route("/")
def home():
    return "S-CIAX Running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
