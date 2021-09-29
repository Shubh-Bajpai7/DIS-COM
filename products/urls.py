from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',views.mainPage,name = 'mainpage'),
    path('myproducts/',views.home, name = 'myproducts'),
    path('scapper/',views.scrapper, name = 'scrapper'),
    path('delete/<int:pk>/',views.delete, name = 'delete'),
]
