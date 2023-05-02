from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponse
from . models import Account_Balance


class AccountMiddleware:
    def  __init__(self,get_response):
        self.get_response = get_response
         # logic to check if user is logged, then fetch the account details from db
        
        initial_balance = Account_Balance.objects.filter(id =1).values()
        balance = initial_balance[0].get('initial_balance')
        self.balance = balance

    def __call__(self,request):
        print("before call")
        # logic to check if user is logged, then fetch the account details from db
        self.balance-=1        
        request.balance = self.balance
        if request.balance <0:
                return HttpResponse('Insufficient balance', status=400)
        else:
             self.balance-1
        response = self.get_response(request)
        print("after call")
        return response
