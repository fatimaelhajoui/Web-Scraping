import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

page_num=0
url= 'https://www.avito.ma/fr/fes/ordinateurs_portables/dell--%C3%A0_vendre?o={page_num}' # enter the name of the website here I use avito as an exemple
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
           'Referer' : 'https://www.avito.ma/'
           }

while True:
   # use requests to ftch url 
   result = requests.get(url, headers=headers)
   #print(result)
   #print(result.reason)


   # use content to save the page content/markup
   source = result.content
   print(source)

   # create soup object to prase content
   soup = BeautifulSoup(source, "lxml")
   page_count=0
   page_limit= soup.find("h1",{"class":"sc-1x0vz2r-0 kofCMe sc-119b2hw-4 liBPCO"}).text
   number = [int(i) for i in page_limit.split() if i.isdigit()]
   for j in range(len(number)):
      page_count=number[j]

   if(page_num > page_count // 34):
      print("pages ended, terminate")
      break
   
   #infos: product name - company name - location - price - description

   #get the infos
   product_name = soup.find_all("p",{"class":"sc-1x0vz2r-0 czqClV"})
   company_name = soup.find_all("p",{"class":"sc-1x0vz2r-0 dNKvDA"})
   location = soup.find_all("div",{"class":"sc-b57yxx-9 jpbLku"})
   price = soup.find_all("p",{"class":"sc-1x0vz2r-0 eCXWei sc-b57yxx-3 IneBF"})
   links = soup.find_all("a",{"class":"sc-1jge648-0"})
   #print(price)

   #put the infos in a lists
   products_list =[]
   companies_list =[]
   locations_list =[]
   prices_list =[]
   links_list =[]
   descriptions_list =[]

   for i in range(len(product_name)):
      products_list.append(product_name[i].text)
      companies_list.append(company_name[i].text)
      locations_list.append(location[i].text)
      prices_list.append(price[i].text)
      links_list.append(links[i]["href"])
   #print(companies_list)
   page_num +=1
   print("page switched")
#loop on every products link and get the description
headers_links={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
           'Referer' : 'https://www.avito.ma/'
           }

for link in links_list:
   result=requests.get(link, headers=headers_links)
   source=result.content
   soup=BeautifulSoup(source, 'lxml')
   description=soup.find("p",{"class":"sc-ij98yj-0 fAYGMO"})
   # print(description.text)
   descriptions_list.append(description.text.strip())


#put infos in table csv

file_list=[products_list,companies_list,locations_list,prices_list,links_list,descriptions_list]
exported= zip_longest(*file_list)
with open("/Users/elhaj/OneDrive/Desktop/python/avito.csv", "w", encoding='utf-8') as myfile:
   write = csv.writer(myfile)
   write.writerow(["product name", "company name", "location", "price", "link", "description"])
   write.writerows(exported)



