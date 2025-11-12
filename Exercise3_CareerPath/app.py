# After installing Flask and Flask CORS, we add import the libraries

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from typing import List, Dict, Optional

app = Flask(__name__)
CORS(app)  # CORS for frontend access

# Load degrees data, this is the JSON file that I created from the data cleaning I carried out.
with open('degrees_data.json', 'r', encoding='utf-8') as f:
    DEGREES_DATA = json.load(f)

# This section contains functions dedicated to calculating the final university admission score for  high school students based on Bachillerato grades, PAU exam results, and subject-specific scores.
def calculate_admission_score(bachillerato_grade: float, pau_exams: List[float], 
                              specific_subjects: List[float]) -> Dict:
    """
    Calculate the final admission score out of 14 points.

    Spanish system:
    - Bachillerato: 60% of grade (max 6 points in calculation, 0.6 * grade)
    - PAU General Phase: Average of 5 exams (max 4 points, 0.4 * average)
    - Specific Phase: Best 2 subjects with 0.2 weight each (max 4 points)

    Total: Max 14 points (10 from admission phase + 4 from specific phase)
    """

    # Bachillerato component (60% of grade, max 6 points)
    bachillerato_component = bachillerato_grade * 0.6

    # PAU general phase component (average of exams, weighted 40%, max 4 points)
    pau_average = sum(pau_exams) / len(pau_exams) if pau_exams else 0
    pau_component = pau_average * 0.4

    # Admission phase score (max 10)
    admission_phase = bachillerato_component + pau_component

    # Specific grades: best 2 subjects with 0.2 weight (max 4 points)
    specific_sorted = sorted(specific_subjects, reverse=True)[:2]
    specific_component = sum([grade * 0.2 for grade in specific_sorted])

    # Total score
    total_score = round(admission_phase + specific_component, 3)

    return {
        'total_score': total_score,
        'breakdown': {
            'bachillerato_component': round(bachillerato_component, 3),
            'pau_component': round(pau_component, 3),
            'admission_phase_score': round(admission_phase, 3),
            'specific_subjects_component': round(specific_component, 3)
        }
    }


def filter_degrees(score: float, specialization: Optional[str] = None,
                  field_interest: Optional[str] = None, 
                  include_double_degrees: bool = True,
                  location: Optional[str] = None,
                  university: Optional[str] = None) -> List[Dict]:
    """Filter degrees based on criteria"""

    filtered = []

    for degree in DEGREES_DATA:
        # Score filter: student's score must be >= cut-off score
        if degree['cut_off_score'] > score:
            continue

        # Specialization filter
        if specialization and degree['specialization'] != specialization:
            continue

        # Field filter
        if field_interest:
            if degree['field'] != field_interest and not degree['is_double_degree']:
                continue

        # Double degree filter
        if not include_double_degrees and degree['is_double_degree']:
            continue

        # Location filter
        if location and degree['province'] != location and location.lower() != 'any':
            continue

        # University filter
        if university and degree['university'] != university:
            continue

        filtered.append(degree)

    return filtered


def categorize_by_reach(student_score: float, degree_score: float) -> str:
    """Categorize a degree as Safety, Match, or Reach"""
    difference = degree_score - student_score

    if difference <= -1.0:
        return "Safety"
    elif difference <= 0.5:
        return "Match"
    else:
        return "Reach"


# API ENDPOINTS

@app.route('/')
def home():
    """Serve the frontend HTML page"""
    return render_template('career_index.html')


@app.route('/api/v1/students/calculate-score', methods=['POST'])
def calculate_score():
    """
    Endpoint 1: Calculate admission score

    Request body:
    {
        "bachillerato_grade": 8.5,
        "pau_exams": [7.5, 8.0, 7.8, 8.2, 7.9],
        "specific_subjects": [8.5, 9.0]
    }
    """
    try:
        data = request.get_json()

        # Validate input
        bachillerato = data.get('bachillerato_grade')
        pau_exams = data.get('pau_exams', [])
        specific_subjects = data.get('specific_subjects', [])

        if bachillerato is None or bachillerato < 0 or bachillerato > 10:
            return jsonify({'error': 'Bachillerato grade must be between 0 and 10'}), 400

        if not pau_exams or len(pau_exams) != 5:
            return jsonify({'error': 'Must provide exactly 5 PAU exam grades'}), 400

        if len(specific_subjects) < 2:
            return jsonify({'error': 'Must provide at least 2 specific subject grades'}), 400

        # Calculate score
        result = calculate_admission_score(bachillerato, pau_exams, specific_subjects)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/students/recommendations', methods=['POST'])
