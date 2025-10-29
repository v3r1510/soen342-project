from flask import Flask, jsonify
from flask_cors import CORS
from controller import bp, initialize_console

app = Flask(__name__)
CORS(app)


app.register_blueprint(bp)

@app.route('/message')
def index():
    return jsonify({"message": "here you go chocolates primates - Zidane Rakane Mansouri - 9 October 2025"})

@app.route('/status')
def status():
    return jsonify({"status": "Backend is running", "endpoints": ["/search", "/routes", "/cities", "/train-types"]})

if __name__ == '__main__':
    app.run(debug=True)
