import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message # import functions from worker.py
from flask_cors import CORS
import os

# initialize flask app
application = Flask(__name__)

# set CORS policy: allow or prevent web pages from making requests to different domains than the one that served the web page
# * means allowing any request
cors = CORS(application, resources={r"/*": {"origins": "*"}})

# three functions that are defined as routes
# 1. the user initially send a request to go to '/' homepage endpoint
# the request trigger this 'index' function and execute the code
@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 2. process requests and handle sending info between apps
@application.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech-to-text")
    audio_binary = request.data # Get the user's speech from their request
    text = speech_to_text(audio_binary) # Call speech_to_text function to transcribe the speech

    # Return the response back to the user in JSON format
    response = application.response_class(
        response=json.dumps({'text': text}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    print(response.data)
    return response

# 3. process requests and handle sending info between apps
@application.route('/process-message', methods=['POST'])
def process_prompt_route():
    user_message = request.json['userMessage'] # Get user's message from their request
    print('user_message', user_message)
    voice = request.json['voice'] # Get user's preferred voice from their request
    print('voice', voice)

    # Call openai_process_message function to process the user's message and get a response back
    openai_response_text = openai_process_message(user_message)

    # Clean the response to remove any empty lines
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])

    # Call our text_to_speech function to convert OpenAI Api's response to speech
    openai_response_speech = text_to_speech(openai_response_text, voice)

    # convert openai_response_speech to base64 string so it can be sent back in the JSON response
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')

    # Send a JSON response back to the user containing their message's response both in text and speech formats
    response = application.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    return response

# starts the server
if __name__ == "__main__":
    application.run(port=8000, host='0.0.0.0') # server runs on port 8000 and have a host be 0.0.0.0 aka localhost
