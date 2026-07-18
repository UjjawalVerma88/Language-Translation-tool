<<<<<<< HEAD
# Lingo — Language Translation Tool

A clean, single-page web app that translates text between languages using the
Microsoft Translator API, built with Flask. Translation happens over AJAX
(no page reloads), with a chat-bubble style result, language swap, copy-to-clipboard,
and loading states.

## Features

- Translate text between 9 common languages, with auto-detect for the source language
- Instant, no-reload translation via a small JSON API (`/api/translate`)
- Swap source/target languages with one click
- Copy the translated result to your clipboard
- Secrets are loaded from environment variables only — safe to make this repo public

## Prerequisites

- Python 3.9+
- An [Azure Translator](https://azure.microsoft.com/en-us/products/ai-services/ai-translator) resource (subscription key + region)

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/language-translation-tool.git
   cd language-translation-tool
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Azure Translator credentials**

   Copy `.env.example` to `.env` and fill in your own key and region:

   ```bash
   cp .env.example .env
   ```

   ```
   AZURE_TRANSLATOR_KEY=your-azure-translator-key-here
   AZURE_TRANSLATOR_REGION=centralindia
   ```

   `.env` is git-ignored, so your key never gets committed.

4. **Run the app**

   ```bash
   python3 app.py
   ```

   Then open http://127.0.0.1:5000 in your browser.

## Project structure

```
.
├── app.py              # Flask app: page route + /api/translate JSON endpoint
├── requirements.txt
├── .env.example         # Copy to .env and fill in your own credentials
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    └── index.html
```

## Security note

Never commit a real `.env` file or hardcode API keys in source files. If a key
is ever exposed in a commit or a shared file, rotate it in the Azure portal
immediately rather than just removing it from the code.
=======
# Language-Translation-tool
A Flask-based Language Translation Tool powered by Microsoft Azure Translator API with real-time translation, language detection, copy-to-clipboard, and a clean responsive UI.
>>>>>>> f0f21840aacbb1e62f2085793eafb2605964c140
