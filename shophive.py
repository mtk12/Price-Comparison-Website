from selenium import webdriver
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


option = webdriver.ChromeOptions()
#option.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)

def shophive(driver,query):
    st = time.time()
    driver.get("https://www.shophive.com/catalogsearch/result/?cat=0&q=" + query)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    title_links_img = soup.find_all('div',{'class',"product-block-inner"})
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
        price.append(element.text)
    
    data = {}
    for i in range(0,len(title)):
        key = title[i]
        data.setdefault(key,[])
        data[key].append(price[i])
        data[key].append(links[i])
        data[key].append(images[i])
        data[key].append('https://www.shophive.com/skin/frontend/default/MAG090172/images/logo3.png')

    end = time.time() - st
    print(end)
    return data