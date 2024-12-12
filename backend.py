# Largely created with ChatGPT

from flask import Flask, request, jsonify
from flask_cors import CORS
from chatgpt import get_full_stamped_topics
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

@app.route('/getstampedtopics', methods=['POST'])
def getstampedtopics():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.get_data(as_text=True)  # Get raw data as string
        data = json.loads(data)  # Manually parse JSON
    transcript = data.get('transcript', '')
    attempts = 0
    max_attempts = 4
    while attempts < max_attempts:
        try:
            return jsonify({'stamped_topics': get_full_stamped_topics(transcript)})
        except Exception as e:
            attempts += 1
            if attempts == max_attempts:
                return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Too many attempts made'}), 500

if __name__ == '__main__':
    app.run(debug=True)
