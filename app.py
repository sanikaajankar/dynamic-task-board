import os
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    """Database model representing a task on the dynamic board."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title}


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    """Render the main task board web page."""
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Return paginated tasks as a JSON list."""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)
    pagination = Task.query.paginate(page=page, per_page=size, error_out=False)
    return jsonify({
        "tasks": [task.to_dict() for task in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200


@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Create a new task from JSON payload."""
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
    """Delete a task by its ID."""
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
    app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1')
