from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from webdriver_manager.chrome import ChromeDriverManager

#
#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)

def yayvo(driver,query):
    st =time.time()
    driver.get("https://yayvo.com/search/result/?q=" + query)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    title_links_img = soup.find_all('li',{'class',"item"})
    pricing = soup.find_all('div',{'class',"price-box"})
    
    links = []
    title = []
    price = []
    images = []
    
    for elem in title_links_img:
        links.append(elem.find('a')['href'])
        title.append(elem.find('a')['title'])
        images.append(elem.find('img')['src'])
        
    for element in pricing:
        x = element.find('p',{'class','special-price'})
        if isinstance(x, type(None)): 
            a = element.find('span',{'class','regular-price'})
            y = a.find('span',{'class','price'})
            pr = y.text
            pr = re.sub("[^0-9]",'', pr)
            price.append(int(pr))
            #price.append(y.text)
        else:
            y = x.find('span',{'class','price'})
            pr = y.text
            pr = re.sub("[^0-9]",'', pr)
            price.append(int(pr))
            #price.append(y.text)
            
    links = links[0:10]
    title = title[0:10]
    price = price[0:10]
    images = images[0:10]
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
