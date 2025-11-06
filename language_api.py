# Import required libraries
from flask import Flask, request, jsonify, render_template
from langdetect import detect
import os

# Initialize Flask app
app = Flask(__name__)

# Map language codes (from langdetect) to full language names
LANGUAGES = {
    "af": "Afrikaans", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali",
    "ca": "Catalan", "cs": "Czech", "cy": "Welsh", "da": "Danish", "de": "German",
    "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian",
    "fa": "Persian", "fi": "Finnish", "fr": "French", "gu": "Gujarati",
    "he": "Hebrew", "hi": "Hindi", "hr": "Croatian", "hu": "Hungarian",
    "id": "Indonesian", "it": "Italian", "ja": "Japanese", "kn": "Kannada",
    "ko": "Korean", "lt": "Lithuanian", "lv": "Latvian", "mk": "Macedonian",
    "ml": "Malayalam", "mr": "Marathi", "ne": "Nepali", "nl": "Dutch",
    "no": "Norwegian", "pa": "Punjabi", "pl": "Polish", "pt": "Portuguese",
    "ro": "Romanian", "ru": "Russian", "sk": "Slovak", "sl": "Slovenian",
    "so": "Somali", "sq": "Albanian", "sv": "Swedish", "sw": "Swahili",
    "ta": "Tamil", "te": "Telugu", "th": "Thai", "tl": "Tagalog",
    "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese",
    "zh-cn": "Chinese (Simplified)", "zh-tw": "Chinese (Traditional)"
}


# Frontend endpoint – serves the HTML interface
@app.route('/')
def index():
    """
    Renders the index.html page.
    Flask automatically looks for this file inside the 'templates' folder.
    """
    return render_template('index.html')


# Endpoint to detect the language of a given text
@app.route('/detect', methods=['POST'])
def detect_language():
    """
    POST /detect
    Expects JSON input with a 'text' field and returns the detected language.
    
    Example request: {"text": "Bonjour tout le monde"}
    Example response: {"language": "French"}
    """
    data = request.get_json()
    
    # Validate request
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field in JSON body'}), 400

    text = data['text']

    try:
        # Detect language code (e.g., 'en', 'es', 'fr')
        code = detect(text)
        
        # Map code to full language name
        language = LANGUAGES.get(code, code)
        
        # Return result as JSON
        return jsonify({'language': language})
    except Exception as e:
        # Handle errors gracefully
        return jsonify({'error': str(e)}), 500


# Endpoint to return instance information for assessment
@app.route('/instance', methods=['GET'])
def get_instance():
    """
    GET /instance
    Runs the following code:
        dirs = os.listdir('/var/lib/cloud/instances/')
        return dirs[0]

    On local systems (e.g., macOS) where this path doesn’t exist,
    returns a mock instance name for testing.
    """
    try:
        path = '/var/lib/cloud/instances/'

        # If the directory doesn't exist (e.g. when running locally)
        if not os.path.exists(path):
            return jsonify({'instance': 'mock-instance-id'})

        # List all folders in the directory
        dirs = os.listdir(path)

        # Handle empty directory case
        if not dirs:
            return jsonify({'error': 'No instances found'}), 404

        # Return the first directory name
        return jsonify({'instance': dirs[0]})

    except Exception as e:
        # Catch OS or permission-related errors
        return jsonify({'error': str(e)}), 500


# Entry point to run the Flask app
if __name__ == '__main__':
    # Run on all IPs (0.0.0.0) and port 5001
    app.run(host='0.0.0.0', port=5001)