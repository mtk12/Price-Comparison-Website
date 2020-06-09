from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from requests import get

#option = webdriver.ChromeOptions()
#option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def mega(query):
    st = time.time()
    url = "http://www.mega.pk/search/" + query + "/"

    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_links_img = soup.find_all('div',{'class',"wrapper1"})
    pricing = soup.find_all('div',{'class',"cat_price"})
    
    links = []
    title = []
    price = []
    images = []
    
    for elem in title_links_img:
        links.append(elem.find('a')['href'])
        title.append(elem.find('img')['alt'])
        images.append(elem.find('img')['data-original'])
        
    for element in pricing:
        pr = element.text
        pr = pr.split()[0]
        pr = re.sub("[^0-9]",'', pr)
        if pr!='':
            price.append(int(pr))
        else:
            price.append(0)
        
    
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
