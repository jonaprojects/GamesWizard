# IMPORTS
from bs4 import BeautifulSoup
import requests
from time import gmtime
from time import strftime
from datetime import date, datetime
import math

weather_keywords = ["weather", 'temperature', 'sunny', 'rain', 'rainy', 'cloud', 'hot', 'cold']


def get_content(url):
    return requests.get(url).text


def extract_weather():
    url = r"https://www.google.com/search?q=weather&rlz=1C1EJFA_enIL798IL813&oq=weather+&aqs=chrome..69i57j0j0i131i433j0l2.1799j0j7&sourceid=chrome&ie=UTF-8"
    html_content = get_content(url)
    soup = BeautifulSoup(html_content, features="lxml")
    # print(soup.prettify())
    tags = soup.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})[1]
    span_tag = tags.findChild("span", recursive=False)
    return span_tag.text


def clean_string(string: str):
    return string.strip().lower()


def analyze_request(request):
    request = clean_string(request)
    words = list(request.split(" "))
    accumulator = ""
    if words[0] == 'wiki':
        print(fr"https://en.wikipedia.org/wiki/{'_'.join(words[1:]).strip().capitalize()}")
        wiki_page = get_content(fr"https://en.wikipedia.org/wiki/{'_'.join(words[1:]).strip().capitalize()}")
        soup = BeautifulSoup(wiki_page, features="lxml")
        body = soup.findChild("body")
        main_div = body.findChild("div", {"class": "mw-body"})
        text_div = main_div.find("div", {"class": "mw-content-ltr"})
        blacklist = [
            'style',
            'script',
            # other elements,
        ]
        text_elements = [t for t in text_div.find_all(text=True) if t.parent.name not in blacklist]
        lines = " ".join(text_elements)
        text_elements = lines.splitlines()
        text_elements = text_elements[:int(len(text_elements) / 2)]
        lines = "\n".join(text_elements)
        accumulator += lines
    elif words[0].startswith("calc"):
        expression = " ".join(words[1:])
        expression = expression.replace(" ", "")
        try:
            accumulator += f"{eval(expression)}\n"
        except Exception as e:
            print(f"{e.__class__}. \n Invalid Expression {expression}")
    for word in words:
        if word in weather_keywords and "temperature" not in accumulator:
            accumulator += f'The temperature is {extract_weather()}\n'
        if word == "day":
            pass
        elif word == "time":
            accumulator += datetime.now().strftime("%H:%M:%S") + "\n"

        elif word == "date":
            accumulator += date.today().strftime("%d/%m/%y") + "\n"

    return accumulator


def main():
    running = True
    while running:
        request = input("What do you want to know  ?  ")
        print(analyze_request(request))


if __name__ == "__main__":
    main()
