from django.urls import path
from . import views

# /products 
# /products/1/detail
# /products/new

urlpatterns = [
    path('', views.Home_Page, name= "homepage"),
    path('upload', views.Upload, name = "upload"),
    path('results', views.Results, name = "results"),
    path('insights', views.Insights, name= "insights")
]