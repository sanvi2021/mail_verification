from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import dns.resolver
from freeapi.serializer import *
from rest_framework import status

# Create your views here.

class DomainRecord(APIView):
    DomainRecord_class = DomainRecordSerializer
    def post(self,request):
        serializer = self.DomainRecord_class(data=request.data)
        if serializer.is_valid():
            ids = ['MX','A','AAAA','CNAME','TXT','SPF']
            domain = str(request.data['domain_name'])
            data ={}
            data["MX"] = []
            data["A"] = []
            data["AAAA"] = []
            data["CNAME"] = []
            data["TXT"] = []
            data["SPF"] = []
            for a in ids:
                try:
                    answers = dns.resolver.query(domain, a)
                    for rdata in answers:
                        print(a, ':', str(rdata))
                        if a == "MX":
                            data["MX"].append(str(rdata))
                        if a == "A":
                            data["A"].append(str(rdata))
                        if a == "AAAA":
                            data["AAAA"].append(str(rdata))
                        if a == "CNAME":
                            data["CNAME"].append(str(rdata))
                        if a == "TXT":
                            data["TXT"].append(str(rdata))
                        if a == "SPF":
                            data["SPF"].append(str(rdata))
                except Exception as e:
                    print(e)
               
            return Response({"data": data})
        else:
            return Response({"message":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    
