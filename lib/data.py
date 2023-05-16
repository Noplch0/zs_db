import requests


def get_html(code, exchange):
    url = "https://www.google.com/finance/quote/" + code + ":%s" % exchange
    text = requests.get(url)
    return text
