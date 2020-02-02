import json
import uuid
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
    user_data = fetch_json('userData', filter={
                           "type": "username", "key": username})
    for quiz in user_data["quizIDs"]:
        user_quizzes.append(quiz)
    return user_quizzes


def display_quizzes_ds(quiz_ids):
    quizzes = []
    for quiz in quiz_ids:
        quiz_data = fetch_json('quizData', filter={"type": "id", "key": quiz})
        quizzes.append(quiz_data)
    return quizzes


def add_quiz(username, quiz):
    # Add quiz to user data
    user_data = fetch_json('userData', filter={"type": "username", "key": username})
    print(quiz)
    user_data["quizIDs"].append(quiz["id"])
    store_json(user_data, "userData")

    # Store the new quiz
    store_json(quiz, "quizData")


def get_user(username):
    user_data = fetch_json('userData', filter={
                           "type": "username", "key": username})
    return user_data


def merge_q_a(question_data, answer_data):
    final_set = []

    for q in question_data:
        print(q)
        q.update({"answers": answer_data[0:4]})
        q.update({"leaderboard": []})
        q.update({"uuid": uuid.uuid4()})
        answer_data = answer_data[4:]
        final_set.append(q)
    
    final_set = {"questions": final_set, "name": "Edit Title", "uuid": uuid.uuid4()}
    return final_set


def parse_more(data):
    print(data)
    question_data = []
    answer_data = []
    for q in data:
        question = " ".join(q['question'])
        question_data.append({"question": question})
    
    for a in data:
        answer_data.append({"answer": a['a'][5:], "isCorrect": False})
        answer_data.append({"answer": a['b'][5:], "isCorrect": False})
        answer_data.append({"answer": a['c'][5:], "isCorrect": False})
        answer_data.append({"answer": a['d'][5:], "isCorrect": False})
    
    answer_data.append({"answer": data[-1]['a'][5:]})
    answer_data.append({"answer": data[-1]['b'][5:]})
    answer_data.append({"answer": data[-1]['c'][5:]})
    answer_data.append({"answer": data[-1]['d'][5:]})

    answer_data = answer_data[4:]
    
    print(answer_data)
    quiz_data = merge_q_a(question_data, answer_data)
    return quiz_data
