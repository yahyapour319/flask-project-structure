import json

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


def test_01_get_user(client, get_user_token):
    """
        GIVEN - a Flask application configured for testing get user api
        WHEN  - the '/api/v1/user' page is requested (GET)
        THEN  - check that the response contained required field with 200 status code
    """

    headers.update({'Authorization': 'JWT %s' % get_user_token})
    response = client.get('/api/v1/user', headers=headers)

    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["success"]
    assert "about_us" in json_data['data']
    assert "birthdate" in json_data['data']
    # ...

def test_02_get_user_invalid_token(client):
    """
        GIVEN - a Flask application configured for testing get user api with invalid token
        WHEN  - the '/api/v1/user' page is requested (GET) with invalid token
        THEN  - check that status code is 401 with Unauthorized type and message refer to token key
    """

    headers.update({'Authorization': 'JWT %s' % "fasfasfs"})
    response = client.get('/api/v1/user', headers=headers)

    json_data = response.get_json()
    assert not json_data["success"]
    assert json_data["error"]["status"] == 401
    assert json_data["error"]["type"] == "Unauthorized"
    assert "token" in json_data["error"]["detail"]


def test_03_put_user(client, get_user_token):
    """
        GIVEN - a Flask application configured for test updating user
        WHEN  - the '/api/v1/user' page is requested (PUT)
        THEN  - check that status code is 201 with success message
    """

    data = {
        "user_info":
            {
                "height": 165,
                "weight": 70
            }
        ,
        "about_us": "about user",
        "birthdate": "1990-03-10",
        "city_id": 1,
        "insurance": 2,
        "disease_records": "disease_records1",
        "email": "user@yahoo.com",
        "full_name": "mohammad mosaed",
        "gender": 2,
        "national_id": "2255448000",
        "province_id": 1
    }

    headers.update({'Authorization': 'JWT %s' % get_user_token})
    response = client.put('/api/v1/user', data=json.dumps(data), headers=headers)

    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data["success"]


def test_03_invalid_user_field(client, get_user_token):
    pass
