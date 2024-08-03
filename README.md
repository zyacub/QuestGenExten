# QuizGen Chrome Extension

QuestGen is a Chrome extension that automatically generates quiz questions based on the content of the user's current website. It uses natural language processing and machine learning to create relevant questions, helping users better understand and retain information from web pages they visit.

## Features

- Automatically generates 10 quiz questions from the current web page
- Stores questions and sources in a database for quick retrieval
- Provides a user-friendly interface to answer questions and track progress
- Allows users to rate the helpfulness of generated questions

## Technology Stack

### Backend (API)

- FastAPI
- SQLAlchemy
- PostgreSQL
- OpenAI's GPT-3.5 Turbo
- Newspaper3k for web scraping

### Frontend (Chrome Extension)

- HTML/CSS/JavaScript
- Chrome Storage API

## Setup and Installation

### Backend

1. Clone the repository
2. Install the required packages.
3. Set up a PostgreSQL database and update the `DATABASE_URL` in `config.py`
4. Set your OpenAI API key in a `.env` file.
5. Run the FastAPI server.

### Frontend (Chrome Extension)

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right corner
3. Click "Load unpacked" and select the directory containing the extension files
4. The QuizGen extension should now be visible in your Chrome toolbar

## Usage

1. Navigate to any web page you want to generate questions for
2. Click on the QuizGen extension icon in your Chrome toolbar
3. The extension will automatically generate 10 questions based on the page content
4. Answer the questions and rate their helpfulness
5. View your progress and performance in the extension interface

## API Endpoints

- `GET /`: Root endpoint
- `GET /url/{full_path:path}`: Generate questions for a given URL
- `POST /questions/create`: Create new questions in the database
- `GET /questions/db`: Retrieve all questions from the database
- `GET /questions/get/{path}`: Get questions for a specific URL
- `DELETE /questions/delete/{path}`: Delete questions for a specific URL
   
