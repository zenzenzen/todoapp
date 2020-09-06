from flask import Flask
app = Flask(__name__)  #__name__ specifies that the application will take on the same name as the file.

@app.route('/')
def index():
    render_template('index.html')