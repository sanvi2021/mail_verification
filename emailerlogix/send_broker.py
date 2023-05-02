import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='TestQueue')
channel.basic_publish(exchange='',
                      routing_key='EmailVerification',
                      body="hello world 676s")
connection.close()