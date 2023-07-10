import json
from app import app
from app import weather_data

def test_get_weather_valid_city():
    client = app.test_client()
    response = client.get('/weather/San Francisco')
    assert response.status_code == 200
    assert json.loads(response.data) == {'temperature': 14, 'weather': 'Cloudy'}

def test_get_weather_invalid_city():
    client = app.test_client()
    response = client.get('/weather/Chicago')
    assert response.status_code == 200
    assert response.data == b"Weather information not available for Chicago"

def test_post_weather():
    client = app.test_client()
    response = client.post('/weather/Pune', json={'info': {'temperature': 28, 'weather': 'Sunny'}})
    assert response.status_code == 200
    assert response.data == b"City data posted"

def test_put_weather():
    client = app.test_client()
    response = client.put('/weather/Pune', json={'info': {'temperature': 41, 'weather': 'Hot'}})
    assert response.status_code == 200
    assert response.data == b"City data updated"

def test_delete_weather():
    client = app.test_client()
    response = client.delete('/weather/Pune')
    assert response.status_code == 200
    assert response.data == b"City data deleted"


