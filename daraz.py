from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

#option = webdriver.ChromeOptions()
##option.add_argument('headless')
#driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe',options=option)

def getURL(title,driver):
    driver.get("https://www.google.com/search?q=" + title + "&tbm=isch&ved=2ahUKEwiltfnniqzoAhVH-RQKHWu-A3gQ2-cCegQIABAA&oq=mobile&gs_l=img.3..0l10.93027.93833..94091...0.0..0.245.1165.0j5j1......0....1..gws-wiz-img.......35i39j0i67j0i131.DkxtywiuK4Y&ei=0k12XqWEM8fyU-v8jsAH&bih=648&biw=1366")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    x = soup.find('div', {'class': 'bRMDJf islir'})
    return (x.find('img')['src'])

def daraz(driver,query):
    st = time.time()
    driver.get("https://www.daraz.pk/catalog/?q=" + query + "&_keyori=ss&from=input&spm=a2a0e.searchlistcategory.search.go.520348d9CdM2Wk")
    y = 100
    for timer in range(0,3):
         driver.execute_script("window.scrollTo(0, "+str(y)+")")
         y += 100 
         time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title_links = soup.find_all('div', {'class': 'c16H9d'})
    pricing = soup.find_all('span', {'class': 'c13VH6'})
    img = soup.find_all('div', {'class': 'cRjKsc'})


    links = []
    title = []
    price = []
    images = []
    
    for p in pricing:
        pr = p.text
        pr = re.sub("[^0-9]",'', pr)
        price.append(int(pr))
    
    for title_link in title_links:
        links.append(title_link.find('a')['href'])
        title.append(title_link.find('a')['title'])
    
    a = 0
    for im in img:
        try:
            images.append(im.find('img')['src'])
        except:
            images.append(getURL(title[a],driver))
        a = a + 1
        if a == 20:
            break
#    links = links[]
#    title = title[]
#    price = price[]
    print(title)
    data = {}
    for i in range(0,20):
        key = title[i]
        data.setdefault(key,[])
        data[key].append(price[i])
        data[key].append(links[i])
        data[key].append(images[i])
        data[key].append('https://laz-img-cdn.alicdn.com/images/ims-web/TB1F29NfwZC2uNjSZFnXXaxZpXa.png')
    
    end = time.time()
    t = end - st
    print(t)
    return data
