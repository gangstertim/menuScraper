from lxml import html
from lxml.cssselect import CSSSelector
import sys
import requests

class GetMenu():
    page = requests.get('http://www.seamless.com/food-delivery/al-zaytouna-philadelphia.19600.r')
    tree = html.fromstring(page.text)

    sel = CSSSelector('.menuItem [name="product"]')
    results = sel(tree)

    data = [r.get('title') for r in results]

    print data


