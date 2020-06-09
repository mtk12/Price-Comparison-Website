from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def rocket(driver,query):
    st = time.time()
    driver.get("https://rocket.pk/catalogsearch/result/?q=" + query)
    y = 200
    for timer in range(0,5):
         driver.execute_script("window.scrollTo(0, "+str(y)+")")
         y += 200 
         time.sleep(1)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title_img = soup.find_all('span',{'class',"product-image-wrapper"})
    link = soup.find_all('strong',{'class',"product-item-name"})
    pricing = soup.find_all('span',{'class',"price"})
    
    
    links = []
    title = []
    price = []
    images = []
    
    a = 1
    for elem in title_img:
        if(a%2 == 0):
            title.append(elem.find('img')['alt'])
            images.append(elem.find('img')['src'])
        a += 1
    
    for elem in link:
        links.append(elem.find('a')['href'])
        
    for element in pricing:
        pr = element.text
        pr = re.sub("[^0-9]",'', pr)
        price.append(int(pr))
    
    if len(price) > 2:
        price.pop()
        price.pop(0)
        
    title = title[0:20]
    links = links[0:20]
    price = price[0:20]
    images = images[0:20]
    
    data = {}
    for i in range(0,len(title)):
        key = title[i]
        data.setdefault(key,[])
        data[key].append(price[i])
        data[key].append(links[i])
        data[key].append(images[i])
        data[key].append('https://rocket.pk/pub/media/logo/stores/1/logo-Final.jpeg')

    end = time.time() - st
    print(end)
    return data
