
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('file_upload/',CSVUploadView.as_view(), name= "upload_file"),
    path('file_process/',FileProcessing.as_view(), name= "file_process"),
    path('email_process/', SingleFileProcessing.as_view(), name = "email_process")   

]
