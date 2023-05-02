import pika

# Define the connection parameters for RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Connect to RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Define the name of the queue to use
queue_name = 'my_queue'

def send_to_queue(data):
    # Declare the queue if it doesn't exist
    channel.queue_declare(queue=queue_name)
    
    # Publish the data to the queue
    channel.basic_publish(exchange='', routing_key=queue_name, body=data)
    
    print(f"Sent '{data}' to queue '{queue_name}'")

def read_from_queue():
    # Declare the queue if it doesn't exist
    channel.queue_declare(queue=queue_name)
    
    # Define a callback function to process incoming messages
    def callback(ch, method, properties, body):
        print(f"Received '{body.decode()}' from queue '{queue_name}'")
    
    # Start consuming messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Example usage
send_to_queue('Hello, world!')
read_from_queue()
