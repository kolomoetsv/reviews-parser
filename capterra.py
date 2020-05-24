import requests
import json
import pandas as pd

df = pd.DataFrame()
url_const = 'https://www.capterra.com/spotlight/rest/reviews?apiVersion=2&productId='
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

competitors = {
    'semrush'  : '198433',
    'moz'      : '116352',
    'raven'    : '121696',
    'ahrefs'   : '176340',
    'serpstat' : '156369',
    'seranking': '142169',
}

#Getting 50 reviews
def get_reviews(url):
    response = requests.get(url, headers = headers)
    reviews = response.json()['hits']
    df_50 = pd.json_normalize(reviews, max_level=1)
    return(df_50)

for value in competitors.values():
    #Getting reviews' number and reviews from the first page
    url = url_const + value + '&from='
    count = requests.get(url, headers = headers).json()['totalHits']  
    df_50 = get_reviews(url)
    df = df.append(df_50, ignore_index=True)
    #Getting all reviews
    for i in range(50, count, 50):
        url = url_const + value + '&from=' + str(i)
        df_50 = get_reviews(url)
        df = df.append(df_50, ignore_index=True)
df.to_csv('file.csv', index=False)


