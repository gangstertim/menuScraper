from flask import Flask, request
from flask_script import Manager
from lxml import html
from lxml.cssselect import CSSSelector
import requests, json, logging

app = Flask(__name__)
manager = Manager(app)

@app.route('/', methods=['POST'])
def getMenu():
    rest = request.form['text']
    app.logger.info('Request: {}'.format(request))
    urls = json.loads(open('restaurantURLs.txt').read())
    with open('restaurants.txt') as f1:
        restaurants = dict((r.lower(), rest[0].lower()) for rest in json.load(f1) for r in rest)

    if rest in restaurants:
        if restaurants[rest] in urls:
            response = scrapeMenu(urls[restaurants[rest]], restaurants[rest])
        else:
            response = "Sorry! I know how much you like %s, so I tried to get a menu from them, but Seamless is a bunch of ninnies and doesn't expose that menu to us!" % restaurants[rest]
    else:
        response = "Whoops! That's not a restaurant in our list! Here are the restaurants we have menus for:\n"
        for r in urls:
            response+=str(r)
            response+="\n"

    app.logger.info('GetMenu response: {}'.format(response))
    return response

def scrapeMenu(url, rest):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    sel = CSSSelector('.menuItem [name="product"]')
    results = sel(tree)

    data = [r.get('title') for r in results]
    
    response = "*%s*\n" % rest
    for d in data:
        response+=str(d) 
        response+="\n"
    
    response+="Or, check out the menu on Seamless here: %s" % url 
    return response 

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


