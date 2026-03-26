from django.urls import path
from . import views

# /products 
# /products/1/detail
# /products/new

urlpatterns = [
    path('', views.Home_Page, name= "homepage"),
    path('recommend', views.Recommend, name = "recommend"),
    path('insights', views.Insights, name= "insights")
]