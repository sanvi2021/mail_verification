from django.shortcuts import render
from .serializer import CSVUploadSerializer, SinglefieldSerializer
import csv
import pandas as pd
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from pathlib import Path
from django.core.files.storage import default_storage
from rest_framework import status
import time
import requests
import pprint
import pika
from .models import *


class CSVUploadView(APIView):
    serializer_class = CSVUploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = request.FILES['csv_file']
            file_name = default_storage.save(file.name, file)
            print("file saved in default storage-----")
            data = pd.read_csv(file_name)
            return Response({'message': data.columns},status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileProcessing(APIView):
    def get(self, request):
        column_name = request.data["email_field"]
        file_name = request.data["file_name"]
        start = time.time()
        file = default_storage.open(file_name)
        for chunk in pd.read_csv(file,chunksize=1000, usecols= [column_name]):
            print(chunk)
            
        return Response({"total execution time:", time.time()-start},status= status.HTTP_200_OK)

class SingleFileProcessing(APIView):
    serializer_class = SinglefieldSerializer
    def post(self,request):    
        serializer = self.serializer_class(data = request.data)       
        if serializer.is_valid():
            print(type(request.data["email"]))
            result = SingleFile(request.data["email"])
            account_balance = request.balance
            
            return Response({"message":result, "account_balance":account_balance}, status= status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

def SingleFile(email):
    try:
        url = "http://127.0.0.1:8080/logix/"
        new_url = url+email
        result = requests.get(url = new_url)
        pprint.pprint(result.json())        
        SingleEmaillist.objects.create(data= result.json())
        return (result.json())
    except Exception as e:
        return e

