# Cloud-Computing-Flask-Assignment
# Exercise 1: Language Detection API

Exercise 1 consists of developing a Flask web application for automatic language detection and text analytics.

## Features

- **Multi-language detection:** Returns all identified languages in any text, with proportional confidence scores.
- **Text statistics:** Shows character count, word count, and number of detected languages.
- **Browser frontend:** Interactive form for easy API testing.
- **Instance info:** Verifies you are running in the cloud.

## Project Structure
You can access the exercise in the "Exercise1_LanguageDetect" folder and it contains:
- language_api.py: the code for the API
- templates/ --> index.html: the html file for the front-end and user experience

## Setup

### Environment

If you use **micromamba** or **conda**:

micromamba create -n langdetect_env python=3.11 

micromamba activate langdetect_env

Or with conda:

conda create -n langdetect_env python=3.11 

conda activate langdetect_env

### Install required packages
pip install flask langdetect

### Run the app
- First, go to the project folder: cd "Exercise1_LanguageDetect"

- Then run the application: python language_api.py

- After starting the app: Open your browser and go to http://localhost:5001 or http://127.0.0.1:5001 to use the Language Detection API.

If you want to access the app from another device on your local network, use your computer’s local IP address (e.g., http://192.168.1.x:5001), replacing x with your computer’s actual IP.

## API Endpoints

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

## Example Usage

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

# Exercise 2: Making the API available in AWS
This exercise demonstrates that the Flask Language Detection API has been successfully deployed to an AWS EC2 instance and is accessible remotely. Information about this exercise is explained and requested screenshots are in the PDF document. In summary, exercise 2 consists of the following:

## 1) Screenshot of the Running Instance
Include a screenshot from the AWS Management Console showing:
- The list of EC2 instances, with the instance clearly in the “Running” state.
- The public IP address of the EC2 instance, which is necessary to access the API from outside the network.
- My username displayed at the top right of the AWS console for verification.

## 2) Screenshot of the /instance Endpoint
- This second point includes a screenshot demonstrating a successful API request to the /instance endpoint of the cloud-hosted Flask app:
- The screenshot shows the cloud instance
- The response must confirm that the API is responding on the deployed instance.

## 3) Extra: Screenshot of the Text Statistics Endpoint
- As an extra for completeness, this point includes a screenshot of a request to the /text-stats endpoint:
- The response should display the number of characters, words, and detected languages, along with a proportional breakdown by language.

# Exercise 3: Bachillerato University Degree Recommendation System

The motivation behind this project is to help my brother choose which university degree to pursue. He's currently in his first year of high school but he has no idea about what he wants to study like a great majority of students. Notwithstanding the importance of choosing a degree, there's no existing platform that tells you what career paths you could pursue based on your high school + PAU predicted grades. 

In Catalonia, you can find this website from the Government of Catalonia about the cut-off grades of Catalonian bachelor's, but the information of studies is in PDF, which is not very convenient to filter degrees: https://universitats.gencat.cat/ca/preinscripcions/notes-tall/

This first version of the project aims to provide a better user experience to high school students, empowering students like my brother to make informed and personalized decisions about their academic futures.

## Features
- **University Admission Calculator (out of 14)**: It converts Bachillerato and PAU grades into your official university admission score (out of 14). It can be your predicted or actual values.
- **Personalized recommendations**: It suggests the top 20 degrees within reach based on your predicted admission score, where you can filter by **high school specialization**(Sciences and Technology, Arts and Humanities, Social Sciences) and/or **bachelor's study field** (e.g., Engineering and Architecture, Social Sciences and Law, Sciences, Arts and Humanities, etc.), **geographic preference** (e.g., Girona, Barcelona, Lleida, Tarragona), and **whether the student is interested in a double degree**.
- **Statistics dashboard**: It shows some statistical data program regarding distribution, score averages, and field-by-field competitiveness of the 555 Catalonian degrees, excluding private universities.


## Project Structure
You can access the exercise in the "Exercise3_CareerPath" folder and it contains:
- app.py: The Flask API backend implementing all core endpoints and business logic.
- templates/career_index.html: The html frontend to interact with the application.
- degrees_data.json: The full database of university degrees and admission requirements. **I personally cleaned the data and added more variables for filtering (see at the end the data cleaning process of the database)**.
- requirements.txt: The list of the required dependencies required to install and run the project.
- raw_database folder: This includes the database of PAU scores in PDF and Excel

## Setup

### Environment

If you use **micromamba** or **conda**:

micromamba create -n career_env python=3.11 

micromamba activate career_env

Or with conda:

conda create -n career_env python=3.11 

conda activate career_env

### Install required packages
pip install flask flask-cors

### ▶Run the app
Now, you go to cd "Exercise3_CareerPath"
python app.py

### Open in your browser

Go to [http://172.21.8.147:5002]

## API Endpoints

### 1st endpoint: `/api/v1/students/calculate-score` (POST)
*Calculate your Spanish university admission score (out of 14) from Bachillerato, general PAU exams, and two specific subject marks.*

**Request:**
{
  "bachillerato_grade": 8.5,
  "pau_exams": [7.5, 8.0, 7.8, 8.2, 7.9],
  "specific_subjects": [8.5, 9.0]
}

**Response:**
{
  "total_score": 11.85,
  "breakdown": {
    "bachillerato_component": 5.1,
    "pau_component": 3.14,
    "admission_phase_score": 8.24,
    "specific_subjects_component": 3.4
  }
}

### 2nd endpoint: `/api/v1/students/recommendations` (POST)
*Returns a ranked list of the best-fit university degrees based on your score, specialization, field of interest, location, and double degree preference*

**Request:**
{
  "total_score": 11.85,
  "specialization": "Science and Technology",
  "field_interest": "Health Sciences",
  "location": "Barcelona",
  "include_double_degrees": true
}

**Response:**
{
  "total_matches": 57,
  "top_recommendations": [
    {
      "code": "11043",
      "name": "Medicina (Campus Clínic) (Barcelona)",
      "university": "UB",
      "location": "Barcelona",
      "province": "Barcelona",
      "field": "Health Sciences",
      "specialization": "Science and Technology",
      "cut_off_score": 12.85,
      "is_double_degree": false,
      "category": "Reach"
    }
  ],
  "student_score": 11.85
}

### 3rd endpoint: `/api/v1/statistics/overview` (GET)
*Presents statistical summaries about score distribution, fields, specializations, and universities*


**Request:**
api/v1/statistics/overview

**Response:**
{
  "average_scores_by_field": {
    "Arts and Humanities": 5.67,
    "Double Degree": 8.93,
    "Engineering and Architecture": 8.74,
    "Health Sciences": 9.35,
    "Sciences": 9.48,
    "Social Sciences and Law": 7.28
  },
  "programs_by_field": {
    "Arts and Humanities": 69,
    "Double Degree": 86,
    "Engineering and Architecture": 120,
    "Health Sciences": 80,
    "Sciences": 38,
    "Social Sciences and Law": 162
  },
  "programs_by_specialization": {
    "Arts and Humanities": 86,
    "Science and Technology": 270,
    "Social Sciences": 199
  },
  "programs_by_university": {
    "UAB": 111,
    "UB": 90,
    "UB / UPC": 2,
    "UPC": 67,
    "UPC / UB /\nUAB / UPF": 1,
    "UPC / UPF": 1,
    "UPF": 47,
    "UPF / UAB": 1,
    "URV": 66,
    "URV / UOC": 1,
    "UVic-UCC": 39,
    "UVic-UCC /\nUB": 1,
    "UdG": 70,
    "UdG / UB": 2,
    "UdL": 56
  },
  "score_distribution": {
    "10.0-12.0": 113,
    "12.0+": 31,
    "5.0-6.0": 164,
    "6.0-8.0": 98,
    "8.0-10.0": 149
  },
  "total_programs": 555
}

## Data Cleaning of the Database
I used the Database from the Generalitat of Catalonia website, which is the official website to retrieve the "cut-off grades" or Notes de Tall in Catalan, of each degree of Catalonian universities (excluding private university bachelor's). I did not have the Excel File, so I converted the PDF file to Excel and followed a multi-step data cleaning process using Excel.

Moreover, I also enriched the dataset by adding several new columns to support feature filtering and analysis in the application:
- Location: The city where each university program is offered
- Province: The province in which the university is located (for broader geographic filtering, there are 4 provinces in Catalonia)
- Field: The academic or professional field of each degree (such as Health Sciences, Engineering, etc.)
- High-School Specialization: The typical Spanish Bachillerato track granting access to each degree (e.g., Science and Technology, Social Sciences, Arts and Humanities)

In order to carry out the cleaning and structuring process, I did the following:

### 1. Extracting Location from Degree Name
All degree names in the dataset ended with their location in parentheses, for example, Administració i Direcció d'Empreses (Barcelona). My goal was to systematically extract just the place name (e.g., Barcelona).

To do this, I used two Excel formulas:
- TEXTAFTER(A1, "(", -1): This extracts all text after the last opening parenthesis in the string from cell A1. For the example above, it would yield Barcelona).
- TEXTBEFORE(..., ")"): Applying this to the previous result, it pulls everything before the closing parenthesis, giving just Barcelona.

Combined into one formula: =TEXTBEFORE(TEXTAFTER(A1,"(",-1), ")").

### 2. Creating and Filling the Region Column
Once I extracted the city names, I wanted to have a broader region classification, in this case, the Catalonia provinces: Barcelona, Tarragona, Girona and Lleida. This classification will be used to the final API so that students living in Girona, for example, can filter Girona-based universities.

In order to do so, I created an Excel tab called "Data_Cleaning" where I created a table with two columns: the first one is the city values (where I extracted by executing the "Unique" Excel formula (45 locations), and with this, I classified them in one of the four region.

After that, I added the Region column by executing a lookup to fill the region column automatically for all rows.

### 3. Adding the Field + High School Specialization columns
To enable more advanced filtering and personalized recommendations, I enriched the dataset by adding two key columns: Field (field of the study of the bachelor's degree) and High School Specialization (the Bachillerato track that typically grants access to each degree).

For the Field column, my goal was to assign every degree to a broader academic area—such as "Health Sciences," "Engineering and Architecture," or, for combined programs, "Double Degree" (so I could offer a filter specifically for dual programs). To automate this field column, I used an LLM in which I prompted it to extract relevant keywords from each degree title and map them to the correct academic area. For example, any degree containing "Enginyeria" was automatically mapped to "Engineering and Architecture." Wherever the LLM or pattern-based lookup didn't retrieve a clear result, such as less common or ambiguous degrees, I assigned the field manually to ensure accuracy.

For the High School Specialization column, I followed a similar approach. I built a mapping table that links each field to its most common Bachillerato specialization. This allowed the platform to let students filter degrees by either their current specialization, their field of interest, or both. For example, a student from a Science and Technology background could still explore management or law degrees if those are accessible or relevant.

### 4. Final Cleaning & Export
As a final step, I made sure all categorical values were consistent (for example, always spelling “Barcelona” the same way), and ensured that all necessary fields were filled in.

With all columns complete and clean, I then exported the Excel table into a JSON file, so it's much convenient for direct use in the API and the HTML backend.

## Author
*Jerico Agdan*  
Cloud Computing Assignment 2
2025-2026