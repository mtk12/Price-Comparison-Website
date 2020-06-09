from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def ishopping(driver,query):
    st = time.time()
    driver.get("https://www.ishopping.pk/search/?q=" + query)
    time.sleep(3)
    title_links_img = driver.find_elements_by_class_name("klevuImgWrap")
    pricing = driver.find_elements_by_class_name("kuSalePrice")
    
    links = []
    title = []
    price = []
    images = []
    
    for elem in title_links_img:
        x = elem.find_element_by_tag_name('a')
        links.append(x.get_property('href'))
        x = elem.find_element_by_tag_name('img')
        title.append(x.get_property('alt'))
        images.append(x.get_property('src'))
        
    for element in pricing:
        pr = element.text
        pr = re.sub("[^0-9]",'', pr)
        price.append(int(pr))
    
    
        
    data = {}
    for i in range(0,len(title)):
        key = title[i]
        data.setdefault(key,[])
        data[key].append(price[i])
        data[key].append(links[i])
        data[key].append(images[i])
        data[key].append('https://d11zer3aoz69xt.cloudfront.net/skin/frontend/ishopping/default/images/logo.png')

    end = time.time() - st
    print(end)
    return data