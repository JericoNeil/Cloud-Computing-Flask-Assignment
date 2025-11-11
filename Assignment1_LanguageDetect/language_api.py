# Import required libraries for web server, language detection, and file system operations.
from flask import Flask, request, jsonify, render_template
from langdetect import detect, detect_langs
import os

# Initialize the Flask web application instance.
app = Flask(__name__)

# Dictionary mapping short language codes to full human-readable names.
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

# The main endpoint serves the enhanced HTML frontend.
@app.route('/')
def index():
    return render_template('index.html')

# First endpoint to detect all possible languages in text, showing probabilities for each.
@app.route('/detect-all-probabilities', methods=['POST'])
def detect_all_probabilities():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field in JSON body'}), 400
    text = data['text']
    try:
        langs = detect_langs(text)
        results = []
        for lang in langs:
            results.append({
                'code': lang.lang,
                'name': LANGUAGES.get(lang.lang, lang.lang),
                'probability': round(lang.prob * 100, 2)
            })
        return jsonify({'languages': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Second endpoint that returns cloud instance info or a mock value.
@app.route('/instance', methods=['GET'])
def get_instance():
    try:
        path = '/var/lib/cloud/instances/'
        if not os.path.exists(path):
            return jsonify({'instance': 'mock-instance-id'})
        dirs = os.listdir(path)
        if not dirs:
            return jsonify({'error': 'No instances found'}), 404
        return jsonify({'instance': dirs[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Third endpoint that returns summary statistics about the submitted text.
# Output is the character count, word count, and number of detected languages.
@app.route('/text-stats', methods=['POST'])
def text_stats():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field in JSON body'}), 400
    text = data['text']
    char_count = len(text)
    word_count = len(text.split())
    # Detect all possible languages and count them for mixed inputs.
    try:
        langs = detect_langs(text)
        num_languages = len(langs)
        language_breakdown = [
            {
                "code": l.lang,
                "name": LANGUAGES.get(l.lang, l.lang),
                "probability": round(l.prob * 100, 2)
            }
            for l in langs
        ]
        return jsonify({
            'char_count': char_count,
            'word_count': word_count,
            'num_languages': num_languages,
            'language_breakdown': language_breakdown
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Starts the Flask server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)