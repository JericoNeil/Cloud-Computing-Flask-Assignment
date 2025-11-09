#!/usr/bin/env python3
"""
Simple test script to verify the API is working correctly
Run this after starting the Flask server (python app.py)
"""

import requests
import json

BASE_URL = "http://localhost:5002/api/v1"

def test_calculate_score():
    print("\n" + "="*60)
    print("TEST 1: Calculate Score")
    print("="*60)

    data = {
        "bachillerato_grade": 8.5,
        "pau_exams": [7.5, 8.0, 7.8, 8.2, 7.9],
        "specific_subjects": [8.5, 9.0]
    }

    response = requests.post(f"{BASE_URL}/students/calculate-score", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_recommendations(score):
    print("\n" + "="*60)
    print("TEST 2: Get Recommendations")
    print("="*60)

    data = {
        "total_score": score,
        "specialization": "Science and Technology",
        "field_interest": "Health Sciences",
        "include_double_degrees": True
    }

    response = requests.post(f"{BASE_URL}/students/recommendations", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total matches: {result.get('total_matches', 0)}")
    print(f"Top 3 recommendations:")
    for i, degree in enumerate(result.get('top_recommendations', [])[:3], 1):
        print(f"  {i}. {degree['name'][:60]}... (Score: {degree['cut_off_score']})")

def test_search():
    print("\n" + "="*60)
    print("TEST 3: Search Degrees")
    print("="*60)

    response = requests.get(f"{BASE_URL}/degrees/search?field=Health%20Sciences&min_score=10")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found: {result.get('count', 0)} programs")

def test_statistics():
    print("\n" + "="*60)
    print("TEST 4: Get Statistics")
    print("="*60)

    response = requests.get(f"{BASE_URL}/statistics/overview")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total programs: {result.get('total_programs', 0)}")
    print(f"Programs by field: {result.get('programs_by_field', {})}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("CareerPath API - Test Suite")
    print("="*60)
    print("Make sure the Flask server is running (python app.py)")
    print("="*60)

    try:
        result = test_calculate_score()
        test_recommendations(result['total_score'])
        test_search()
        test_statistics()

        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Make sure the Flask server is running on http://localhost:5002")
