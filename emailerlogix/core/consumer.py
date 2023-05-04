import pika
import requests
import json

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
        email_id = body.decode()
        endpoint_url = f'http://127.0.0.1:8080/logix/{email_id}'
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
    result = []
    def callback(ch, method, properties, body):
        dict = json.loads(body)
        email_id = dict.get('email')
        b = [c for c in email_id.values()]
        for i in b:
            endpoint_url = 'http://178.18.240.183:8080/logix/'+i
            try:

                response = requests.get(endpoint_url)
                result.append(response.json())
            except Exception as e:
                print(e)

        connection.close()
            
        return result

    # Start consuming messages from the queue
    try:
        channel.basic_consume(queue='bulk_email', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        return result
    except Exception as e:
        return e

def consume_email_2():
    # Define a callback function to handle incoming messages
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare the queue to consume from
    channel.queue_declare(queue='bulk_email')
    result = []
    def callback(ch, method, properties, body):
        dict = json.loads(body)
        email_id = dict.get('email')
        b = [c for c in email_id.values()]
        for i in b:
            endpoint_url = 'http://178.18.240.183:8081/logix/'+i
            try:

                response = requests.get(endpoint_url)
                result.append(response.json())
            except Exception as e:
                print(e)

        connection.close()
            
        return result

    # Start consuming messages from the queue
    try:
        channel.basic_consume(queue='bulk_email', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        return result
    except Exception as e:
        return e


def result_publish(processed_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='processed_email') 
    channel.basic_publish(exchange='', routing_key='processed_email', body=processed_data)
    connection.close()
