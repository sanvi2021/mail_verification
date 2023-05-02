import pika

# Define the connection parameters for RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Connect to RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

queue_name = 'TestQueue'

def read_from_queue():
    # Declare the queue if it doesn't exist
    channel.queue_declare(queue=queue_name)
    
    # Define a callback function to process incoming messages
    def callback(ch, method, properties, body):
        print(f"Received '{body.decode()}' from queue '{queue_name}'")
    
    # Start consuming messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


read_from_queue()