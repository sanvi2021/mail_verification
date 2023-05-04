
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('domain_record/', DomainRecord.as_view(), name = "DomainRecord"),  

]
