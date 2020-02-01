from flask import Flask, jsonify
import os
from service import get_sample_quiz

app = Flask(__name__)


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

    return 'It works!'


@app.route('/studyQ/get_quiz')
def studyq_get_quiz():
    """
    Map quiz objects to account and return quizzes

    :return:
    """
    return 'It works!'


@app.route('/studyQ/mattest')
def test_endpoint():
    """
    Map quiz objects to account and return quizzes

    :return:
    """
    quiz = get_sample_quiz()
    return jsonify({quiz})


if __name__ == '__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 8080)))
