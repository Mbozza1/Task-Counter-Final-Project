from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# app = Flask(__name__)
# Create a flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  task = db.Column(db.String(200), nullable=False)
  due_date = db.Column(db.Date, nullable=False)
  tags = db.Column(db.String(200), nullable=True)
  priority = db.Column(db.String(10), nullable=False)


@app.route('/')
def index():
  tasks = Task.query.order_by(Task.due_date.asc()).all()
  today = datetime.utcnow().date()
  for task in tasks:
    task.is_overdue = task.due_date < today

  return render_template('index.html',
                         tasks=tasks,
                         search=False,
                         datetime=datetime)


@app.route('/search', methods=['POST'])
def search():
  search_query = request.form.get('search')
  search_results = Task.query.filter(
    Task.task.contains(search_query)).order_by(Task.due_date).all()
  return render_template('index.html', tasks=search_results, search=True)


@app.route('/add-task', methods=['POST'])
def add_task():
  task = request.form.get('task')
  due_date_str = request.form.get('due_date')
  due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
  priority = request.form.get('priority')
  tags_str = request.form.get('tags')
  tags = tags_str.strip() if tags_str else None

  new_task = Task(task=task, due_date=due_date, priority=priority, tags=tags)

  try:
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))
  except Exception as e:
    return str(e)


@app.route('/edit-task/<int:task_id>')
def edit_task(task_id):
  task = Task.query.get_or_404(task_id)
  return render_template('editTask.html', task=task)


@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
  task = Task.query.get(task_id)
  if task:
    task.task = request.form.get('task')
    due_date_str = request.form.get('due_date')
    task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    task.priority = request.form.get('priority')
    task.tags = request.form.get('tags')
    db.session.commit()
  return redirect(url_for('index'))


@app.route('/complete_task', methods=['POST'])
def complete_task():
  data = request.json
  task_id = data.get('task_id')
  task = Task.query.get(task_id)
  if task:
    db.session.delete(task)
    db.session.commit()
  return '', 204


if __name__ == '__main__':
  # Run the Flask app
  with app.app_context():
    db.create_all()
  app.run(host='0.0.0.0', debug=True, port=8080)
