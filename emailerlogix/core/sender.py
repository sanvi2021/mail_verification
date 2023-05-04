import pika

def publish_go(email):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='single_email') 
    channel.basic_publish(exchange='', routing_key='single_email', body=email)
    connection.close()


def publish_bulk(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='bulk_email') 
    channel.basic_publish(exchange='', routing_key='bulk_email', body=data)
    connection.close()
