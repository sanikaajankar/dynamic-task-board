# Dynamic Task Board

A full-stack task board web application built with Flask, SQLite, Bootstrap 5, and the JavaScript Fetch API for dynamic DOM updates without page reloads.

## Features
- **Fetch API Integration**: Uses asynchronous `GET`, `POST`, and `DELETE` requests to sync tasks with the backend.
- **Dynamic DOM Manipulation**: Adds and removes task items in real time without refreshing the page.
- **Persistent SQLite Storage**: Stores tasks using Flask-SQLAlchemy.

## API Endpoints
- `GET /` - Serves the dynamic task board interface.
- `GET /api/tasks` - Returns a JSON list of all tasks.
- `POST /api/tasks` - Creates a new task from JSON `{"title": "Task name"}`.
- `DELETE /api/tasks/<id>` - Deletes a task by ID.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `python app.py`
3. Open `http://localhost:5000/` in your browser.
