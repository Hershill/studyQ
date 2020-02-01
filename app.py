from flask import Flask, request, jsonify, make_response
import os
import logging
from service import *

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


@app.route('/studyQ/quizzes')
def studyQnew():
    return 'It works!'


@app.route('/studyQ/get_quizzes')
def studyq_get_quizzes():
    """
    Returns quizzes objects associated with account id

    :return:
    """

    # Get account ID

    return 'It works!'


@app.route('/studyQ/get_quiz', methods=['GET', 'POST'])
def studyq_get_quiz():
    """
    Map quiz objects to account and return quizzes

    :return:
    """
    data = request.json
    user_id = data["userId"]
    username = data["username"]
    # Get data from server
    if request.method == 'GET':
        return make_response(jsonify({"sample": "json"}), 200)

    # Send data to server
    if request.method == 'POST':
        # all quiz ids of the user
        quiz_ids = get_quizz_ids(user_id)
        # return quiz data for quiz ids
        quiz_data = display_quizzes(quiz_ids)
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


if __name__ == '__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 8080)))
