#coding: utf8
"""
"""
import time
import json
import sys
from random import randrange
import re

# Loco server requests
from loco_requests import \
    fill_sms_code_request, \
    fill_send_sms_code_request, \
    fill_auth_with_token_request, \
    fill_game_info_request, \
    fill_game_create_request, \
    fill_question_request, \
    fill_answer_request, \
    fill_stats_request


from network_functions import \
    POST_and_get_JSON_response, \
    GET_and_get_JSON_response

def log_msg(country_abbrev, national_number, msg):
    print('{0}.{1}: {2}'.format(country_abbrev, national_number, msg))

"""
Getting SMS code from Loco server
"""
def get_sms_code_from_Loco(country_abbrev, national_number):

    request = fill_sms_code_request(country_abbrev=country_abbrev,
                                    national_number=national_number)

    json_response = POST_and_get_JSON_response(request['url'], \
                            request['headers'], request['data'])
    if json_response is None or 'authentication_key' not in json_response:
        log_msg(country_abbrev, national_number, 'Wrong response')
        return None

    log_msg(country_abbrev, national_number, 'SMS code is sent')
    return json_response

"""
Authorizing with SMS code
"""
def authorize(country_abbrev, national_number, sms_code) -> 'profile_token':

    # sending SMS code to Loco
    request = fill_send_sms_code_request(country_abbrev=country_abbrev,
                                         national_number=national_number,
                                         sms_code=sms_code)

    json_response = POST_and_get_JSON_response(request['url'], \
                            request['headers'], \
                            request['data'])

    if json_response is None or 'access_token' not in json_response:
        log_msg(country_abbrev, national_number, 'Wrong response')
        return None

    # trying to authorize
    access_token = json_response['access_token']
    token_type = json_response['token_type']
    request = fill_auth_with_token_request(token_type=token_type,
                                           token=access_token)

    log_msg(country_abbrev, national_number,
            'trying to authorize with {0} token: {1}...'.\
                format(token_type, access_token))
    json_response = GET_and_get_JSON_response(request['url'], \
                            request['headers'])

    if json_response is None:
        log_msg(country_abbrev, national_number, 'Wrong response')
        return None

    full_name = json_response['full_name']
    user_name = json_response['username']
    profile_token = json_response['token']
    log_msg(country_abbrev, national_number,
            'Authorized. user_name: {0}, full_name: {1}'.\
            format(user_name, full_name))

    return profile_token


ERR_CODE_MAIN_LOOP=1
def main_play_loop(country_abbrev, national_number, profile_token):

    global ERR_CODE_MAIN_LOOP

    status_dict = {
        'total_coins' : 0,
        'questions' : 0,
        'games' : 0,
    }
    yield status_dict

    for i in range(500):

        time.sleep(0.2)

        # getting game info
        log_msg(country_abbrev, national_number, 'getting game info (index={0}'.\
                format(i))
        request = fill_game_info_request(profile_token, i)
        json_response = GET_and_get_JSON_response(request['url'], \
                                request['headers'])

        if json_response is None or 'data' not in json_response \
                or 'uid' not in json_response['data']:
            log_msg(country_abbrev, national_number, 'Wrong response')
            yield {'error' : ERR_CODE_MAIN_LOOP}
            return None

        # starting game
        log_msg(country_abbrev, national_number, 'starting game')
        contest_uid = json_response['data']['uid']
        request = fill_game_create_request(profile_token, i, contest_uid)
        json_response = POST_and_get_JSON_response(request['url'], \
                                request['headers'],\
                                request['data'])

        if json_response is None:
            log_msg(country_abbrev, national_number, 'Wrong response')
            yield {'error' : ERR_CODE_MAIN_LOOP}
            return None

        if not json_response['success']:
            log_msg(country_abbrev, national_number,
                    'Can\'t start game. Trying again...')
            continue

        event_uid = json_response['data']['event_uid'].lstrip()
        total_questions = json_response['data']['total_questions']

        question_request = fill_question_request(profile_token, event_uid)
        answer_request = fill_answer_request(profile_token, event_uid, 0, '*')
        # answering questions
        for q in range(total_questions):

            # requesting question
            json_response = POST_and_get_JSON_response(question_request['url'], \
                                    question_request['headers'])

            if json_response is None:
                log_msg(country_abbrev, national_number, 'question: wrong response')
                yield {'error' : ERR_CODE_MAIN_LOOP}
                return None

            if not json_response['success']:
                log_msg(country_abbrev, national_number,
                        'Can\'t get question. Restarting game...')
                break

            question_uid = json_response['data']['question_uid']
            print('question {0}'.format(q+1))

            #time.sleep(1)

            answer_request['data']['rank'] = str(randrange(3))
            answer_request['data']['questionUid'] = question_uid

            json_response = POST_and_get_JSON_response(answer_request['url'], \
                                    answer_request['headers'], \
                                    answer_request['data'])

            if json_response is None:
                log_msg(country_abbrev, national_number, 'answer: wrong response')
                yield {'error' : ERR_CODE_MAIN_LOOP}
                return None

            if not json_response['success']:
                log_msg(country_abbrev, national_number,
                        'Can\'t send answer. Restarting game...')
                break

            # updating status
            try:
                coins_earned = int(json_response['data']['coins_earned'])
            except:
                log_msg(country_abbrev, national_number,
                        'answer: can\'t get coins count')
                yield {'error' : ERR_CODE_MAIN_LOOP}
                return None

            status_dict['total_coins'] += coins_earned #TODO: get from response
            status_dict['questions'] += 1
            yield status_dict

        # updating game count
        if json_response['success']:
            status_dict['games'] += 1
            yield status_dict
