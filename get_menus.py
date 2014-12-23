from lxml import html
from lxml.cssselect import CSSSelector
import sys
import requests
import json


def getMenu(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    sel = CSSSelector('.menuItem [name="product"]')
    results = sel(tree)

    data = [r.get('title') for r in results]
    print data

urls = json.loads(open('restaurantURLs.txt').read())

with open('restaurants.txt') as f1:
    restaurants = dict((r.lower(), rest[0].lower()) for rest in json.load(f1) for r in rest)


rest = sys.argv[1]
if rest in restaurants:
    if restaurants[rest] in urls:
        getMenu(urls[restaurants[rest]])
    else:
        print "Sorry! Seamless is awful and doesn't expose the menu from %s to us!" % restaurants[rest]
else:
    print "Whoops! That's not a restaurant in our list! Here are the restaurants we have menus for:"


