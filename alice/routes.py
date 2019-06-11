from alice import app, db
from flask import request
from flask import jsonify
from .model.models import AppUser
from .intent_classifier.classifier import classify_intent
from .actions.executor import execute_action
from .natural_language.generator import generate_text
import alice.nlp.lemmatizer as nlp_lem


def create_response(text, received_data):
    """
    :param string text: the final text response of our chat bot
    :param dict received_data: the json structure received from Yandex
    :return dict: chat bot response as json structure
    """
    return {
        "response": {
            "text": text,
            "tts": text,
            "end_session": False,
        },
        "session": {
            "session_id": received_data['session']['session_id'],
            "message_id": received_data['session']['message_id'],
            "user_id": received_data['session']['user_id'],
        },
        "version": received_data['version']
    }


@app.route('/alice', methods=['POST'])
def alice():
    """
    The main chat bot controller for handling Yandex requests
    """
    received_data = request.get_json()

    yandex_id = received_data['session']['user_id']
    session_is_new = received_data['session']['new']
    user = AppUser.query.get(yandex_id)

    # If user exists and session is new, reset his location
    if user and session_is_new:
        user.location = []
        db.session.commit()

    # If user doesn't exist, create user
    if user is None:
        user = AppUser(yandex_id=yandex_id, username="пользователь", location=[], json_filename="data_0001.json")
        db.session.add(user)
        db.session.commit()

    # If search mode off, None.
    user_search_request = user.search_request
    command = received_data["request"]["command"].lower()

    # Saving original utterance because command will be processed
    original_utterance = command

    # If it's not the answer to specifier, lemmatize command for better understanding
    if not user_search_request:
        command = nlp_lem.lemmatize_sentence(command)
    intent = classify_intent(original_utterance, command, session_is_new, user_search_request)
    token, nl_entities = execute_action(intent, yandex_id, command)
    text = generate_text(token, nl_entities)
    response = create_response(text, received_data)
    return jsonify(response)


@app.route('/')
def hello_world():
    """
    This controller is for chat bot testing purposes
    """
    return 'Hello World!'
