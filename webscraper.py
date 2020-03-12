import urllib.request

from bs4 import BeautifulSoup


def is_ingredient(tag):
    return tag.name == "span" and tag.has_attr('itemprop') and tag['itemprop'] == "recipeIngredient"


def is_direction(tag):
    return tag.name == "span" and tag.has_attr('class') and "recipe-directions__list--item" in tag['class']


def is_title(tag):
    return tag.name == "h1" and tag.has_attr('class') and "recipe-summary__h1" in tag['class']  and tag.has_attr('itemprop') and tag['itemprop'] == "name"


def parse_recipe(url):
    request_url = urllib.request.urlopen(url)
    web_html = str(request_url.read())
    soup = BeautifulSoup(web_html, 'html.parser')
    ingredients = [span.contents[0] for span in soup.find_all(is_ingredient)]
    soup = BeautifulSoup(web_html, 'html.parser')
    directions = [span.contents[0].strip()[:-2] if len(span.contents) > 0 else '' for span in soup.find_all(is_direction)]
    while '' in directions:
        directions.remove('')
    name = soup.find_all(is_title)[0].contents[0].strip()
    return {'ingredients': ingredients, 'directions': directions, 'name': name}
