# Dynamic Task Board (Heroku Deployed)

A full-stack task board web application built with Flask, SQLite, Bootstrap 5, and the JavaScript Fetch API, configured for production deployment on Heroku with GitHub Actions CI/CD.

## Live Application
- **Heroku Live URL**: `https://herokuapp.com`
- **Health / API Check**: `GET /api/tasks`

## Deployment & CI/CD Setup
- **`Procfile`**: Configured with `web: gunicorn app:app` to run the Flask application using Gunicorn in production.
- **`runtime.txt`**: Pins Python `3.11.9` for reproducible builds on Heroku.
- **`requirements.txt`**: Includes `Flask`, `Flask-SQLAlchemy`, and `gunicorn`.
- **CI/CD Pipeline**: Automated via `.github/workflows/heroku.yml` to verify dependencies and deploy on every push to `main`.

## How to Deploy to Heroku Manually
1. Install the Heroku CLI and log in: `heroku login`
2. Create a Heroku app: `heroku create sanika-dynamic-task-board`
3. Push to Heroku: `git push heroku main`
4. Open live app: `heroku open`
