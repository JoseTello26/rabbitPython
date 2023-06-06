import pika, json
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2', port=5672, virtual_host='/', credentials=credentials, blocked_connection_timeout=60))
channel = connection.channel()
channel.queue_declare(queue='user')

if __name__ == '__main__':
    correo = input("Ingrese correo: ")
    password = input("Contraseña: ")
    usuario = {'correo': correo, 'pass': password}

    usuario = json.dumps(usuario)

    channel.basic_publish(exchange='', routing_key='user', body= usuario)
    print(" [x] Sent")
    connection.close()
