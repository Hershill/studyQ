import json


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


def get_quizz_ids(user_id):
    user_quizzes = []
    with open("userData.json", 'r') as f:
        user_data = json.load(f)
    
    if user_id in user_data["userIDs"]:
        for quiz in user_data["userIDs"][user_id]["quizIDs"]:
            user_quizzes.append(quiz)
    
    return user_quizzes

def display_quizzes(quiz_ids):
    quizzes = []
    with open("sampleData.json", 'r') as f:
        quiz_data = json.load(f)
    
    for quiz in quiz_data["quizzItems"]:
        if quiz["id"] in quiz_ids:
            quizzes.append(quiz)

    # for quiz_id in quiz_ids:
    #     for quiz in quiz_data["quiz"]:
    #         if quiz_id == quiz["id"]:
    #             quizzes.append(quiz)
    return quizzes

