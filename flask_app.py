from MySQLdb import Connect, connect

from flask import Flask, redirect

from flask import render_template

from flask import jsonify

from flask import request

from flask_mysqldb import MySQL  #3

from flask import url_for

import pymysql

import mysql.connector


app = Flask(__name__, template_folder=r'D:\CURSOS\flask proyectos\app-pedidos\templates', static_url_path='/static')

#nos conectamos a sql

db = pymysql.connect(host='localhost', user='root', password='', database='atn')
cursor = db.cursor()

#------------------------------------------- RUTAS ----------------------------------------------#

@app.route('/')
def pag_principal():
    return render_template('index.html')

@app.route('/opciones')
def op():
    return render_template('clientes/opciones_clientes.html')

@app.route('/opciones-gastos')
def op_gasto():
    return render_template('gastos/opciones_gastos.html')

@app.route('/opciones-ingresos')
def op_ingreso():
    return render_template('ingresos/opciones_ingresos.html')

@app.route('/opciones-pedidos')
def op_pedidos():
    return render_template('pedidos/opciones_pedidos.html')

#------------------------------------- AGREGAR CLIENTE ---------------------------------------------------
@app.route('/form')
def mostrar_formulario():
    return render_template('clientes/formulario.html')

@app.route('/agregar-cliente', methods=['POST'])
def agregar_cliente():
    direccion = request.form['direccion']
    telefono = request.form['telefono']

    # Insertar datos en la base de datos
    query = "INSERT INTO clientes (direccion, telefono) VALUES (%s, %s)"
    cursor.execute(query, (direccion, telefono))
    db.commit()

    return 'Cliente agregado correctamente'


#------------------------------------- MODIFICAR CLIENTES ---------------------------------------------------
@app.route('/formulario_modificacion')
def mostrar_formulario_modificacion():
    # Obtener la lista de clientes desde la base de datos
    query = "SELECT id_cliente, direccion, telefono FROM clientes"
    cursor.execute(query)
    clientes = cursor.fetchall()

    return render_template('clientes/formulario_modificacion.html', clientes=clientes)


@app.route('/modificar_cliente', methods=['POST'])
def modificar_cliente():
    
    id_cliente = request.form['id_cliente']
    nueva_direccion = request.form['direccion']
    nuevo_telefono = request.form['telefono']

    # Actualizar datos en la base de datos
    query = "UPDATE clientes SET direccion=%s, telefono=%s WHERE id_cliente=%s"
    cursor.execute(query, (nueva_direccion, nuevo_telefono, id_cliente))
    db.commit()

    return 'Cliente modificado correctamente'


#------------------------------------- VER CLIENTES ---------------------------------------------------
@app.route('/customers') #2
def get_all_customers():                      
    query = "select id_cliente, direccion, telefono from clientes"    #7  #obtener info de todos los clientes
    cursor.execute(query)
    data = cursor.fetchall()                     #8
    
    resultado = []                            #9  
    for fila in data:                         #10
        contenido = { 
                     "id_cliente": fila[0], 
                     "telefono": fila[1], 
                     "direccion": fila[2] 
                     }  #11
        resultado.append (contenido)                     
    
    return render_template('clientes/ver_clientes.html', resultado = resultado)



#------------------------------------- ELIMINAR CLIENTE ---------------------------------------------------
@app.route('/formulario_eliminacion')
def mostrar_for_eli():
    # Obtener la lista de clientes desde la base de datos
    query = "SELECT * FROM clientes"
    cursor.execute(query)
    clientes = cursor.fetchall()

    return render_template('clientes/eliminar.html', clientes=clientes)



@app.route('/delete', methods = ['POST'])
def remove_customer():                        
    id_cliente = request.form['id_cliente']
    
    query_eliminar_pedidos = "DELETE FROM pedidos WHERE id_cliente = %s"
    cursor.execute(query_eliminar_pedidos, (id_cliente,))
    db.commit()
    
    query = ("delete from clientes where id_cliente = %s")  #5
    cursor.execute(query, (id_cliente))
    db.commit() #6
    return "eliminado correctamente"


#------------------------------------- AGREGAR GASTOS ---------------------------------------------------
@app.route('/form-gasto')
def form_gasto():
    return render_template('gastos/form_agregar_gasto.html')


