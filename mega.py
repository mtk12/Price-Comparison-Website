from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
#option = webdriver.ChromeOptions()
#option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def mega(driver,query):
    st = time.time()
    driver.get("http://www.mega.pk/search/" + query + "/")
    y = 200
    for timer in range(0,5):
         driver.execute_script("window.scrollTo(0, "+str(y)+")")
         y += 200 
         time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(1)
    title_links_img = soup.find_all('div',{'class',"wrapper1"})
    pricing = soup.find_all('div',{'class',"cat_price"})
    
    links = []
    title = []
    price = []
    images = []
    
    for elem in title_links_img:
        links.append(elem.find('a')['href'])
        title.append(elem.find('img')['alt'])
        images.append(elem.find('img')['src'])
        
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
        data[key].append('https://www.cartright.pk/StoreLogos/11/mega.pk.png')

    end = time.time() - st
    print(end)
    return data
