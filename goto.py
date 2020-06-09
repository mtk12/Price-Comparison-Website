from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
#option = webdriver.ChromeOptions()
#
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def goto(driver,query):
    st = time.time()
    driver.get("https://www.goto.com.pk/catalog-search/filter/q/" + query)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    title_links_img = soup.find_all('div',{'class',"product-image preloader"})
    pricing = soup.find_all('div',{'class',"price-box"})
    
    links = []
    title = []
    price = []
    images = []
    
    for elem in title_links_img:
        links.append(elem.find('a')['href'])
        title.append(elem.find('a')['title'])
        images.append(elem.find('img')['src'])
          
    for elem in pricing:
          x = elem.find('span',{'class','price'})
          pr = x.text
          pr = re.sub("[^0-9]",'', pr)
          price.append(int(pr))
          #price.append(pr)
          
    links = links[0:20]
    title = title[0:20]
    price = price[0:20]
    data = {}
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