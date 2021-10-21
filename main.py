import json
import requests
from bs4 import BeautifulSoup


def get_first_news():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
    }
    url = 'https://gordonua.com/news/science.html'

    articles = []

    try:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('div', class_='media')
    except Exception as e:
        print(e)

    news = {}
    for article in articles:
        try:
            article_title = article.find('div', class_='lenta_head').find('a').text.strip()
            article_date = article.find('div', class_='for_data').text.split('|')[0].strip()
            article_url = f'https://gordonua.com' + article.find('div', class_='lenta_head').find('a').get('href')
            article_id = article_url.split('-')[-1].split('.')[0]
            #print(f'{article_id}: \n{article_title} \n{article_url} \n{article_date}')
            news[article_id] = {
                'article_title': article_title,
                'article_url': article_url,
                'article_date': article_date
            }
        except Exception as e:
            print(e)

    with open('news.json', 'w', encoding='utf-8') as file:
        json.dump(news, file, indent=4, ensure_ascii=False)


def update_news():
    with open('news.json', 'r', encoding='utf-8') as file:
        news = json.load(file)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
    }
    url = 'https://gordonua.com/news/science.html'

    articles = []

    try:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('div', class_='media')
    except Exception as e:
        print(e)

    last_news = {}
    for article in articles:
        try:
            article_url = f'https://gordonua.com' + article.find('div', class_='lenta_head').find('a').get('href')
            article_id = article_url.split('-')[-1].split('.')[0]
            if article_id in news:
                continue
            else:
                try:
                    article_title = article.find('div', class_='lenta_head').find('a').text.strip()
                    article_date = article.find('div', class_='for_data').text.split('|')[0].strip()
                    #print(f'{article_id}: \n{article_title} \n{article_url} \n{article_date}')
                    news[article_id] = {
                        'article_title': article_title,
                        'article_url': article_url,
                        'article_date': article_date
                    }
                    last_news[article_id] = {
                        'article_title': article_title,
                        'article_url': article_url,
                        'article_date': article_date
                    }
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    with open('update_news.json', 'w', encoding='utf-8') as file:
        json.dump(last_news, file, indent=4, ensure_ascii=False)

    return last_news


def main():
    pass


if __name__ == '__main__':
    main()