@app.route('/agregar-gasto', methods = ['POST'])
def agregar_gasto():
    gasto = request.form['gasto']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']

    # Insertar datos en la base de datos
    query = "INSERT INTO gastos (gasto, descripcion, fecha) VALUES (%s, %s, %s)"
    cursor.execute(query, (gasto, descripcion, fecha))
    db.commit()

    return 'Gasto agregado correctamente'


#------------------------------------- VER GASTOS ---------------------------------------------------
@app.route('/ver-gastos')
def ver_gastos():                     
    query = "select id_gasto, gasto, descripcion, fecha from gastos"    
    cursor.execute(query)
    data = cursor.fetchall()                    
    total = 0
    resultado = []  
                               
    for fila in data:                         
        contenido = { 
                     "id_gasto": fila[0], 
                     "gasto": fila[1], 
                     "descripcion": fila[2],
                     "fecha": fila[3] 
                    } 
        total += fila[1]
        resultado.append (contenido)                     
    
    return render_template('gastos/ver_gastos.html', resultado = resultado, total=total)


#------------------------------------- ELIMINAR GASTOS ---------------------------------------------------
@app.route('/form-elimi_gasto')
def mostrar_for_eli_g():
    # Obtener la lista de gastos desde la base de datos
    query = "SELECT id_gasto, gasto, descripcion FROM gastos"
    cursor.execute(query)
    info = cursor.fetchall()

    return render_template('gastos/eliminar_gasto.html', info=info)



@app.route('/delete-gasto', methods = ['POST'])
def remove_gasto():                       
    id_gasto = request.form['id_gasto']
    
    query = ("delete from gastos where id_gasto = %s")  #5
    cursor.execute(query, (id_gasto))
    db.commit() #6
    return "eliminado correctamente"


#------------------------------------- AGREGAR INGRESOS  ---------------------------------------------------
@app.route('/form-ingre')
def form_ingre():
    return render_template('ingresos/form_agregar_ingre.html')


@app.route('/agregar-ingre', methods = ['POST'])
def agregar_ingre():
    ingreso = request.form['ingreso']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']

    # Insertar datos en la base de datos
    query = "INSERT INTO ingresos (ingreso, descripcion, fecha) VALUES (%s, %s, %s)"
    cursor.execute(query, (ingreso, descripcion, fecha))
    db.commit()

    return 'Ingreso agregado correctamente'


#------------------------------------- ELIMINAR INGRESOS  ---------------------------------------------------
@app.route('/form-elimi-ingre')
def mostrar_for_eli_ingre():
    # Obtener la lista de gastos desde la base de datos
    query = "SELECT id_ingreso, ingreso, descripcion FROM ingresos"
    cursor.execute(query)
    info = cursor.fetchall()

    return render_template('ingresos/eliminar_ingreso.html', info=info)


@app.route('/delete-ingre', methods = ['POST'])
def remove_ingreso():                       
    id_ingreso = request.form['id_ingreso']
    
    query = ("delete from ingresos where id_ingreso = %s")  #5
    cursor.execute(query, (id_ingreso))
    db.commit() #6
    return "eliminado correctamente"


#----------------------------------------- VER INGRESOS  ---------------------------------------------------
@app.route('/ver-ingresos')
def ver_ingresos():                     
    query = "select id_ingreso, ingreso, descripcion, fecha from ingresos"    
    cursor.execute(query)
    data = cursor.fetchall()                    
    total = 0
    resultado = []  
                               
    for fila in data:                         
        contenido = { 
                     "id_ingreso": fila[0], 
                     "ingreso": fila[1], 
                     "descripcion": fila[2],
                     "fecha": fila[3] 
                    } 
        total += fila[1]
        resultado.append (contenido)                     
    
    return render_template('ingresos/ver_ingresos.html', resultado = resultado, total=total)


#-----------------------------------------  BALANCE ----------------------------------------------------------
@app.route('/balance')
def balance():
    query = "select id_ingreso, ingreso, descripcion, fecha from ingresos"    
    cursor.execute(query)
    data = cursor.fetchall()                    
    total = 0
                               
    for fila in data:                         
        contenido = { 
                     "id_ingreso": fila[0], 
                     "ingreso": fila[1], 
                     "descripcion": fila[2],
                     "fecha": fila[3] 
                    } 
        total += fila[1]
        
    query = "select id_gasto, gasto, descripcion, fecha from gastos"    
    cursor.execute(query)
    data = cursor.fetchall()                    
    total1 = 0
    resultado = []  
                               
    for fila in data:                         
        contenido = { 
                     "id_gasto": fila[0], 
                     "gasto": fila[1], 
                     "descripcion": fila[2],
                     "fecha": fila[3] 
                    } 
        total1 += fila[1]
    
    
    return render_template('balance/balance.html', total=total, total1=total1)


