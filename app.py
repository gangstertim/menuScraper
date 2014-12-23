import json, logging
from flask import Flask, request
from flask_script import Manager
from getMenus import GetMenu

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
manager = Manager(app)
getMenu  = GetMenu()

if __name__ == '__main__':
    manager.run()

@app.route('/', methods=['POST'])
def index():
    post = [s.strip() for s in request.form['text'].lower().strip().split(':', 2)]
    user = request.form['user_name']
    app.logger.info('Raw: {}\tPost: {}\tUser: {}'.format(request.form['text'], post, user))
    orderbot_response = orderbot(user, post)
    app.logger.info('Orderbot response: {}'.format(orderbot_response))
    response = post_message(orderbot_response)
    app.logger.info('Response to slack: {}'.format(response))
    return response

def payload(text):
    return {"channel": "#seamless-thursday",
            "username": "OrderBot",
            "text": text,
            "icon_emoji": ":fatbot:",
            'link_names': 1}

def post_message(message):
    if message:
        return json.dumps(payload(message))
    return message
