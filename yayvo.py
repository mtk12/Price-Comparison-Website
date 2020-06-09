from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from webdriver_manager.chrome import ChromeDriverManager
from requests import get


#
#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)

def yayvo(driver,query):
    st =time.time()
    url = "https://yayvo.com/search/result/?q=" + query

    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')    
    
    title_links_img = soup.find_all('li',{'class',"item"})
    
    prices = soup.find_all('div',{'class',"price-box"})
    
    links = []
    title = []
    price = []
    images = []
            
    for elem in prices:
        try:
            pri = elem.find('span',{'class','regular-price'})
        except:
            pri = elem.find('p',{'class','special-price'})
            
        if pri == None:
            pri = elem.find('p',{'class','special-price'})
        pr = pri.text
        pr = re.sub("[^0-9]",'', pr)
        price.append(int(pr))
                
    for elem in title_links_img:
        links.append(elem.find('a')['href'])
        title.append(elem.find('a')['title'])
        images.append(elem.find('img')['data-src'])
        
    data = {}
    
    for i in range(0,len(title)):
        key = title[i]
        data.setdefault(key,[])
        data[key].append(price[i])
        data[key].append(links[i])
        data[key].append(images[i])
        data[key].append('http://yayvo.com/skin/frontend/default/yayvo_new/images/yayvo_logo.png')
    end = time.time() - st
    print(end)
    return data

#p = yayvo(driver,"ghee")