#------------------------------------------ AGREGAR PEDIDOS  --------------------------------------------------- 
@app.route('/form-agregar-pedido', methods=['GET'])
def agregar_pedidos():
    query = "select id_cliente, direccion, telefono from clientes"    #7  #obtener info de todos los clientes
    cursor.execute(query)
    data = cursor.fetchall()                     #8
    
    resultado = []                            #9  
    for fila in data:                         #10
        contenido = { 
                     "id_cliente": fila[0], 
                     "telefono": fila[1], 
                     "direccion": fila[2] 
                     }  #11
        resultado.append (contenido)       

    return render_template('pedidos/agregar_pedido.html', lista_de_clientes=resultado)

@app.route('/agregar-pedido', methods=['POST'])
def agregar_pedidos_en_serio():
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    id_cliente = request.form.get('cliente')
    importe = request.form['importe']

    # Insertar datos en la base de datos
    query = "INSERT INTO pedidos (descripcion, fecha, id_cliente, importe) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (descripcion, fecha, id_cliente, importe))
    db.commit()
    return 'Pedido agregado correctamente'

#------------------------------------------ VER PEDIDOS  ---------------------------------------------------
@app.route('/ver-pedidos', methods=['GET'])
def ver_pedidos():
    return render_template('pedidos/ver_pedidos.html')

@app.route('/ver-pedidos', methods=['POST'])
def ver_pedidos_por_fecha():
    fecha = request.form.get('fecha')

    # Consulta para obtener los pedidos de una fecha específica
    query = "SELECT * FROM pedidos WHERE fecha = %s"
    cursor.execute(query, (fecha))
    data = cursor.fetchall()                     #8
    
    resultado = []                            #9 
    resultado_dire = []     
    for fila in data:          
       
        id_cliente = fila[3]
        # Consulta para obtener la dirección del cliente
        query_cliente = "SELECT direccion FROM clientes WHERE id_cliente = %s"
        cursor.execute(query_cliente, (id_cliente))
        direccion_cliente = cursor.fetchone()[0]  # Obtén la dirección del primer resultado
        
        contenido = { 
                     "id_pedido": fila[0], 
                     "descripcion": fila[1], 
                     "fecha": fila[2],
                     "id_cliente": fila[3],
                     "importe": fila[4],
                     "direccion_cliente": direccion_cliente 
                     }  #11
        resultado.append (contenido)
        
    #total de ingreso de pedidos
    query_total_pedidos = "select * from pedidos"    
    cursor.execute(query_total_pedidos)
    datas = cursor.fetchall()                    
    total_ingre_pedidos = 0 
                               
    for fila in datas:                         
        contenido = { 
                     "id_pedido": fila[0], 
                     "descripcion": fila[1], 
                     "fecha": fila[2],
                     "id_cliente": fila[3],
                     "importe": fila[4],
                     "direccion_cliente": direccion_cliente 
                     }
        total_ingre_pedidos += fila[4]

    return render_template('pedidos/ver_pedidos.html', pedidos=resultado, fecha_seleccionada=fecha, total_ingre_pedidos = total_ingre_pedidos)


#------------------------------------------ ELIMINAR PEDIDOS  ---------------------------------------------------
@app.route('/form-elimi-pedido')
def mostrar_for_eli_pedi():
    query = "SELECT * FROM pedidos"
    cursor.execute(query)
    informacion = cursor.fetchall()

    return render_template('pedidos/eliminar_pedido.html', informacion=informacion)


@app.route('/delete-pedido', methods = ['POST'])
def remove_pedido():                       
    id_pedido = request.form['id_pedido']
    
    query = ("delete from pedidos where id_pedido = %s")  #5
    cursor.execute(query, (id_pedido))
    db.commit() #6
    return "eliminado correctamente"


if __name__ == '__main__':
    app.run(debug=True)