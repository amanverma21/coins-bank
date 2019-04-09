#coding: utf8
"""
This module contains JSON requests for Loco server.
Some request fields will be filled
automatically from 'settings.ini' file.
Fields with '#fill' mark should be filled during
exchange with server in main script.
"""
import configparser
import re

config = configparser.ConfigParser()
config.read('settings.ini')

client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']
device_id = config['DEFAULT']['device_id']

# get sms code from Loco
def fill_sms_code_request(country_abbrev, national_number):
    global client_id
    global client_secret

    sms_code_request = {
        'url' : 'https://api.getloconow.com:443/v2/user/phone/send_verification_code/',
        'headers' : {
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'X-APP-VERSION':'10150',
            'X-PLATFORM':'5',
            'X-APP-LANGUAGE':'1',
            'Content-Type':'application/json; charset=UTF-8',
            'Content-Length':'240', # will be recalculated before send
            'Host':'api.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        },
        'data' : {
            u'client_id': client_id,
            u'client_secret': client_secret,
            u'country': country_abbrev,
            u'phone': national_number
        }
    }
    return sms_code_request

# send sms code to Loco
def fill_send_sms_code_request(country_abbrev, national_number, sms_code):
    global client_id
    global client_secret
    send_code_request = {
        'url' : 'https://api.getloconow.com:443/v2/user/verify/',
        'headers' : {
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'X-APP-VERSION':'10150',
            'X-PLATFORM':'5',
            'X-APP-LANGUAGE':'1',
            'Content-Type':'application/json; charset=UTF-8',
            'Content-Length':'267', # will be recalculated before send
            'Host':'api.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        },
        'data' : {
            u'client_id': client_id,
            u'client_secret': client_secret,
            u'code': sms_code, # fill sms code
            u'country': country_abbrev,
            u'language': u'1',
            u'phone': national_number
        }
    }
    return send_code_request

# authorization with given token
def fill_auth_with_token_request(token_type, token):
    global device_id
    authorization = ' '.join([token_type, token])

    auth_with_token_request = {

        'url' : 'https://api.getloconow.com:443/v2/user/me/',

        'headers' : {
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'X-APP-VERSION':'10150',
            'X-APP-LANGUAGE':'1',
            'X-PLATFORM':'5',
            'Device-Id': device_id,
            'Authorization': authorization,
            'Host':'api.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        }
    }
    return auth_with_token_request

# getting info for game with given index
def fill_game_info_request(profile_token, game_index):
    global device_id
    game_info_request = {

        'url' : 'https://pastgames.getloconow.com/v1/game/info/',

        'headers' : {
            'item-index': str(game_index),
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'Authorization': profile_token,
            'X-APP-VERSION':'10150',
            'X-APP-LANGUAGE':'1',
            'X-PLATFORM':'5',
            'Device-Id': device_id,
            'Host':'pastgames.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        }

    }
    return game_info_request

# game event starting
def fill_game_create_request(profile_token, game_index, game_uid):
    global device_id
    game_create_request = {

        'url' : 'https://pastgames.getloconow.com:443/v1/event/create/',

        'headers' : {
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'Authorization': profile_token,
            'X-APP-VERSION':'10150',
            'X-APP-LANGUAGE':'1',
            'X-PLATFORM':'5',
            'Device-Id': device_id,
            'Content-Type':'application/json; charset=UTF-8',
            'Content-Length':'267', # will be recalculated before send
            'Host':'pastgames.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        },

        'data' : {
            'contestUid' : game_uid,
            'itemIndex' : game_index, # fill
        },
    }
    return game_create_request

# requesing next question from game event with EVENT_UID id.
# game with this id should be created earlier
# with 'game_create_request'.
# game event starting
def fill_question_request(profile_token, event_uid):
    global device_id
    question_request = {

        'url' : 'https://pastgames.getloconow.com:443/v1/event/EVENT_UID/question/',

        'headers' : {
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'Authorization': profile_token, # fill
            'X-APP-VERSION':'10150',
            'X-APP-LANGUAGE':'1',
            'X-PLATFORM':'5',
            'Device-Id': device_id,
            'Content-Length':'0',
            'Host':'pastgames.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        },
    }

    question_request['url'] = \
        re.sub(r'(https://.*/v1/event/).*(/question/)', \
        r'\1PLACEHOLDER\2', \
        question_request['url']).replace('PLACEHOLDER',event_uid)

    return question_request

# sending answer
def fill_answer_request(profile_token, event_uid, answer_index, question_uid):
    global device_id
    answer_request = {

        'url' : 'https://pastgames.getloconow.com:443/v1/event/EVENT_UID/answer/',

        'headers' : {
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'Authorization': profile_token, # fill
            'X-APP-VERSION':'10150',
            'X-APP-LANGUAGE':'1',
            'X-PLATFORM':'5',
            'Device-Id': device_id,
            'Content-Type':'application/json; charset=UTF-8',
            'Content-Length':'0',
            'Host':'pastgames.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        },

        'data' : {
            'rank' : str(answer_index), # fill (answer number)
            'questionUid' : question_uid, # fill
        },
    }
    answer_request['url'] = \
        re.sub(r'(https://.*/v1/event/).*(/answer/)', \
        r'\1PLACEHOLDER\2', \
        answer_request['url']).replace('PLACEHOLDER',event_uid)

    return answer_request

# getting statistics for event with EVENT_UID id.
def fill_stats_request(profile_token, event_uid):
    global device_id
    stats_request = {

        'url' : 'https://pastgames.getloconow.com:443/v1/event/EVENT_UID/stats/',

        'headers' : {
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 3W Build/KTU84P)',
            'Authorization': 'LONG_ID', # fill
            'X-APP-VERSION':'10150',
            'X-APP-LANGUAGE':'1',
            'X-PLATFORM':'5',
            'Device-Id': device_id,
            'Host':'pastgames.getloconow.com',
            'Connection':'Keep-Alive',
            'Accept-Encoding':'gzip',
        },
    }
    return stats_request

