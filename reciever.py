import pika, sys, os, json, psycopg2
login=False
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='user')

conn = psycopg2.connect(dbname="tienda",
                        user="postgres",
                        password="postgres",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

def main():
    def callback(ch, method, properties, body):
        global login
        contenido = str(body).strip('b\'')
        print(" [x] Received " + contenido)
        usuario = json.loads(str(contenido))
        if(not login): 
            correo = usuario['correo']
            pwd = usuario['pass']
            #print('usuario: ' + usuario['correo'])
            #print('pass: ' + usuario['pass'])
            cursor.execute('SELECT correo, pass FROM usuarios')
            results = cursor.fetchall()
            if((correo, pwd) in results):
                print("[x] LOGGED IN")
                cursor.execute(f'SELECT id, nombre FROM usuarios WHERE correo={correo}')
                user=cursor.fetchone()
                envia_usuario(*user)
                login = True
            else:
                print("[X] ERROR DE LOGIN")
                envia_error(1)
    def envia_error(codigo):
        mensaje = {'codigo': codigo}
        mensaje = json.dumps(mensaje)
        channel.basic_publish(exchange='', routing_key='user', body= mensaje)
        print(" [x] Sent error")
        #connection.close()

    def envia_usuario(id, nombre):
        #login=False
        #while(not login):
        
        mensaje = {'codigo': 0, 'usuario': {'id': id, 'nombre': nombre}}
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
