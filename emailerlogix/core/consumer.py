import pika
import requests
import json
from threading import Thread

def consume_single_email():
    # Define a callback function to handle incoming messages
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue to consume from
    channel.queue_declare(queue='single_email')
    result = []
    def callback(ch, method, properties, body):
        print("Received message: %r" % body)
    # acknowledge the receipt of the message
        # ch.basic_ack(delivery_tag=method.delivery_tag)
        email_id = body.decode('utf-8')
        print(email_id,'--------------------------------')
        endpoint_url = f'http://178.18.240.183:8080/logix/{email_id}'
        response = requests.get(endpoint_url)
        result.append(response.json())
        connection.close() 
    # Start consuming messages from the queue
    try:
        channel.basic_consume(queue='single_email', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        return result
    except Exception as e:
        return e


def consume_email():
    # Define a callback function to handle incoming messages
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare the queue to consume from
    channel.queue_declare(queue='bulk_email')
    print("inside consumer ---herh---------")
    result = []
    def callback(ch, method, properties, body):
        # trying for worker code 
        print(" [x] Received %r" % body.decode())

        # code ends
        dict = json.loads(body)
        email_id = list(dict.values())
        chunksize = 2
        emails = email_id[0:10]
        emails2 = email_id[11:21]
        print(emails,'==========================',len(emails))
        # emails2 = email_id[51:]
        res1 = []
        for email in emails:
            thread = CustomThread(email)
            thread.start()
            thread.join()
            reply = thread.result
            res1.append(reply)   
        connection.close()   
        return result.append(res1)

    # Start consuming messages from the queue
    try:
        channel.basic_consume(queue='bulk_email', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        return result
    except Exception as e:
        return e
    
class CustomThread(Thread):
    def __init__(self,email):
        self.email = email
        self.result = None
        Thread.__init__(self)
        
    
    def run(self):
        endpoint_url = 'http://178.18.240.183:8080/logix/'+self.email
        try:
            response = requests.get(endpoint_url)
            self.result = response.json()
            return self.result
        except Exception as e:
            print(e)
