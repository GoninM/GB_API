import requests
import json
# from requests_html import HTMLSession
from requests_html import HTMLSession


if __name__ == "__main__":
    url = f"https://dzen.ru/news/rubric/culture"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    print(response.text)

# тут я получаю не html страничку видимо, я некий скрипт,
# который видимо запускается браузером. и его я не могу спарсить.
# но интернет не оставил в беде и предложил решение. оно ниже
# pip install requests-html

    session = HTMLSession()
    r = session.get(url)
    r.html.render()


