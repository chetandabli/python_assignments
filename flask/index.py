from flask import Flask

app = Flask(__name__)

@app.route('/')
def green():
    return "Hello World!"

@app.route('/farewell/')
def bye():
    return "Goodbye"

@app.route('/greet/<name>')
def greet(name=None):
    if name:
        return 'Hello, {}'.format(name)
    else:
        return "Hello World!"

@app.route('/farewell/<name>')
def farewell(name=None):
    if name:
        return "Goodbye, {}!".format(name)
    else:
        return "Goodbye"

if __name__ == '__main__':
    app.run()
