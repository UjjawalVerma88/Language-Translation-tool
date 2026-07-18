from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

import os
from dotenv import load_dotenv

# Secrets always come from the environment (.env locally, real env vars in
# production) — never hardcoded, so this repo is safe to make public.
load_dotenv()

SUBSCRIPTION_KEY = os.environ.get('AZURE_TRANSLATOR_KEY', 'AZURE_TRANSLATOR_KEY')
REGION = os.environ.get('AZURE_TRANSLATOR_REGION', 'centralindia')

if not SUBSCRIPTION_KEY:
    print(
        "WARNING: AZURE_TRANSLATOR_KEY is not set. Copy .env.example to .env "
        "and add your Azure Translator key before making requests."
    )

# Microsoft Translator API function
def translate_text_microsoft(text, target_language, subscription_key, region, source_language=''):
    if not subscription_key:
        return "Error: AZURE_TRANSLATOR_KEY is not configured on the server."

    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    params = {
        'api-version': '3.0',
        'to': target_language,
        'from': source_language
    }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'Ocp-Apim-Subscription-Region': region
    }
    body = [{
        'text': text
    }]
    try:
        response = requests.post(endpoint, params=params, headers=headers, json=body, timeout=10)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    if response.status_code == 200:
        translated_text = response.json()[0]['translations'][0]['text']
        return translated_text
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ''
    if request.method == 'POST':
        text = request.form['text']
        target_language = request.form['target_language']
        source_language = request.form.get('source_language', '')
        translated_text = translate_text_microsoft(text, target_language, SUBSCRIPTION_KEY, REGION, source_language)
    return render_template('index.html', translated_text=translated_text)

@app.route('/api/translate', methods=['POST'])
def api_translate():
    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    target_language = data.get('target_language', 'en')
    source_language = data.get('source_language', '')

    if not text:
        return jsonify({'error': 'Enter some text to translate.'}), 400

    result = translate_text_microsoft(text, target_language, SUBSCRIPTION_KEY, REGION, source_language)
    is_error = result.startswith('Error:') or result.startswith('Request failed:')
    if is_error:
        return jsonify({'error': result}), 502
    return jsonify({'translated_text': result})


if __name__ == '__main__':
    app.run(debug=True)