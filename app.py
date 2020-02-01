from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def studyQ():
    return 'studyQ!'


@app.route('/studyQ/quizzes')
def studyQnew():
    return 'It works!'


if __name__ == '__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 8080)))
