import time
import requests

from bs4 import BeautifulSoup

from components.problem.models import Problem, Topic
from settings import proj_conf


def receive_clear_data(soup: BeautifulSoup):
    tds = soup.find_all("td", class_="id")
    ids = [''] * len(tds)
    urls = [''] * len(tds)
    topics = [[] for i in range(len(tds))]

    for i in range(len(tds)):
        ids[i] = tds[i].text.strip()
        new_soup = BeautifulSoup(str(tds[i]), "lxml")
        urls[i] = proj_conf.parsing_source + new_soup.find("a", href=True)["href"]

    names = [div.text.strip() for div in soup.find_all("div", attrs={"style": "float: left;"})]

    topics_divs = soup.find_all(
        "div",
        attrs={"style": "float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;"}
    )

    for i in range(len(topics_divs)):
        items = topics_divs[i].text.split('\r')

        for item in items:
            item = item.strip() if not item.strip() or item.strip()[-1] != ',' else item.strip()[0:-1]
            topics[i].append(item.lower())

    complexity = [
        int(span.text.strip()) if span.text.strip() else None for span in soup.find_all("span", class_="ProblemRating")
    ]

    count_decided = [int(td.text.strip()[1:]) if td.text.strip() else 0 for td in soup.find_all("td", attrs={"style": "font-size: 1.1rem;"})]

    return ids, names, urls, topics, complexity, count_decided


def parsing_pages(page: str):
    soup = BeautifulSoup(page, "lxml")
    number_pages = int(soup.find_all("span", class_="page-index")[-1].text)

    ids, names, urls, topics, complexities, count_decided = receive_clear_data(soup=soup)
    Problem.create_batch(
        names=names,
        numbers=ids,
        complexities=complexities,
        count_decided=count_decided,
        urls=urls,
        topics=topics,
        length_batch=len(ids)
    )

    for num in range(2, number_pages+1):
        codeforces_url = f'/page/{num}?'.join(proj_conf.codeforce_url.split('?'))
        req = requests.get(url=codeforces_url)

        while req.status_code != 200:
            time.sleep(0.5)
            req = requests.get(url=proj_conf.codeforce_url)

        soup = BeautifulSoup(req.text, "lxml")
        ids, names, urls, topics, complexity, count_decided = receive_clear_data(soup=soup)

        Problem.create_batch(
            names=names,
            numbers=ids,
            complexities=complexities,
            count_decided=count_decided,
            urls=urls,
            topics=topics,
            length_batch=len(ids)
        )

