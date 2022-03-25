import json
from bs4 import BeautifulSoup
import requests


def get_data():
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/95.0.4638.69 Safari/537.36"
    }
    fresh_news = {}

    with open("news.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    url = "https://www.championat.com/tags/5-fk-zenit/news/"

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")
    all_news = soup.find_all("div", class_="news-item")

    for new in all_news[:10]:
        new_content = new.find("div", class_="news-item__content")

        href = "https://www.championat.com" + new_content.find_all("a")[0].get("href")
        slug = href.split("/")[-1].split(".")[0].split("-")[1]

        if slug in news_dict.keys():
            continue

        title = new_content.find_all("a")[0].text

        src_time = requests.get(href, headers=headers).text
        soup_time = BeautifulSoup(src_time, "lxml")

        full_time = soup_time.find("time", class_="article-head__date").text

        news_dict[slug] = {
            "Заголовок": title,
            "Ссылка": href,
            "Дата публикации": full_time
        }

        fresh_news[slug] = {
            "Заголовок": title,
            "Ссылка": href,
            "Дата публикации": full_time
        }

        if len(news_dict) == 11:
            del news_dict[min(news_dict.keys())]

    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news
