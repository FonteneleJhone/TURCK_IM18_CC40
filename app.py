from flask import Flask, jsonify
import os
import json
import multiprocessing

app = Flask(__name__)

def run_main():
    exec(open("main.py").read())

def read_api_data():
    # Read data from api.json
    file_path = os.path.join(os.path.dirname(__file__), 'api.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

@app.route('/')
def index():
    # Read data from api.json
    api_data = read_api_data()

    # Extract relevant information
    sensor_data = api_data.get('im18_ccm40', {})
    temperature = sensor_data.get('Temperatura', '')
    humidity = sensor_data.get('Umidade', '')
    distance = sensor_data.get('Distancia', '')

    # Return JSON response
    return jsonify({
        "temperature": temperature,
        "humidity": humidity,
        "distance": distance
    })

if __name__ == '__main__':
    #app.run(host='192.168.0.9', port=5000, debug=True)
    p = multiprocessing.Process(target=run_main)
    p.start()
    app.run(host='192.168.0.9', port=5000, debug=True)
