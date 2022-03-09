from crypt import methods
import json
import requests as global_requests

from flask import Flask, request
from waitress import serve

from table_handlers import ChannelsHandler, UsersHandler, TokensHandler

app = Flask(__name__)


@app.route('/channel_list_by_id/', methods=['GET'])
def get_channel_list_by_id():
    token = str(request.args.get('token'))

    check_is_token = tokens_handler.is_token(token)

    if check_is_token:
        user_id = tokens_handler.get_user_id(token)
        channels_list = channels_handler.get_channels_list(user_id)

        response = {
            'response': 200,
            'channels_list': channels_list,
        }

    else:
        response = {
            'response': 401
        }

    response = json.dumps(response)

    return response            

@app.route('/get_user_api_key/', methods=['GET'])
def get_user_api_key():
    token = str(request.args.get('token'))

    check_is_token = tokens_handler.is_token(token)

    if check_is_token:
        user_id = tokens_handler.get_user_id(token)
        api_key = users_handler.get_user_api_key(user_id)

        response = {
            'response': 200,
            'api_key': api_key 
        }

    else:
        response = {
            'response': 401

        }
    
    response = json.dumps(response)

    return response

@app.route('/get_user_login', methods=['GET'])
def get_user_login():
    token = str(request.args.get('login'))

    check_is_token  = tokens_handler.is_token(token)

    if check_is_token:
        user_id = tokens_handler.get_user_id(token)
        login = users_handler.get_user_login_by_id(user_id)
        
        resoponse = {
            'response': 200,
            'login': login 
        }

    else:
        response = {
            'response': 401

        }
    
    response = json.dumps(response)

    return response

@app.route('/insert_new_user/', methods=['GET'])
def post_insert_new_user():
    login = str(request.args.get('login'))
    password = str(request.args.get('password'))
    api_key = str(request.args.get('api_key'))
    
    if len(login) < 4:

        response = {
            'response': 408
        }

        response = json.dumps(response)
        return response

    if len(password) < 8:

        response = {
            'response': 409
        }

        response = json.dumps(response)
        return response

    is_api_key_correct = check_api_key(api_key)
    if not is_api_key_correct:

        response = {
            'response': 402 
        }

        response = json.dumps(response)
        return response

    is_login_in_database = users_handler.is_login(login)
    if is_login_in_database:

        response = {
            'response': 403
        }

        response = json.dumps(response)
        return response

    result = users_handler.insert_new_user(login, password, api_key)
    if result:

        response = {
            'response': 200
        }      

        response = json.dumps(response)
        return response          
    
    else:

        response = {
            'response': 404
        }

        response = json.dumps(response)
        return response

@app.route('/add_channel/', methods=['GET'])
def post_add_channel():
    token = str(request.args.get('token'))
    channel_url = str(request.args.get('channel_url'))

    check_is_token = tokens_handler.is_token(token) 

    if check_is_token:
        user_id = tokens_handler.get_user_id(token)
        api_key = users_handler.get_user_api_key(user_id)

        is_channel_url_correct = check_channel_url(api_key, channel_url)

        if is_channel_url_correct:

            result = channels_handler.add_channel(user_id, channel_url)

            if result:
                response = {
                    'response': 200
                }

            else:

                response = {
                    'response': 404
                }
        
        else:
            response = {
                'response': 407
            }
            
    else:
        response = {
            'response': 401
        }

    response = json.dumps(response)

    return response

@app.route('/del_channel/', methods=['GET'])
def delete_del_channel():
    token = str(request.args.get('token'))
    channel_url = str(request.args.get('channel_url'))

    check_is_token = tokens_handler.is_token(token)

    if check_is_token:
        user_id = tokens_handler.get_user_id(token)
        result = channels_handler.del_channel(user_id, channel_url)

        if result:

            response = {
                'response': 200,
            }

        else:

            response = {
                'response': 405,
            }
        
    else:
        response = {
            'response': 401,
        }

    response = json.dumps(response)

    return response

@app.route('/generate_token/', methods=['GET'])
def get_generated_token():
    login = str(request.args.get('login'))
    password = str(request.args.get('password'))

    check_is_account = users_handler.is_account(login, password)

    if check_is_account:
        user_id = users_handler.get_user_id_by_login(login)
        token = tokens_handler.add_token(user_id)

        response = {
            'response': 200,
            'token': token
        }

    else:
        response = {
            'response': 406,
        }

    response = json.dumps(response)

    return response

@app.route('/update_user_login/', methods=['GET'])
def update_login():
    login = str(request.args.get('login'))
    token = str(request.args.get('token'))

    if len(login) < 4:

        response = {
            'response': 408
        }

        response = json.dumps(response)
        return response    

    check_is_login = users_handler.is_login(login)

    if not check_is_login:
        check_is_token = tokens_handler.is_token(token)

        if check_is_token:
            user_id = tokens_handler.get_user_id(token)
            users_handler.update_user_login(user_id, login)

            response = {
                'response': 200
            }

        else:
            response = {
                'response': 401
            }

    else:
        response = {
            'response': 403
        }

    response = json.dumps(response)

    return response

@app.route('/update_user_api_key/', methods=['GET'])
def update_user_api_key():
    api_key = str(request.args.get('api_key'))
    token = str(request.args.get('token'))

    is_token_correct = tokens_handler.is_token(token)

    if is_token_correct:
        is_api_key_correct = check_api_key(api_key)

        if is_api_key_correct:
            user_id = tokens_handler.get_user_id(token)
        
            users_handler.update_user_api_key(user_id, api_key)

            response = {
                'response': 200
            }

        else:
            response = {
                'response': 402
            }
    
    else:
        response = {
            'response': 401
        }
    
    response = json.dumps(response)

    return response

@app.route('/test/', methods=['GET'])
def test():
    response = {'Response': 'Hello, Camilus!'}

    response = json.dumps(response)

    return response

def check_api_key(api_key: str) -> bool:
    """Проверка ключа апи тестовым запросом."""
    request = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId=UCMcC_43zGHttf9bY-xJOTwA&part=snippet,id&order=date&maxResults=1"

    resp = global_requests.get(request)
    if resp.status_code == 200:
        return True
    
    else:
        return False
    
def check_channel_url(api_key: str, channel_url: str) -> bool:
    """Проверка канала по пробному запросу."""
    channel_id = channel_url.split('/')[-1] #Получение id в ссылке.
    
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=5"

    resp = global_requests.get(url)

    if resp.status_code == 200:
        return True

    else:
        return False

if __name__=='__main__':
    users_handler = UsersHandler()
    channels_handler = ChannelsHandler()
    tokens_handler = TokensHandler()
    serve(app, host='0.0.0.0', port=12345)
