from flask import Flask, jsonify
from flask_cors import CORS
from controller import bp, initialize_console

app = Flask(__name__)
CORS(app)

# Register the controller blueprint
app.register_blueprint(bp)

@app.route('/message')
def index():
    return jsonify({"message": "here you go chocolates primates - Zidane Rakane Mansouri - 9 October 2025"})

@app.route('/status')
def status():
    return jsonify({"status": "Backend is running", "endpoints": ["/search", "/routes", "/cities", "/train-types"]})

if __name__ == '__main__':
    # Initialize the console with your CSV file
    # You'll need to add your data file path here
    # initialize_console('path/to/your/data.csv')
    app.run(debug=True)