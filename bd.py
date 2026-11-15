import mysql.connector

def conectar_bd():
    host="localhost"
    usuario='root'
    contraseña=''
    database='viajes_jose'
    conexion=mysql.connector.connect(host=host,user=usuario,password=contraseña,database=database)
    return conexion
def obtener_viajes(conexion):
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            v.*,
            a.nombre AS acompañante,

            (
                SELECT GROUP_CONCAT(DISTINCT d.nombre SEPARATOR ', ')
                FROM viajes_destino vd
                JOIN destino d ON vd.id_destino = d.id
                WHERE vd.id_viaje = v.id_viaje
            ) AS destinos,

            (
                SELECT GROUP_CONCAT(DISTINCT c.nombre SEPARATOR ', ')
                FROM carga ca
                JOIN compradores c ON ca.id_comprador = c.id
                WHERE ca.id_viaje_destino IN (
                    SELECT vd.id
                    FROM viajes_destino vd
                    WHERE vd.id_viaje = v.id_viaje
                )
            ) AS compradores,

            (
                SELECT GROUP_CONCAT(
                    CONCAT(ca.kilogramos, ' kg de ', p.nombre)
                    SEPARATOR ', '
                )
                FROM carga ca
                JOIN pescados p ON ca.id_pescado = p.id
                WHERE ca.id_viaje_destino IN (
                    SELECT vd.id
                    FROM viajes_destino vd
                    WHERE vd.id_viaje = v.id_viaje
                )
            ) AS cargas

        FROM viajes v
        LEFT JOIN acompañantes a
            ON v.id_acompañante = a.id
    """

    cursor.execute(consulta)
    datos = cursor.fetchall()
    cursor.close()
    return datos
def obtener_destino(conexion):
    cursor=conexion.cursor(dictionary=True)
    consulta="SELECT id,nombre,kilometros FROM destino"
    cursor.execute(consulta)
    datos=cursor.fetchall()
    cursor.close()
    return datos

def buscar_destino_por_nombre(conexion, nombre):
    cursor = conexion.cursor(dictionary=True)

    consulta = "SELECT id,nombre,kilometros FROM destino WHERE LOWER(nombre) LIKE %s"
    parametro = (f"%{nombre.lower()}%",)

    cursor.execute(consulta, parametro)
    datos = cursor.fetchall()

    cursor.close()
    return datos

def crear_destino(conexion,nombre,km):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO destino(nombre,kilometros) VALUES (%s,%s)",(nombre,km))
    conexion.commit()
    id=cursor.lastrowid
    cursor.close()
    return id

#consultas de comprador
def obtener_compradores(conexion):
    cursor=conexion.cursor(dictionary=True)
    consulta="SELECT id,nombre FROM compradores"
    cursor.execute(consulta)
    datos=cursor.fetchall()
    cursor.close()
    return datos

def buscar_comprador_por_nombre(conexion, nombre):
    cursor = conexion.cursor(dictionary=True)

    consulta = "SELECT id,nombre FROM compradores WHERE LOWER(nombre) LIKE %s"
    parametro = (f"%{nombre.lower()}%",)

    cursor.execute(consulta, parametro)
    datos = cursor.fetchall()

    cursor.close()
    return datos

def crear_comprador(conexion,nombre):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO compradores(nombre) VALUES (%s)",(nombre,))
    conexion.commit()
    id=cursor.lastrowid
    cursor.close()
    return id



# CONSULTAS DE PESCADOS

def obtener_pescados(conexion):
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT id,nombre FROM pescados"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    cursor.close()
    return datos


def buscar_pescado_por_nombre(conexion, nombre):
    cursor = conexion.cursor(dictionary=True)

    consulta = "SELECT id,nombre FROM pescados WHERE LOWER(nombre) LIKE %s"
    parametro = (f"%{nombre.lower()}%",)

    cursor.execute(consulta, parametro)
    datos = cursor.fetchall()

    cursor.close()
    return datos


def crear_pescado(conexion, nombre):
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO pescados(nombre) VALUES (%s)",
        (nombre,)
    )

    conexion.commit()
    nuevo_id = cursor.lastrowid

    cursor.close()
    return nuevo_id

# CONSULTAS DE ACOMPAÑANTES

def obtener_acompañantes(conexion):
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT id,nombre FROM acompañantes"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    cursor.close()
    return datos


def buscar_acompañante_por_nombre(conexion, nombre):
    cursor = conexion.cursor(dictionary=True)

    consulta = "SELECT id,nombre FROM acompañantes WHERE LOWER(nombre) LIKE %s"
    parametro = (f"%{nombre.lower()}%",)

    cursor.execute(consulta, parametro)
    datos = cursor.fetchall()

    cursor.close()
    return datos


def crear_acompañante(conexion, nombre):
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO acompañantes(nombre) VALUES (%s)",
        (nombre,)
    )

    conexion.commit()
    nuevo_id = cursor.lastrowid

    cursor.close()
    return nuevo_id

def crear_viaje(conexion, fecha, km, bruto, gastos, id_acompañante=None):
    cursor = conexion.cursor()

    total = bruto - gastos

    consulta = """
        INSERT INTO viajes
        (fecha, km_hechos, dinero_bruto_total, gastos_viaje, total, id_acompañante)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(consulta, (fecha, km, bruto, gastos, total, id_acompañante))

    nuevo_id = cursor.lastrowid
    cursor.close()

    return nuevo_id


def crear_viaje_destino(conexion, id_viaje, id_destino):
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO viajes_destino (id_viaje, id_destino) VALUES (%s, %s)",
        (id_viaje, id_destino)
    )

    nuevo_id = cursor.lastrowid
    cursor.close()

    return nuevo_id


def crear_carga(conexion, kg, id_pescado, id_viaje_destino, id_comprador=None):
    cursor = conexion.cursor()
    cursor.execute(
        """INSERT INTO carga
           (kilogramos, id_pescado, id_viaje_destino, id_comprador)
           VALUES (%s, %s, %s, %s)""",
        (kg, id_pescado, id_viaje_destino, id_comprador)
    )
    cursor.close()