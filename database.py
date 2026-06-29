import json
import os

def load_quiz_data():
    file_path = "skills.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {
        "questions": [
            {
                "id": 1,
                "text": "Q1: A primary goal of Artificial Intelligence is...",
                "options": [
                    "A. Making artificial ideas",
                    "B. Mimicking human intelligence",
                    "C. Correct option",
                    "D. Creating network protocols"
                ],
                "correct": "C. Correct option"
            }
        ]
    }