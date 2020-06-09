from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from requests import get

#option = webdriver.ChromeOptions()
#option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def symbios(query):
    st = time.time()
    url = "https://www.symbios.pk/search.php?search_query=" + query
    
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title_links_img = soup.find_all('div',{'class',"product-image"})
    pricing = soup.find_all('span',{'class',"price"})
    
    links = []
    title = []
    price = []
    images = []
    for elem in title_links_img:
        links.append(elem.find('a')['href'])
        title.append(elem.find('img')['title'])
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
        data[key].append('https://www.symbios.pk/assets/symbios-logo.png')
    end = time.time() - st
    print(end)
    return data
