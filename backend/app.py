from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/message')
def index():
    return jsonify({"message": "here you go chocolates primates - Zidane Rakane Mansouri - 9 October 2025"})

if __name__ == '__main__':
        app.run(debug=True)