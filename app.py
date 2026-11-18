from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20


class Task(db.Model):
    """Database model representing a single task item on the board."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        """Serialize the Task instance into a JSON-compatible dictionary."""
        return {"id": self.id, "title": self.title}


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    """
    Serve the main task board HTML page.
    Renders the front-end UI where users interact with tasks via Fetch API.
    """
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve a paginated list of tasks from the SQLite database.
    Accepts optional query parameters 'page' and 'size' and returns JSON.
    """
    page = request.args.get('page', DEFAULT_PAGE, type=int)
    size = request.args.get('size', DEFAULT_PAGE_SIZE, type=int)
    pagination = Task.query.paginate(page=page, per_page=size, error_out=False)
    return jsonify({
        "tasks": [task.to_dict() for task in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200


@app.route('/api/tasks', methods=['POST'])
def add_task():
    """
    Create a new task from a JSON request body containing 'title'.
    Validates non-empty input up to 200 characters and returns HTTP 201.
    """
    data = request.get_json() or {}
    title = str(data.get('title', '')).strip()
    if not title or len(title) > 200:
        return jsonify({"error": "Title is required (max 200 characters)"}), 400

    try:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task added", "task": new_task.to_dict()}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Failed to save task"}), 500


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete an existing task identified by its integer 'task_id'.
    Returns HTTP 200 upon deletion or HTTP 404 if the task does not exist.
    """
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Failed to delete task"}), 500


if __name__ == '__main__':
    app.run(debug=True)
