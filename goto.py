from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from requests import get

#option = webdriver.ChromeOptions()
#
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def goto(driver,query):
    st = time.time()
    url = "https://www.goto.com.pk/catalog-search/filter/q/" + query

    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_links_img = soup.find_all('div',{'class',"product-image"})
    
    prices = soup.find_all('span',{'class',"regular-price"})
    
    links = []
    title = []
    price = []
    images = []
            
    for elem in prices:
        pr = elem.text
        pr = re.sub("[^0-9]",'', pr)
        price.append(int(pr))
                
    for elem in title_links_img:
        links.append(elem.find('a')['href'])
        title.append(elem.find('img')['alt'])
        images.append(elem.find('img')['data-src'])
        
    data = {}
    if len(price) < len(title):
        for i in range(0,len(price)):
            key = title[i]
            data.setdefault(key,[])
            data[key].append(price[i])
            data[key].append(links[i])
            data[key].append(images[i])
            data[key].append('https://cdn.goto.com.pk/uploads/logo/logo.png')
    else:
        for i in range(0,len(title)):
            key = title[i]
            data.setdefault(key,[])
            data[key].append(price[i])
            data[key].append(links[i])
            data[key].append(images[i])
            data[key].append('https://cdn.goto.com.pk/uploads/logo/logo.png')
    end = time.time() - st
    print(end)
    return data