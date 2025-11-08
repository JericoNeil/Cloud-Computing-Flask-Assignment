# Cloud-Computing-Flask-Assignment
# 🌐 Language Detection API

A cloud-ready Flask web application for automatic language detection and text analytics. Perfect for cloud computing assignments and API demonstrations!

## 🚀 Features

- **Multi-language detection:** Returns all identified languages in any text, with proportional confidence scores.
- **Text statistics:** Shows character count, word count, and number of detected languages.
- **Browser frontend:** Interactive form for easy API testing.
- **Instance info:** Verifies you are running in the cloud.

## 📂 Project Structure

language_api.py
templates/
└── index.html

## ⚙️ Setup

### 🐍 Environment (Recommended)

If you use **micromamba** or **conda**:

micromamba create -n langdetect_env python=3.11 

micromamba activate langdetect_env

Or with conda:

conda create -n langdetect_env python=3.11 

conda activate langdetect_env

### 📦 Install required packages
pip install flask langdetect

### ▶️ Run the app
python language_api.py


### 🌍 Open in your browser

Go to [http://localhost:5001/](http://localhost:5001/)

## 🔗 API Endpoints

### `/detect-all-probabilities` (POST)
*Detects all languages and their probabilities.*

**Request:**
{ "text": "your input text" }

**Response:**
{
"languages": [
{ "name": "English", "code": "en", "probability": 65.2 },
{ "name": "Spanish", "code": "es", "probability": 34.8 }
]
}

### `/text-stats` (POST)
*Returns summary statistics about input text.*

**Request:**
{ "text": "your input text" }

**Response:**
{
"char_count": 38,
"word_count": 9,
"num_languages": 2,
"language_breakdown": [
{ "name": "English", "code": "en", "probability": 55.0 },
{ "name": "Spanish", "code": "es", "probability": 45.0 }
]
}

### `/instance` (GET)
*Returns cloud compute instance info (or mock value when local).*

**Response:**
{ "instance": "mock-instance-id" }

## 💻 Example Usage

1. **Detect Languages:**  
   Type *Hello, my name is María. Tengo 24 años.*  
   Click "Detect Languages"  
   Result:
   Detected languages:
- English (en): 55.0%
- Spanish (es): 45.0%

2. **Show Text Statistics such as number of characters, words, number of detected languages and language breakdown:**  
Click "Show Text Statistics"  
Result:

Text Statistics: 

Characters: 38 | Words: 9 | Detected languages: 2

Language breakdown:
- English (en): 55.0%
- Spanish (es): 45.0%

## 👤 Author

*Jerico Agdan*  
Cloud Computing Assignment 2
2025-2026
   
