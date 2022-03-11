from dataclasses import replace
from genericpath import exists
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
import requests
import pandas as pd
from sqlalchemy import asc
print('Please enter a currency name')
currency_name=input()
currency_name=str(currency_name)
currency_name=currency_name.lower()
currency_name=re.sub('[*,. ]','-',currency_name)
r=requests.get('https://coinmarketcap.com/')
htmlCode=BeautifulSoup(r.content,'html5lib')

all_url=htmlCode.find_all('a',{'href':re.compile('/currencies/'+currency_name)})#currency_name url'ini bulur.
all_url=[url['href'] for url in all_url]
myUrl=all_url[0]
myUrl=myUrl.replace('/currencies/','').replace('/','')
print(myUrl)

    


headers = {
    'authority': 'api.coinmarketcap.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://coinmarketcap.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://coinmarketcap.com/',
    'accept-language': 'tr-TR,tr;q=0.9',
}

params = (
    ('slug', str(myUrl)),
    ('start', '1'),
    ('limit', '100'),
    ('category', 'spot'),
    ('sort', 'cmc_rank_advanced'),
)

response = requests.get(f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={str(myUrl)}&start=1&limit=100&category=spot&sort=cmc_rank_advanced', headers=headers)
results_json=response.json()
markets=results_json['data']['marketPairs']
all_data=[]

for market in markets:
   market_data= {'marketName':market['exchangeName'],
                'marketPair':market['marketPair'],
                'Price':market['price'],
    
                }
   all_data.append(market_data)
            
#print(all_data)            
df=pd.json_normalize(all_data)
df=df.sort_values('Price',ascending=False)
df.to_csv(f'{currency_name}.csv')

top_price=df.head(1)['Price'].values
bottom_price=df.tail(1)['Price'].values
differenceOfPrices=df.head(1)['Price'].values-df.tail(1)['Price'].values
meanPrices=df.mean()['Price']
inferences={'top_price':str(top_price[0]),
'bottom_price':str(bottom_price[0]),
'differenceOfPrices':str(differenceOfPrices[0]),
'meanPrices':str(meanPrices)
}
inferences=str(inferences)
print(inferences)
with open(f'{myUrl}.txt','w') as myTxt:
    myTxt.write(inferences)
#print([value for value in df['Price'].values if value>df.mean()['Price']])

