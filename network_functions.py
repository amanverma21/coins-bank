import requests
import json
"""
This module contains networking functions.
"""

# perform HTTP POST request and get JSON response content
def POST_and_get_JSON_response(url, headers, data=None):
    if not data is None:
        data = json.dumps(data, ensure_ascii=False)
        headers['Content-Length'] = str(len(data))

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError:
        print('ERROR: connection error')
        return None
    except Timeout:
        print('ERROR: response timeout')
        return None
    except:
        print('ERROR: can\'t get response')
        return None

    if not response.ok:
        print('ERROR: response is not OK')
        print(response)
    try:
        return response.json()
    except:
        print('ERROR: no valid JSON in response')
        return None

# perform HTTP GET request and get JSON response content
def GET_and_get_JSON_response(url, params):

    try:
        response = requests.get(url=url, headers=params)
    except ConnectionError:
        print('ERROR: connection error')
        return None
    except Timeout:
        print('ERROR: response timeout')
        return None
    except:
        print('ERROR: can\'t get response')
        return None

    if not response.ok:
        print('ERROR: response is not OK')
        print(response)
    try:
        return response.json()
    except:
        print('ERROR: no valid JSON in response')
        return None
