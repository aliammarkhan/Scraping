from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

#path to chrome driver path
chrome_driver_path = "C:\Development\chromedriver.exe"
#form link where i will save my data and get a csv file
form_link = "https://docs.google.com/forms/d/e/1FAIpQLSdrKpoJDo6snf_vU3sdD5M_nsGTU0pvhxSQitnjtDBotiddEQ/viewform"
#Zameen.com link for Rental homes in North Nazimabad
zameen_link = "https://www.zameen.com/Rentals/Karachi_North_Nazimabad-11-1.html"
#headers that are sent by the browser with each request
header = {
    'Request Line' : 'GET / HTTP/1.1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Accept-Language':'en-US,en;q=0.9',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate',
    'X-Http-Proto':'HTTP/1.1',
    'X-Real-Ip':'51.15.192.242',
    }
#get the html
response  = requests.get(url = zameen_link,headers = header).text
#make soup
soup = BeautifulSoup(response,"html.parser")

#class names of html tags we will use to scrap
address_class = "_162e6469"
info_class ="c0df3811"
price_class = "f343d9ce"
link_class = "_7ac32433"

address = []
info = []
prices = []
link = []

for i,class_ in enumerate([address_class,info_class,price_class,link_class]):
    tags = soup.find_all(class_ = class_)
    for tag in tags:
        if i == 0: 
            address.append(tag.getText())
        elif i == 1:
            info.append(tag.getText())
        elif i == 2:
             prices.append("PKR " + tag.getText())
        else:
            if tag.get("href") !=None:
                link.append("https://www.zameen.com"+tag.get("href"))


#intialize selenium object
driver = webdriver.Chrome(chrome_driver_path)
driver.get(form_link)

#get the input tags      


time.sleep(1)

for a,p,i,l in zip(address,prices,info,link):
   
    inputs = driver.find_elements_by_class_name("exportInput")
    
    inputs[0].send_keys(a)
    inputs[1].send_keys(p)
    inputs[2].send_keys(i)
    inputs[3].send_keys(l)

    #click the submit button
    submit = driver.find_element_by_class_name("exportButtonContent")
    submit.click()
    
    #click submit other responses button
    another = driver.find_element_by_css_selector(".freebirdFormviewerViewResponseLinksContainer a")
    another.click()
    #wait for one second
    time.sleep(2)
#quit the browser
driver.quit()

