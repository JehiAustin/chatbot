# ChatGPT Clone

A simple Django chat app that talks to an AI (OpenAI or built-in mock). Use the web UI or the JSON API to send messages and get responses.

## Features

- **Web chat** – Submit questions and see conversation history on one page
- **REST API** – `POST /api/chat/` with JSON `{"question": "..."}` for integration with other apps
- **OpenAI** – Real answers when `OPENAI_API_KEY` is set
- **Mock AI** – Works without an API key; uses predefined replies for greetings and random mock answers for other questions
- **Normal queries** – Greetings like "hi", "hello", "what is your name?" always get friendly replies (no API call, saves quota)
- **Sample data** – Management command to seed the database with example Q&A

## Prerequisites

- Python 3.9+
- pip (or your preferred package manager)

## Installation

1. **Clone or open the project**
   ```bash
   cd chatgpt_app
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**  
   Create a `.env` file in the project root (same folder as `manage.py`):

   ```env
   # Optional: use real OpenAI (leave unset to use Mock AI)
   OPENAI_API_KEY=sk-your-key-here

   # Optional: force Mock AI even when OPENAI_API_KEY is set
   USE_MOCK_AI=0
   ```

   - **No `OPENAI_API_KEY`** → Mock AI only  
   - **Set `OPENAI_API_KEY`** → OpenAI for non-greeting questions; greetings still use built-in replies  
   - **Set `USE_MOCK_AI=1`** → Always use Mock AI (no API calls)

5. **Database**
   ```bash
   python manage.py migrate
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

   Open **http://127.0.0.1:8000/** in your browser.

## Usage

### Web UI

- Go to **http://127.0.0.1:8000/**
- Type a message and click **Send**
- Greetings (hi, hello, what is your name, etc.) get instant replies; other questions use OpenAI or Mock AI

### API

**Endpoint:** `POST /api/chat/`

**Request:**
```json
{ "question": "What is Python?" }
```

**Success (200):**
```json
{ "answer": "Python is a programming language..." }
```

**Error (4xx/5xx):**
```json
{ "error": "Question is required" }
```

Example with curl:
```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

### Sample queries (seed data)

Add example messages to the database (uses your current AI: OpenAI or Mock):

```bash
python manage.py run_sample_queries
```

Clear existing messages and then add samples:

```bash
python manage.py run_sample_queries --clear
```

Sample questions include: Hi, Hello, What is your name?, How are you?, What can you do?, plus Python, Django, REST APIs, clean code, and machine learning.

### Admin

Create a superuser to manage chat messages in the Django admin:

```bash
python manage.py createsuperuser
```

Then open **http://127.0.0.1:8000/admin/** and log in.

## How the AI works

| Situation | Behavior |
|-----------|----------|
| Message is a **normal query** (hi, hello, what is your name?, thanks, bye, etc.) | Always returns a predefined friendly reply. **No API call.** |
| **No `OPENAI_API_KEY`** or **`USE_MOCK_AI=1`** | Other messages get a random **Mock AI** response. |
| **`OPENAI_API_KEY`** set and not mock | Other messages are sent to **OpenAI** (e.g. gpt-3.5-turbo). |
| OpenAI fails (quota, network, etc.) | Falls back to Mock AI so the user still gets a reply. |

## Project structure

```
chatgpt_app/
├── manage.py
├── requirements.txt
├── .env                    # Your env vars (create this; not in git)
├── chat/
│   ├── llm.py              # AI logic: normal queries, mock, OpenAI
│   ├── models.py           # ChatMessage (question, answer, created_at)
│   ├── views.py            # chat_view (web), chat_api (JSON)
│   ├── urls.py             # / and /api/chat/
│   ├── templates/chat/     # chat.html
│   └── management/commands/
│       └── run_sample_queries.py
└── chatgpt_app/
    ├── settings.py
    └── urls.py
```

## Tech stack

- **Django 4.2**
- **OpenAI** (optional) for real AI responses
- **django-cors-headers** for cross-origin API access
- **python-dotenv** for loading `.env`

## License

Use and modify as you like.
