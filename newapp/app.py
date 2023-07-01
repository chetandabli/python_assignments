from flask import Flask
app = Flask(__name__)

@app.route('/')
def green():
    return "Hello World!"

@app.route('/greet/<name>')
def name(name = None):
    return 'Hello, {}'.format(name)
@app.route('/farewell/<x>')
def bye(x = None):
    return "Goodbye, {}!".format(x)


if __name__ == '__main__':
    app.run()