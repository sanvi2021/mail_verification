from django.shortcuts import render
from .serializer import CSVUploadSerializer, SinglefieldSerializer, DomainRecordSerializer
import csv
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from pathlib import Path
from django.core.files.storage import default_storage
from rest_framework import status
import time
from .models import *
from .sender import *
from .consumer import *
import dns.resolver

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
        counter = 0
        
        for chunk in pd.read_csv(file,chunksize=10, usecols= [column_name]):
            publish_bulk(chunk.to_json())        
            counter +=1
            print(counter,"---------chunk here------")
            resp = consume_email()
            print("chunks processed", counter)
          
        return Response({"total execution time":time.time()-start, "message": resp},status= status.HTTP_200_OK)

class SingleFileProcessing(APIView):
    serializer_class = SinglefieldSerializer
    def post(self,request):    
        serializer = self.serializer_class(data = request.data)       
        if serializer.is_valid():
            print(type(request.data["email"]))
            publish_go(request.data["email"])
            result = consume_single_email()
            account_balance = request.balance
            verified_email = SingleEmaillist.objects.create(data=result)
            updated_account = Account_Balance.objects.update(initial_balance=account_balance)
            return Response({"message":result, "account_balance":account_balance}, status= status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

