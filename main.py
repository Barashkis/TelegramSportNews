from bs4 import BeautifulSoup
import aiohttp
from fake_useragent import UserAgent


async def get_fresh_data(dp):
    state = dp.current_state()

    useragent = UserAgent()
    headers = {
        "Accept": "*/*",
        "User-Agent": useragent.random
    }

    fresh_news = {}

    data = await state.get_data()
    all_news_dict = data["news_data"]
    news_count = data["news_count"]

    url = "https://www.championat.com/tags/5-fk-zenit/news/"

    async with aiohttp.ClientSession() as session:
        req = await session.get(url, headers=headers)
        src = await req.text()

        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find_all("div", class_="news-item")

        for new in all_news[:news_count]:
            new_content = new.find("div", class_="news-item__content")

            href = new_content.find_all("a")[0].get("href")

            if "news" in href:
                href = "https://www.championat.com" + href
                slug = href.split("/")[-1].split(".")[0].split("-")[1]
            else:
                slug = href.split("/")[-1]

            title = new_content.find_all("a")[0].text

            if slug not in all_news_dict.keys():
                fresh_news[slug] = {
                    "Заголовок": title,
                    "Ссылка": href
                }

    return fresh_news


async def get_data(dp):
    state = dp.current_state()

    useragent = UserAgent()
    headers = {
        "Accept": "*/*",
        "User-Agent": useragent.random
    }

    all_news_dict = {}

    data = await state.get_data()
    news_count = data["news_count"]

    url = "https://www.championat.com/tags/5-fk-zenit/news/"

    async with aiohttp.ClientSession() as session:
        req = await session.get(url, headers=headers)
        src = await req.text()

        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find_all("div", class_="news-item")

        for new in all_news[:news_count]:
            new_content = new.find("div", class_="news-item__content")

            href = new_content.find_all("a")[0].get("href")

            if "news" in href:
                href = "https://www.championat.com" + href
                slug = href.split("/")[-1].split(".")[0].split("-")[1]
            else:
                slug = href.split("/")[-1]

            title = new_content.find_all("a")[0].text

            all_news_dict[slug] = {
                "Заголовок": title,
                "Ссылка": href
            }

        await state.update_data({
            "news_data": all_news_dict
        })
