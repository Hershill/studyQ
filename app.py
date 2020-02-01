from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def studyQ():
    return 'studyQ!'


@app.route('/studyQ')
def studyQ():
    return 'It works!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
