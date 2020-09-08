from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  #__name__ specifies that the application will take on the same name as the file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/todoapp'
dbObject = SQLAlchemy(app) # Call in a db object that we can use to perform CRUD operations.



class ToDo(dbObject.Model):
    __tablename__ = 'todos'
    id = dbObject.Column(dbObject.Integer, primary_key=True)
    description = dbObject.Column(dbObject.String(), nullable=False)
    # completed = dbObjectColumn(dbObjectBoolean, nullable=True)

    def __repr__(self): #built-in reprint method for debugging
        return f'<Todo {self.id} {self.description}'

dbObject.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=ToDo.query.all()
    )


@app.route('/todos/create', methods=['POST'])
def create_todo():
    newDescription = request.get_json()['description']
    newItem = ToDo(description=newDescription)
    dbObject.session.add(newItem)       #ignore the red underline
    dbObject.session.commit()

    #you should redirect after finishing... instead of returning the home view
    return jsonify({
        'description': newItem.description
    })

# if __name__ == '__main__':
#     app.run()