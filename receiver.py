import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive-report', methods=['POST'])
def receive_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    with open('testreport.json', 'w') as f:
        import json
        json.dump(data, f, indent=4)
        
    print("Test report received and saved as testreport.json successfully!")
    return jsonify({"status": "success", "message": "Report saved"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)