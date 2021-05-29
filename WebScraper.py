import requests
from bs4 import BeautifulSoup
import pandas as pd 

baseurl = 'https://www.carpetvista.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'} #Avoid getting blocked as 'python' user

data = []
productLinks = []
c=0
types = ['nain-9-la', 'nain-6-la', 'tabriz-50-raj','tabriz-60-raj-silk-warp'] #Add type

for n in range(0, len(types)): #Selects each type of carpet's webpage
    for i in range(1,4): #Loop through the pages of items
        a = requests.get('https://www.carpetvista.com/carpets/all?group={type}&sort=random&page={index}&setCurrency=GBP'.format(type=types[n], index=i)).text
        soup = BeautifulSoup(a, 'html.parser')
        productList = soup.find_all ('div', {'class':'e-carpetBox'})
        
        for product in productList: #Find all the href links
            link = product.find('a', {'class':''}).get('href')
            productLinks.append(baseurl + link + '&setCurrency=GBP')


for link in productLinks: #Looping all the individual item webpages to 
    b = requests.get(link, headers=headers).text
    soup2 = BeautifulSoup(b, 'html.parser')

    try:
        name = soup2.find('h1', {'class':'pdp-headline'}).text.replace('\n','')
    except:
        name = None
    
    try:
        price = soup2.find('div', {'class':'p-price'}).text.replace('\n','').replace('"','')
    except:
        price = None
    
    try:
        size = soup2.find('div', {'class':'p-size'}).text.replace('\n','')
    except:
        size = None

    carpet = {'name':name,'price':price,'size':size}
    data.append(carpet)
    c=c+1
    print('Item ', c, ' complete')

df = pd.DataFrame(data)

df.to_csv('Data.csv')

print(df)