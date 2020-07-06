from selenium import webdriver
import time
from bs4 import BeautifulSoup
from requests import get
import re

#
#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def hummart(query):
    st = time.time()
    url = "https://hummart.com/catalogsearch/result/?q=" + query

#    titles = driver.find_elements_by_class_name("result-title")
#    links = driver.find_elements_by_class_name("result-content")
#    pricing = driver.find_elements_by_class_name("price-wrapper-inner")
#    images = driver.find_elements_by_class_name("result-thumbnail")
    
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title_links_img = soup.find_all('div',{'class',"product-item-photo"})
    prices = soup.find_all('span',{'class',"price"})
    links = []
    title = []
    price = []
    images = []
        
    for elem in prices:
        pr = elem.text
        pr = re.sub("[^0-9]",'', pr)
        price.append(int(pr))
        
    price = list(set(price))
    
    for elem in title_links_img:
            links.append(elem.find('a')['href'])
            title.append(elem.find('img')['alt'])
            images.append(elem.find('img')['src'])
    
    title = list(set(title))
    
    if len(title) > len(price):
        data = {}
        for i in range(0,len(price)):
            key = title[i]
            data.setdefault(key,[])
            data[key].append(price[i])
            data[key].append(links[i])
            data[key].append(images[i])
            data[key].append('https://hummart.com/media/logo/websites/1/Hum_Mart_Logo_final_low_size.png')
    else:
        data = {}
        for i in range(0,len(title)):
            key = title[i]
            data.setdefault(key,[])
            data[key].append(price[i])
            data[key].append(links[i])
            data[key].append(images[i])
            data[key].append('https://hummart.com/media/logo/websites/1/Hum_Mart_Logo_final_low_size.png')
            
    end = time.time() - st
    print(end)
    return data