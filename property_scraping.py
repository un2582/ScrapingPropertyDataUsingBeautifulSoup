import requests
import pandas
from bs4 import BeautifulSoup

r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
soup = BeautifulSoup(c,"html.parser")
page_number = soup.find_all("a",{"class","Page"})[-1].text
l = []
base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,int(page_number) * 10,10):
    url = (base_url + str(page) +".html")
    r = requests.get(url,headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all("div",{"class","propertyRow"})
    for item in all:
        d = {}
        try:
            d["Address"]=(item.find_all("span",{"class","propAddressCollapse"})[0].text.replace("\n",""))
        except:
            d["Address"] = None
        try:
            d["Locality"]=(item.find_all("span",{"class","propAddressCollapse"})[1].text.replace("\n",""))
        except:
            d["Locality"] = None
        try:
            d["Price"]=(item.find("h4",{"class","propPrice"}).text.replace("\n","").replace(" ",""))
        except:
            d["Price"] = None
        try:
            d["Bed"] = (item.find("span",{"class","infoBed"}).find("b").text.replace("\n","").replace(" ",""))
        except:
            d["Bed"] = (None)

        try:
            d["Full Bath"] = (item.find("span",{"class","infoValueFullBath"}).find("b").text.replace("\n","").replace(" ",""))
        except:
            d["Full Bath"] =  None

        try:
            d["Square Feet"] = (item.find("span",{"class","infoSqFt"}).find("b").text.replace("\n","").replace(" ",""))
        except:
            d["Square Feet"] = (None)

        try:
            d["Half Bath"] = (item.find("span",{"class","infoValueHalfBath"}).find("b").text.replace("\n","").replace(" ",""))
        except:
            d["Half Bath"] = (None)
        d["Lot Size"] = None
        d["Appliances"] = None
        for columnGroup in item.find_all("div",{"class","columnGroup"}):
            feat = ""
            for featureGroup in columnGroup.find_all("span",{"class","featureGroup"}):
                if "Lot Size" in featureGroup.text:
                    for featureName in columnGroup.find_all("span",{"class","featureName"}):
                        feat = feat + featureName.text
                        d["Lot Size"] = (feat)


                if "Appliances" in featureGroup.text:
                    for featureName in columnGroup.find_all("span",{"class","featureName"}):
                        feat = feat + featureName.text
                        d["Appliances"] = (feat)


        l.append(d)

df = pandas.DataFrame(l)
df
df.to_csv(r"C:\Users\un258\Documents\Webscraping practice\output.csv")
