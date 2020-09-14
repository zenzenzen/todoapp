from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

#   THIS CODE WAS COPY+PASTED FROM THE UDACITY COURSE.
#   IT IS BEING USED TO PROVIDE A CONTROL AND DEBUG ISSUES IN THE MAIN
#   COURSE WORK THAT I'M CURRENTLY WORKING THROUGH.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://developer@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
  description = request.get_json()['description']
  todo = Todo(description=description, completed=False)
  db.session.add(todo)
  db.session.commit()
  return jsonify({
    'description': todo.description
  })

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.order_by('id').all())