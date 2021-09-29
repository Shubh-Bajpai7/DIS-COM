from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup as soup
from django.shortcuts import render,HttpResponse
import requests
import datetime
import json
import time
current_time = datetime.datetime.now()
import os
from pathlib import Path
from .models import Product

headers={
    "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/90.0.4430.212 Safari/537.36'
    }

def mainPage(request):
    return render(request,'products/mainpage.html')

@login_required
def home(request):
    products = Product.objects.filter(owner=request.user)
    context = {'products':products}
    return render(request,'products/checklist.html', context)

def scrapper(request):
    if request.method == "POST":
        link = request.POST['Search']
        if "amazon" in link:
            #my_url = "https://www.amazon.in/Lenovo-Windows-Graphics-Phantom-82AU00KEIN/dp/B08JLR75BD/ref=sr_1_1?crid=184T7B1RYM91H&dchild=1&keywords=lenovo+legion+5&qid=1621256742&sprefix=leno%2Caps%2C513&sr=8-1"    
            page = requests.get(link,headers = headers)
            page_soup = soup(page.content,'html.parser')
            
            title = page_soup.find(id="productTitle").get_text()

            price = ""
            if page_soup.find(id = "priceblock_dealprice") is not None and page_soup.find(id = "priceblock_ourprice") is not None:
                price = page_soup.find(id = "priceblock_dealprice").get_text()     
            elif page_soup.find(id = "priceblock_dealprice") is not None:
                price = page_soup.find(id = "priceblock_dealprice").get_text()
            elif page_soup.find(id = "priceblock_ourprice") is not None:
                price = page_soup.find(id = "priceblock_ourprice").get_text()

            rating = "No Information on Rating" 
            if page_soup.find(class_="a-icon-alt") is not None:
                rating = page_soup.find(class_="a-icon-alt").get_text().strip()
            
            ratings = "No Information on Ratings" 
            if page_soup.find(id="acrCustomerReviewText") is not None:
                ratings = page_soup.find(id="acrCustomerReviewText").get_text().strip()
            availability  = ""
            if page_soup.find(id="availability")is not None:
                availability = page_soup.find(id="availability").get_text().strip()
            else:
                availability = "No Information on Availability"
            url = link
            dataPhone = {
                'NAME':title.strip(),
                'PRICE':price.strip(),
                'RATING':rating.strip(),
                'RATINGS':ratings.strip(),
                'AVAILABILITY':availability.strip(),
                'URL':url.strip(),
            }
            with open('amazon.json','w') as json_file:
                json.dump(dataPhone,json_file)

            user = request.user
            BASE_DIR = Path(__file__).resolve().parent.parent
            FILE_PATH = os.path.join(BASE_DIR,'amazon.json')
            jsonFile = open(FILE_PATH)
            data = json.load(jsonFile)
            Product.objects.create(
                name = data['NAME'],
                price = data['PRICE'],
                rating = data['RATING'],
                availability = data['AVAILABILITY'],
                url = data['URL'],
                site = "Amazon",
                owner = user
            )
        if "flipkart" in link:
            #my_url = 'https://www.flipkart.com/asian-coscos-sports-shoes-running-shoes-walking-shoes-training-shoes-running-shoes-men/p/itmfe37fzu48vnye?pid=SHOF78HRHXTDFGGJ&lid=LSTSHOF78HRHXTDFGGJMQBFHM&marketplace=FLIPKART&srno=b_1_4&otracker=hp_omu_Deals%2Bof%2Bthe%2BDay_3_3.dealCard.OMU_V9I2VX1CA508_2&otracker1=hp_omu_SECTIONED_neo%2Fmerchandising_Deals%2Bof%2Bthe%2BDay_NA_dealCard_cc_3_NA_view-all_2&fm=neo%2Fmerchandising&iid=a711d5f7-02dd-40e0-bf60-6291ef961095.SHOF78HRHXTDFGGJ.SEARCH&ppt=browse&ppn=browse&ssid=mklz3vlxog0000001603514448562'
            page = requests.get(link,headers = headers)
            page_soup = soup(page.content,'html.parser')
            title = page_soup.find(class_="B_NuCI").get_text()
            price = page_soup.find(class_="_30jeq3 _16Jk6d").get_text()
            rating = page_soup.find(class_="_3LWZlK").get_text()
            #ratings = page_soup.find(class_="_38sUEc").get_text()
            ratings = "1000"
            url = link
            
            dataPhone = {
                'NAME':title.strip(),
                'PRICE':price.strip(),
                'RATING':rating.strip(),
                'RATINGS':ratings.strip(), 
                'URL':url.strip(), 
            }
            with open('flipkart.json','w') as json_file:
                json.dump(dataPhone,json_file)

            user = request.user
            BASE_DIR = Path(__file__).resolve().parent.parent
            FILE_PATH = os.path.join(BASE_DIR,'flipkart.json')
            jsonFile = open(FILE_PATH)
            data = json.load(jsonFile)
            Product.objects.create(
                name = data['NAME'],
                price = data['PRICE'],
                rating = data['RATING'],
                url = data['URL'],
                site = "Flipkart",
                owner = user
            )

    return redirect('products:mainpage')

def delete(request,pk):
    product = Product.objects.filter(pk=pk)
    product.delete()
    return redirect('products:myproducts')


