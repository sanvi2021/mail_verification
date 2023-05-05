import time
from threading import Thread
import requests



class CustomThread(Thread):
    def __init__(self,email):
        self.email = email
        
        Thread.__init__(self)
        self.result = None

    def run(self):
        print(self.email,'inside the run')
        endpoint_url = 'http://178.18.240.183:8080/logix/'+self.email
        try:
            response = requests.get(endpoint_url)
            self.result = response.json()
            print(self.result,'result')
            return self.result
        except Exception as e:
            print(e)


emails = ['nishant.kumar164@gmail.com','nishant.kumar0322@gmail.com']
res = []
for email in emails:
    thread = CustomThread(email)
    thread.start()
    thread.join()
    reply = thread.result
    res.append(reply)

print(res,'at last')