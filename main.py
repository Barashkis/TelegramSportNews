from bs4 import BeautifulSoup
import requests


async def get_fresh_data(dp):
    state = dp.current_state()
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/95.0.4638.69 Safari/537.36"
    }
    fresh_news = {}

    data = await state.get_data()
    all_news_dict = data["news_data"]
    news_count = data["news_count"]

    url = "https://www.championat.com/tags/5-fk-zenit/news/"

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")
    all_news = soup.find_all("div", class_="news-item")

    for new in all_news[:news_count]:
        new_content = new.find("div", class_="news-item__content")

        href = "https://www.championat.com" + new_content.find_all("a")[0].get("href")
        slug = href.split("/")[-1].split(".")[0].split("-")[1]

        title = new_content.find_all("a")[0].text

        if slug in all_news_dict.keys():
            continue

        fresh_news[slug] = {
            "Заголовок": title,
            "Ссылка": href
        }

    return fresh_news


async def get_data(dp):
    state = dp.current_state()
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/95.0.4638.69 Safari/537.36"
    }

    all_news_dict = {}

    data = await state.get_data()
    news_count = data["news_count"]

    url = "https://www.championat.com/tags/5-fk-zenit/news/"

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")
    all_news = soup.find_all("div", class_="news-item")

    for new in all_news[:news_count]:
        new_content = new.find("div", class_="news-item__content")

        href = "https://www.championat.com" + new_content.find_all("a")[0].get("href")
        slug = href.split("/")[-1].split(".")[0].split("-")[1]

        title = new_content.find_all("a")[0].text

        all_news_dict[slug] = {
            "Заголовок": title,
            "Ссылка": href
        }

    await state.update_data({
        "news_data": all_news_dict
    })
