from flask import Flask, render_template, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate
import sys

app = Flask(__name__)  #__name__ specifies that the application will take on the same name as the file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
dbObject = SQLAlchemy(app) # Call in a db object that we can use to perform CRUD operations.

migrate = Migrate(app, dbObject)

class ToDoList(dbObject.Model):
    __tablename__ = 'todolists'
    id = dbObject.Column(dbObject.Integer, primary_key=True)
    listName = dbObject.Column(dbObject.String(), nullable=False)
    todos = dbObject.relationship('ToDo', backref='lists', lazy=True)

class ToDo(dbObject.Model):
    __tablename__ = 'todos'
    id = dbObject.Column(dbObject.Integer, primary_key=True)
    description = dbObject.Column(dbObject.String(), nullable=False)
    completed = dbObject.Column(dbObject.Boolean, nullable=False)
    listID = dbObject.Column(dbObject.Integer, dbObject.ForeignKey('todolists.id'))

    def __repr__(self): #built-in reprint method for debugging
        return f'<Todo {self.id} {self.description} {self.completed}'



# dbObject.create_all()   --> No longer required because we're using Flask-Migrate now.

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        newDescription = request.get_json()['description']
        newItem = ToDo(description=newDescription, completed=False)
        dbObject.session.add(newItem)       
        dbObject.session.commit()    
        body['description'] = newItem.description   #  Circumvent expire_on_commit issues
                                                    # by maintaining desc data after commit
                                                    # to actively update page w/o refresh
                                                    # and prevent accessing stale object after
                                                    # the commit.
    except:
        error = True
        dbObject.session.rollback()
        print(sys.exc_info())
        
    finally:
        dbObject.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = ToDo.query.get(todo_id)
    todo.completed = completed
    dbObject.session.commit()
  except:
    dbObject.session.rollback()
  finally:
    dbObject.session.close()
  return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])  # Don't need to have additional '/delete' path after <todo_id>
def delete_todo(todo_id):
    # validDelete = make_response(jsonify({}), 204)
    deleteTag = int(todo_id)
    try:
        ToDo.query.filter_by(id = deleteTag).delete() # I had an extra = for "X == Y" 
                                                      # Turns out maybe this is unnecessary
        dbObject.session.commit()
    except:
        dbObject.session.rollback()
    finally:
        dbObject.session.close()
        return jsonify({'success':True})

@app.route('/lists/<list_id>')
def index(list_id):
    return render_template('index.html', 
    data=ToDo.query.filter_by(list_id=ListID).order_by('id')
    .all()

# if __name__ == '__main__':
#     app.run()