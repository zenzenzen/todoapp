from flask import Flask, render_template
app = Flask(__name__)  #__name__ specifies that the application will take on the same name as the file.

@app.route('/')
def index():
    return render_template('index.html', data=[{
        'description': 'Todo 1'
    }, {
        'description': 'Todo 2'
    }, {
        'description': 'Todo 3'
    }, {
        'description': 'Todo 4'
    }])