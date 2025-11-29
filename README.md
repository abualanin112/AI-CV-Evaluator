# CV Evaluation & Ranking System

A smart recruitment tool that automates the process of screening CVs against job descriptions using AI.

## Features

- **Job Description Management**: Define job roles and requirements.
- **Bulk CV Upload**: Upload multiple CVs (PDF, TXT, MD) at once.
- **AI-Powered Evaluation**: Uses **Google Gemini 2.0 Flash** to analyze CVs against job requirements.
- **Smart Ranking**: Automatically ranks candidates based on a fit score (0-100).
- **Detailed Insights**: Provides strengths, weaknesses, and a summary for each candidate.
- **Automated Email Drafting**: Generates a personalized interview invitation email for the top candidate.
- **Vector Search**: Uses ChromaDB for efficient storage and retrieval of CV embeddings.

## Tech Stack

- **Backend**: Django 5.2
- **AI Model**: Google Gemini 2.0 Flash (via LangChain)
- **Vector DB**: ChromaDB
- **Frontend**: Bootstrap 5
- **Testing**: Pytest, Playwright

## Setup Instructions

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/abualanin112/AI-CV-Evaluator
    cd cv_evaluator_project
    ```

2.  **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: If `requirements.txt` is missing, install manually: `pip install django langchain-google-genai chromadb pdfplumber markdown pytest pytest-django pytest-playwright`)_

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your Google API key:

    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    GEMINI_MODEL=gemini-2.0-flash
    DEBUG=True
    SECRET_KEY=your_secret_key
    ```

5.  **Run Migrations**:

    ```bash
    python manage.py migrate
    ```

6.  **Run the Server**:

    ```bash
    python manage.py runserver
    ```

7.  **Access the App**:
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Testing

To run the test suite (Unit, Integration, and E2E):

```bash
pytest
```
