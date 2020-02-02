from flask import Flask, request, jsonify, make_response
import os
import logging
import datetime
from service import get_quiz_ids_ds, display_quizzes_ds, get_sample_quiz, get_user, add_quiz

from datastore import store_json, fetch_json

app = Flask(__name__)

# Logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Load the configuration from the config file
app.config.from_pyfile('config.py')


@app.route('/')
def studyQ():
    return 'studyQ!'


@app.route('/studyQ/datastore_fetch_quizzes', methods=['GET', 'POST'])
def datastore_fetch_quizzes():
    """
    Map quiz objects to account and return quizzes

    :return:
    """
    # Get data from server (for web ui)
    if request.method == 'GET':
        username = request.args.get("username")
        # all quiz ids of the user
        quiz_ids = get_quiz_ids_ds(username)
        # return quiz data for quiz ids
        quiz_data = display_quizzes_ds(quiz_ids)
        return make_response(jsonify(quiz_data), 200)
        # return make_response(jsonify({"sample": "json"}), 200)

    # Send data to server
    if request.method == 'POST':
        data = request.json
        username = data["username"]
        # all quiz ids of the user
        quiz_ids = get_quiz_ids_ds(username)
        # return quiz data for quiz ids
        quiz_data = display_quizzes_ds(quiz_ids)
        return jsonify(quiz_data)

    return 'It works!'


@app.route('/studyQ/mattest')
def test_endpoint():
    """
    Map quiz objects to account and return quizzes

    :return:
    """
    quiz = get_sample_quiz()
    return jsonify(quiz)


@app.route('/datastore')
def root():
    # store_json("quizData")
    # store_json("userData")

    # sample = fetch_json("quizData")
    sample = fetch_json("userData")

    return jsonify(list(sample)[0])


@app.route('/studyQ/quiz', methods=['POST'])
def create_quiz():
    username = request.form.get("username")
    quiz = request.form.get("quiz")
    add_quiz(username, quiz)


@app.route('/studyQ/account', methods=['GET', 'POST'])
def create_account():
    # Send data to server
    if request.method == 'POST':
        username = request.form.get("username")
        # data = request.json
        # username = data["username"]
        # all quiz ids of the user
        user_data = get_user(username)
        if not user_data:
            user_data = {"username": username, "quizIDs": []}
            store_json(user_data, "userData")

    # Send data to server
    if request.method == 'GET':
        username = request.args.get("username")
        # all quiz ids of the user
        user_data = get_user(username)
        if not user_data:
            user_data = {"username": username, "quizIDs": []}
            store_json(user_data, "userData")

    return make_response(jsonify(user_data), 200)


if __name__ == '__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 8080)))
