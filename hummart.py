from selenium import webdriver
import time
from bs4 import BeautifulSoup
#
#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def hummart(driver,query):
    st = time.time()
    driver.get("https://hummart.com/catalogsearch/result/?q=" + query)

    titles = driver.find_elements_by_class_name("result-title")
    links = driver.find_elements_by_class_name("result-content")
    pricing = driver.find_elements_by_class_name("price-wrapper-inner")
    images = driver.find_elements_by_class_name("result-thumbnail")
    
    link = []
    title = []
    price = []
    image = []
    
    for elem in titles:
        title.append(elem.text)
          
    for elem in links:
          x = elem.find_element_by_tag_name('a')
          link.append(x.get_property('href'))
    
    for elem in images:
          x = elem.find_element_by_tag_name('img')
          image.append(x.get_property('src'))
          
    for elem in pricing:
        x = elem.find_element_by_class_name('after_special')
        price.append(elem.text)
    
    y = filter(lambda x: x != "", price)
    price = list(y)
    
    data = {}
    for i in range(0,len(title)):
        key = title[i]
        data.setdefault(key,[])
        data[key].append(price[i])
        data[key].append(link[i])
        data[key].append(image[i])
        data[key].append('https://hummart.com/media/logo/websites/1/Hum_Mart_Logo_final_low_size.png')
    end = time.time() - st
    print(end)
    return data