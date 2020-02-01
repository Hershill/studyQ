from flask import Flask
import os

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
def studyq_get_quizzes():
    """
    Map quiz objects to account and return quizzes

    :return:
    """
    return 'It works!'


if __name__ == '__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 8080)))
