from workers import task
from .models import Product
import smtplib
from bs4 import BeautifulSoup as soup
import requests
from django.contrib.auth.models import User

@task(schedule=30)
def background_scrapper():
    products = Product.objects.all()

    for product in products:
        my_url = product.url
        user_email = product.owner.email
        headers={
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/90.0.4430.212 Safari/537.36'
        }
        if "amazon" in my_url:

            page = requests.get(my_url,headers = headers)
            page_soup = soup(page.content,'html.parser')
            
            pc = ""
            if page_soup.find(id = "priceblock_dealprice") is not None and page_soup.find(id = "priceblock_ourprice") is not None:
                pc = page_soup.find(id = "priceblock_dealprice").get_text()     
            elif page_soup.find(id = "priceblock_dealprice") is not None:
                pc = page_soup.find(id = "priceblock_dealprice").get_text()
            elif page_soup.find(id = "priceblock_ourprice") is not None:
                pc  = page_soup.find(id = "priceblock_ourprice").get_text()
            
            record = Product.objects.get(url = my_url)

            if record.price != pc: 
                server = smtplib.SMTP_SSL("smtp.gmail.com",465)
                server.login("omkargadute@gmail.com","#")
                server.sendmail("omkargadute@gmail.com",user_email,"Price of your saved product is changed, please check.")   

                server.quit()

                record.price = pc
                record.save()
            else:
                print("No Change")
        if "flipkart" in my_url:
            page = requests.get(my_url,headers = headers)
            page_soup = soup(page.content,'html.parser')
            pc = page_soup.find(class_="_30jeq3 _16Jk6d").get_text()
            record = Product.objects.get(url = my_url)

            if record.price != pc: 
                server = smtplib.SMTP_SSL("smtp.gmail.com",465)
                server.login("omkargadute@gmail.com","#")
                server.sendmail("omkargadute@gmail.com",user_email,"Price of your saved product is changed, please check.")   

                server.quit()

                record.price = pc
                record.save()
            else:
                print("No Change")


background_scrapper()