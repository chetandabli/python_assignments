from flask import Flask, request

app = Flask(__name__)

weather_data = {
    'San Francisco': {'temperature': 14, 'weather': 'Cloudy'},
    'New York': {'temperature': 20, 'weather': 'Sunny'},
    'Los Angeles': {'temperature': 24, 'weather': 'Sunny'},
    'Seattle': {'temperature': 10, 'weather': 'Rainy'},
    'Austin': {'temperature': 32, 'weather': 'Hot'},
}

@app.route('/weather/<string:city>')
def get_weather(city):
    if city in weather_data:
        return weather_data[city]
    else:
        return f"Weather information not available for {city}"
    
@app.route('/weather/<string:city>', methods=['POST'])
def post_weather(city):
    data = request.get_json()
    weather = data["info"]
    weather_data[city] = weather
    return "City data posted"

@app.route('/weather/<string:city>', methods=['PUT'])
def put_weather(city):
    data = request.get_json()
    weather = data["info"]
    weather_data[city] = weather
    return "City data updated"

@app.route('/weather/<string:city>', methods=['DELETE'])
def delete_weather(city):
    del weather_data[city]
    return "City data deleted"

if __name__ == '__main__':
    app.run()
