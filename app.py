from flask import Flask, request, jsonify, make_response
import os
import logging
import datetime
from service import get_quiz_ids_ds, display_quizzes_ds, get_sample_quiz, get_user, parse_more, add_quiz
from google.cloud import vision
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


@app.route('/studyQ/quiz', methods=['GET'])
def create_quiz():
    username = request.args.get("username")
    quiz = request.args.get("quiz")
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


@app.route('/studyQ/vision-api', methods=['GET', 'POST'])
def detect_text_uri():
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    uri = request.args.get("image-gcs")
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    ocr = ""
    questionList = []
    current_question = []
    all_answers = []
    a_answer = []
    b_answer = []
    c_answer = []
    d_answer = []
    which_letter = 'none'
    question = True
    first_question_bool = True
    first_abcd = True
    ab_only_question = False
    first_time = True
    quizzletCard = []
    texts = texts[1:]
    for text in texts:

        aWord = str('{}'.format(text.description))
        if '0.' in aWord or '1.' in aWord or '2.' in aWord or '3.' in aWord or \
                '4.' in aWord or '5.' in aWord or '6.' in aWord or '7.' in aWord or \
                '8.' in aWord or '9.' in aWord:

            if first_question_bool:
                previous_question = current_question
                first_question_bool = False

            which_letter = 'none'
            question = True
            first_question = False
            if first_abcd:
                first_abcd = False
                print(len(a_answer))

            if ab_only_question:
                a_string = ""
                for elem in a_answer:
                    a_string = a_string + " " + elem

                b_string = ""
                for elem in b_answer:
                    b_string = b_string + " " + elem

                dictionary = {}
                dictionary['question'] = current_question
                dictionary['a'] = a_string
                dictionary['b'] = b_string
                dictionary['c'] = ''
                dictionary['d'] = ''
                quizzletCard.append(dictionary)
                a_answer = []
                b_answer = []

            else:  # create dictionary with a,b,c,d
                # convert d_answer into one string
                d_string = ""
                for elem in d_answer:
                    d_string = d_string + " " + elem

                c_string = ""
                for elem in c_answer:
                    c_string = c_string + " " + elem

                b_string = ""
                for elem in b_answer:
                    b_string = b_string + " " + elem

                a_string = ""
                for elem in a_answer:
                    a_string = a_string + " " + elem

                q_string = ""
                for elem in current_question:
                    q_string = q_string + " " + elem

                dictionary = {}
                dictionary['question'] = current_question
                dictionary['a'] = a_string
                dictionary['b'] = b_string
                dictionary['c'] = c_string
                dictionary['d'] = d_string
                quizzletCard.append(dictionary)
                a_answer = []
                b_answer = []
                c_answer = []
                d_answer = []

        elif '(a)' in aWord:
            first_question = False
            question = False
            current_question = []
            which_letter = 'a'
        elif '(b)' in aWord:
            which_letter = 'b'
            ab_only_question = True
        elif '(c)' in aWord:
            which_letter = 'c'
            ab_only_question = False
        elif '(d)' in aWord:
            which_letter = 'd'

        # two statements could be entered at one time, a always gets priority.
        # Tried to remove with and statements.

        # This works fine, don't change
        if which_letter == 'a' and '(b)' not in aWord \
                and '(c)' not in aWord and '(d)' not in aWord:
            a_answer.append(aWord)
        elif which_letter == 'b' and '(a)' not in aWord \
                and '(c)' not in aWord and '(d)' not in aWord:
            b_answer.append(aWord)
        elif which_letter == 'c' and '(b)' not in aWord \
                and '(a)' not in aWord and '(d)' not in aWord:
            c_answer.append(aWord)
        elif which_letter == 'd' and '(a)' not in aWord \
                and '(c)' not in aWord and '(b)' not in aWord:
            d_answer.append(aWord)

        if question:
            current_question.append(aWord)

        # print('"{}"'.format(text.description))
        ocr += '"{}"'.format(text.description)

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    quizzletCard = parse_more(quizzletCard)
    # a works if you include the first (a), for a_answer[1:]
    return jsonify(quizzletCard)


if __name__ == '__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 8080)))
