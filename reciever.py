import pika, sys, os, json, psycopg2
login=False
connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['RABBITMQ_HOST'], port=os.environ['RABBITMQ_PORT']))
channel = connection.channel()

channel.queue_declare(queue='js-python')
channel.queue_declare(queue='python-js')

conn = psycopg2.connect(dbname="tienda",
                        user=os.environ['POSTGRES_USER'],
                        password=os.environ['POSTGRES_PASSWORD'],
                        host=os.environ['POSTGRES_HOST'],
                        port=os.environ['POSTGRES_PORT'])
cursor = conn.cursor()

def main():
    def callback(ch, method, properties, body):
        global login
        contenido = str(body).strip('b\'')
        print(" [x] Received " + contenido)
        usuario = json.loads(str(contenido))
        if(not login): 
            if usuario["type"]=='login':
                correo = usuario['email']
                pwd = usuario['pass']
                #print('usuario: ' + usuario['email'])
                #print('pass: ' + usuario['pass'])
                cursor.execute('SELECT correo, pass FROM usuarios')
                results = cursor.fetchall()
                if((correo, pwd) in results):
                    print("[x] LOGGED IN")
                    cursor.execute(f"SELECT id, nombre FROM usuarios WHERE correo = '{correo}' ")
                    user=cursor.fetchone()
                    envia_usuario(*user)
                    login = True
                else:
                    print("[X] ERROR DE LOGIN")
                    envia_error(1)
            elif usuario["type"]=='signup':
                correo = usuario['email']
                pwd = usuario['pass']
                nombre = usuario['email']
                cursor.execute('SELECT correo, pass FROM usuarios')
                results = cursor.fetchall()
                if((correo, pwd) in results):
                    print("[X] ERROR DE REGISTRO")
                    envia_error(1)
                else:
                    cursor.execute(f"INSERT INTO usuarios (nombre,correo, pass) VALUES ('{nombre}', '{correo}', '{pwd}')")
                    conn.commit()
                    print("[x] REGISTRADO USUARIO")
                    cursor.execute(f"SELECT id, nombre FROM usuarios WHERE correo = '{correo}' ")
                    user=cursor.fetchone()
                    print(user)
                    envia_usuario(*user)
                    login = True
        else:
            if('codigo' in usuario.keys()):
                if(usuario['codigo']==9):
                    print("[X] USUARIO CERRO LOGIN "+user[1])
                    login=False 
            else:
                for prod in usuario['productos']:
                    cursor.execute(f"INSERT INTO ventas (id_usuario, id_producto, cantidad, precio) VALUES ({usuario['usuario_ID']},{prod['ID']}, {prod['cantidad']}, {prod['precio']})")
                print("[X] COMPRA REGISTRADA")
                envia_actualizacion_bd(usuario['productos'])


    def envia_error(codigo):
        mensaje = {'codigo': codigo}
        mensaje = json.dumps(mensaje)
        channel.basic_publish(exchange='', routing_key='python-js', body= mensaje)
        print(" [x] Sent error")
        #connection.close()

    def envia_usuario(id, nombre):
        #login=False
        #while(not login):
        
        mensaje = {'codigo': 0, 'usuario': {'id': id, 'nombre': nombre}}
        mensaje = json.dumps(mensaje)
        channel.basic_publish(exchange='', routing_key='python-js', body= mensaje)
        
        #channel.basic_publish(exchange='', routing_key='query', body= "lol")
        print(" [x] Sent user ID")
        #connection.close()   
    def envia_actualizacion_bd(productos):
        actualizacion = {'productos': productos}
        actualizacion = json.dumps(actualizacion)
        channel.basic_publish(exchange='', routing_key='python-java', body= actualizacion)
        print(" [x] Sent update to product DB")


    channel.basic_consume(queue='js-python', on_message_callback=callback, auto_ack=True)

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

