import pika, sys, os, json
login=False
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='user')

def main():
    def callback(ch, method, properties, body):
        global login
        contenido = str(body).strip('b\'')
        print(" [x] Received " + contenido)
        usuario = json.loads(str(contenido))
        if(not login): 
            print('usuario: ' + usuario['correo'])
            print('pass: ' + usuario['pass'])
            if(usuario['correo'] != "asdasd@uni.pe" and usuario["pass"]!="asdads123"):
                print("[X] ERROR DE LOGIN")
                envia_error(1)
            else:
                print("[x] LOGGED IN")
                envia_usuario("ID01")
                login = True
    def envia_error(codigo):
        mensaje = {'codigo': codigo}
        mensaje = json.dumps(mensaje)
        channel.basic_publish(exchange='', routing_key='user', body= mensaje)
        print(" [x] Sent error")
        #connection.close()

    def envia_usuario(id):
        #login=False
        #while(not login):
        
        mensaje = {'codigo': 0, 'usuario': id}
        mensaje = json.dumps(mensaje)
        channel.basic_publish(exchange='', routing_key='user', body= mensaje)
        
        #channel.basic_publish(exchange='', routing_key='query', body= "lol")
        print(" [x] Sent user ID")
        #connection.close()   


    channel.basic_consume(queue='user', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
