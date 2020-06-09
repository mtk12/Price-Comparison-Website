from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from webdriver_manager.chrome import ChromeDriverManager
from requests import get

#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)
#
#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
def daraz(driver,query):
    st = time.time()
    url = "https://www.daraz.pk/catalog/?q=" + query
    
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x = soup.prettify()
        
    names = re.findall(r'\"name":"(.+?)\"',x)
    pro_img_Url = re.findall(r'\"productUrl":"(.+?)\","image":"(.+?)\"',x)
    prices = re.findall(r'\"price":"(.+?)\"',x)
    
    title = []
    price = []
    link = []
    img = []
    
    for i in prices:
        v = float(i)
        price.append(int(v))
        
    for i in pro_img_Url:
        link.append(i[0])
        img.append(i[1])
        
    
    
    for i in names:
        t = i.split()
        if len(t)>1:
            title.append(i)
    
    if len(title) < len(price):
        data = {}
        for i in range(0,len(title)):
            key = title[i]
            data.setdefault(key,[])
            data[key].append(price[i])
            data[key].append(link[i])
            data[key].append(img[i])
            data[key].append('https://laz-img-cdn.alicdn.com/images/ims-web/TB1F29NfwZC2uNjSZFnXXaxZpXa.png')
    else:
        data = {}
        for i in range(0,len(price)):
            key = title[i]
            data.setdefault(key,[])
            data[key].append(price[i])
            data[key].append(link[i])
            data[key].append(img[i])
            data[key].append('https://laz-img-cdn.alicdn.com/images/ims-web/TB1F29NfwZC2uNjSZFnXXaxZpXa.png')
        
    end = time.time()
    t = end - st
    print(t)
    return data
