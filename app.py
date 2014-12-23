import json, logging
from flask import Flask, request
from flask_script import Manager
import get_menus as menu

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()

@app.route('/', methods=['POST'])
def index():
    post = request.form['text']
    app.logger.info('Raw: {}'.format(request.form['text']))
    getmenu_response = menu.getMenu(post)
    app.logger.info('GetMenu response: {}'.format(getmenu_response))
    response = post_message(getmenu_response)
    return response

def payload(text):
    return {"username": "MenuBot",
            "text": text,
            "icon_emoji": ":fatbot:",
            'link_names': 1}

def post_message(message):
    if message:
        return json.dumps(payload(message))
    return message
