import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1:8080'))
channel = connection.channel()

def publish_go(method,body):
    properties = pika.BasicProperties(method)
    channel.queue_declare(queue='TestQueue')
    channel.basic_publish(exchange='',
                        routing_key='EmailVerification',
                        body=body,
                        properties=properties)
    connection.close()