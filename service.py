import json
from datastore import store_json, fetch_json

def get_sample_quiz():
    quiz = {
        "id": "2b811da9-57f1-43db-8d67-9f9dc1c7958a",
        "name": "hehe",
        "questions": [
            {
                "id": "bee4acb6-5d64-48fe-b6e6-0856c9826462",
                "question": "Which number is cooler",
                "answers": [
                    {"answer": "420", "isCorrect": False},
                    {"answer": "666", "isCorrect": False},
                    {"answer": "42", "isCorrect": False},
                    {"answer": "69", "isCorrect": True}
                ]
            },
            {
                "id": "21529fa9-dfe6-4ba8-97d7-f57eda22e830",
                "question": "What's the average air speed of a swallow",
                "answers": [
                    {"answer": "20 m/s", "isCorrect": False},
                    {"answer": "40 m/s", "isCorrect": False},
                    {"answer": "11 m/s", "isCorrect": True},
                    {"answer": "69 m/s", "isCorrect": False}
                ]
            }
        ],
        "score": 0
    }

    return quiz


def get_quiz_ids_ds(username):
    user_quizzes = []
    user_data = fetch_json('userData', filter={"type": "username", "key": username})
    for quiz in user_data["quizIDs"]:
        user_quizzes.append(quiz)
    return user_quizzes


def display_quizzes_ds(quiz_ids):
    quizzes = []
    for quiz in quiz_ids:
        quiz_data = fetch_json('quizData', filter={"type": "id", "key": quiz})
        quizzes.append(quiz_data)
    return quizzes


def get_user(username):
    user_data = fetch_json('userData', filter={"type": "username", "key": username})
    return user_data
