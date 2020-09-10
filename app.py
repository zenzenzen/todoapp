from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)  #__name__ specifies that the application will take on the same name as the file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/todoapp'
dbObject = SQLAlchemy(app) # Call in a db object that we can use to perform CRUD operations.

migrate = Migrate(app, dbObject)


class ToDo(dbObject.Model):
    __tablename__ = 'todos'
    id = dbObject.Column(dbObject.Integer, primary_key=True)
    description = dbObject.Column(dbObject.String(), nullable=False)
    completed = dbObject.Column(dbObject.Boolean, nullable=False, default = False)
    # completed = dbObjectColumn(dbObjectBoolean, nullable=True)

    def __repr__(self): #built-in reprint method for debugging
        return f'<Todo {self.id} {self.description}'

# dbObject.create_all()   --> No longer required because we're using Flask-Migrate now.

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        newDescription = request.get_json()['description']
        newItem = ToDo(description=newDescription)
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
    if not error:
        return jsonify(body)
    if error:
        abort(500)

@app.route('/')
def index():
    return render_template('index.html', data=ToDo.query.all()
    )

# if __name__ == '__main__':
#     app.run()
