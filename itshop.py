from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
#option = webdriver.ChromeOptions()
#
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)


def itshop(driver,query):
    st = time.time()
    driver.get("https://www.itshop.pk/search.php?search_query=" + query + "&x=0&y=0")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    title_links = soup.find_all('div',{'class',"ProductDetails"})
    pricing = soup.find_all('span',{'class',"ProductPrice"})
    img = soup.find_all('div',{'class',"ProductImage"})
    
    links = []
    title = []
    price = []
    images = []
    
    for elem in title_links:
        x = elem.find('strong')
        links.append(x.find('a')['href'])
        title.append(x.text)
    
    for elemm in img:
        images.append(elemm.find('img')['src'])
        
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
        data[key].append('https://www.itshop.pk/product_images/logo.png')
    end = time.time() - st
    print(end)
    return data