def get_recommendations():
    """
    Endpoint 2: Get top degree recommendations

    Request body:
    {
        "total_score": 11.85,
        "specialization": "Science and Technology",
        "field_interest": "Health Sciences",
        "include_double_degrees": true,
        "location": "Barcelona"
    }
    """
    try:
        data = request.get_json()

        score = data.get('total_score')
        specialization = data.get('specialization')
        field_interest = data.get('field_interest')
        include_double_degrees = data.get('include_double_degrees', True)
        location = data.get('location')

        if score is None or score < 0 or score > 14:
            return jsonify({'error': 'Total score must be between 0 and 14'}), 400

        # Filter degrees
        filtered = filter_degrees(
            score=score,
            specialization=specialization,
            field_interest=field_interest,
            include_double_degrees=include_double_degrees,
            location=location
        )

        # Sort by cut-off score (descending) to show most competitive first
        filtered.sort(key=lambda x: x['cut_off_score'], reverse=True)

        # Take top 20
        top_20 = filtered[:20]

        # Add reach categorization
        for degree in top_20:
            degree['category'] = categorize_by_reach(score, degree['cut_off_score'])

        return jsonify({
            'total_matches': len(filtered),
            'top_recommendations': top_20,
            'student_score': score
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/degrees/search', methods=['GET'])
def search_degrees():
    """
    Endpoint 3: Search and filter degrees

    Query parameters:
    - field: Field of study
    - min_score: Minimum cut-off score
    - max_score: Maximum cut-off score
    - university: University code
    - location: Province
    - specialization: High school specialization
    - double_degree: true/false
    """
    try:
        field = request.args.get('field')
        min_score = float(request.args.get('min_score', 0))
        max_score = float(request.args.get('max_score', 14))
        university = request.args.get('university')
        location = request.args.get('location')
        specialization = request.args.get('specialization')
        double_degree = request.args.get('double_degree', '').lower() == 'true'

        # Filter
        results = []
        for degree in DEGREES_DATA:
            # Apply filters
            if degree['cut_off_score'] < min_score or degree['cut_off_score'] > max_score:
                continue
            if field and degree['field'] != field:
                continue
            if university and degree['university'] != university:
                continue
            if location and degree['province'] != location:
                continue
            if specialization and degree['specialization'] != specialization:
                continue
            if double_degree and not degree['is_double_degree']:
                continue

            results.append(degree)

        # Sort by score
        results.sort(key=lambda x: x['cut_off_score'], reverse=True)

        return jsonify({
            'count': len(results),
            'results': results
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/degrees/<code>', methods=['GET'])
def get_degree_details(code):
    """
    Endpoint 4: Get details of a specific degree by code
    """
    try:
        for degree in DEGREES_DATA:
            if degree['code'] == code:
                return jsonify(degree), 200

        return jsonify({'error': 'Degree not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/statistics/overview', methods=['GET'])
def get_statistics():
    """
    Endpoint 5: Get statistical overview of the admission landscape
    """
    try:
        # Calculate statistics
        total_programs = len(DEGREES_DATA)

        # Score distribution
        score_ranges = {
            '5.0-6.0': 0,
            '6.0-8.0': 0,
            '8.0-10.0': 0,
            '10.0-12.0': 0,
            '12.0+': 0
        }

        fields_count = {}
        specializations_count = {}
        universities_count = {}
        field_avg_scores = {}
        field_score_sums = {}

        for degree in DEGREES_DATA:
            score = degree['cut_off_score']

            # Score ranges
            if score < 6.0:
                score_ranges['5.0-6.0'] += 1
            elif score < 8.0:
                score_ranges['6.0-8.0'] += 1
            elif score < 10.0:
                score_ranges['8.0-10.0'] += 1
            elif score < 12.0:
                score_ranges['10.0-12.0'] += 1
            else:
                score_ranges['12.0+'] += 1

            # Count by field
            field = degree['field']
            fields_count[field] = fields_count.get(field, 0) + 1
            field_score_sums[field] = field_score_sums.get(field, 0) + score

            # Count by specialization
            spec = degree['specialization']
            specializations_count[spec] = specializations_count.get(spec, 0) + 1

            # Count by university
            uni = degree['university']
            universities_count[uni] = universities_count.get(uni, 0) + 1

        # Calculate average scores by field
        for field in fields_count:
            field_avg_scores[field] = round(field_score_sums[field] / fields_count[field], 2)

        return jsonify({
            'total_programs': total_programs,
            'score_distribution': score_ranges,
            'programs_by_field': fields_count,
            'programs_by_specialization': specializations_count,
            'programs_by_university': universities_count,
            'average_scores_by_field': field_avg_scores
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# To run the application

if __name__ == '__main__':
    print("=" * 60)
    print("CareerPath API - Bachillerato to University Guide")
    print("=" * 60)
    print(f"Total programs loaded: {len(DEGREES_DATA)}")
    print("\nAPI Endpoints:")
    print("  POST   /api/v1/students/calculate-score")
    print("  POST   /api/v1/students/recommendations")
    print("  GET    /api/v1/degrees/search")
    print("  GET    /api/v1/degrees/<code>")
    print("  GET    /api/v1/statistics/overview")
    print("\nStarting server on http://localhost:5002")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5002)
