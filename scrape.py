from schedule import repeat, every, run_pending
import time
from bs4 import BeautifulSoup
import requests

@repeat(every(4).seconds, n=2)
def get_top5_hackernews_articles(n:int) -> list[dict]:


    url = 'https://news.ycombinator.com/'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.select('.titleline > a')
    scores = soup.select('.score')


    data = []
    for link, score in zip(links, scores):
        article_name = link.text
        article_url = link.attrs['href']
        article_score = score.text
        data.append({
            "url": article_url,
            "name": article_name,
            "score": int(article_score.split()[0])
        })

    top_N = sorted(data, key=lambda x: x['score'], reverse=True)[:n]
    print(top_N)
    requests.get('https://uptime.betterstack.com/api/v1/heartbeat/vC5MXne2HnSgM8FRrntw2zWB')
    return top_N

# schedule.every().day.at('09:17').do(get_top5_hackernews_articles)

while True:
    run_pending()
    time.sleep(1)