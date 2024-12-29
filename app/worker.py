from openai import OpenAI # import gpt-3 model from openai
import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from the .env file
load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# get the api key, region and instance from environment variables
api_key_stt = os.getenv('IBM_API_KEY_STT')
region_stt = os.getenv('IBM_REGION_STT')
instance_stt = os.getenv('INSTANCE_STT')
api_key_tts = os.getenv('IBM_API_KEY_TTS')
region_tts = os.getenv('IBM_REGION_TTS')
instance_tts = os.getenv('INSTANCE_TTS')

def speech_to_text(audio_binary):

    # Set up Watson Speech-to-Text HTTP Api url
    # base_url = '...'
    # api_url = base_url+'/speech-to-text/api/v1/recognize'
    base_url = f'https://api.{region_stt}.speech-to-text.watson.cloud.ibm.com'
    api_url = f"{base_url}/instances/{instance_stt}/v1/recognize"

    # Set up parameters for our HTTP request
    params = {
        'model': 'en-US_Multimedia',
    }

    # Set up the body of our HTTP request
    body = audio_binary

    # Send a HTTP Post request
    # response = requests.post(api_url, params=params, data=audio_binary).json()
    response = requests.post(api_url, params=params, data=audio_binary, auth=HTTPBasicAuth('apikey', api_key_stt)).json()

    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text


def text_to_speech(text, voice=""):
    # Set up Watson Text-to-Speech HTTP Api url
    # base_url = '...'
    # api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    base_url = f'https://api.{region_tts}.text-to-speech.watson.cloud.ibm.com'
    api_url = f"{base_url}/instances/{instance_tts}/v1/synthesize?output=output_text.wav"

    # Adding voice parameter in api_url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    # Set the headers for our HTTP request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }

    # Send a HTTP Post request to Watson Text-to-Speech Service
    response = requests.post(api_url, headers=headers, json=json_data, auth=HTTPBasicAuth('apikey', api_key_tts))
    print('text to speech response:', response)
    return response.content


def openai_process_message(user_message):
    # Set the prompt for OpenAI Api
    prompt = "Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations."
    # Call the OpenAI Api to process our prompt
    openai_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=4000
    )
    print("openai response:", openai_response)
    # Parse the response to get the response message for our prompt
    response_text = openai_response.choices[0].message.content
    return response_text
