from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/greet/<name>')
def name(name = None):
    return 'Hello, {}'.format(name)
@app.route('/farewell/<x>')
def bye(x = None):
    return "Goodbye, {}!".format(x)

data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    global data
    if request.method == 'POST':
        x = request.get_json()
        keys = x.keys()
        
        key = list(keys)[0]
        value = x[key]
        data[key] = value
        return 'Entry created successfully!'
    return data

@app.route('/read')
def read():
    global data
    return data

@app.route('/update', methods=['PATCH'])
def update():
    if request.method == 'PATCH':
        x = request.get_json()
        keys = x.keys()
        key = list(keys)[0]

        if key in data:
            value = x[key]
            data[key] = value
            return 'Entry updated successfully!'
        else:
            return 'Entry does not exist.'

@app.route('/delete/<key>', methods=["DELETE"])
def delete(key):
    if request.method == 'DELETE':
        if key in data:
            del data[key]
            return 'Entry deleted successfully!'
        else:
            return 'Entry does not exist.'


if __name__ == '__main__':
    app.run()