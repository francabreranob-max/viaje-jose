from bd import conectar_bd,obtener_viajes,obtener_destino,buscar_destino_por_nombre,crear_destino,buscar_comprador_por_nombre,obtener_compradores,crear_comprador
from bd import obtener_pescados, buscar_pescado_por_nombre, crear_pescado
from bd import obtener_acompañantes, buscar_acompañante_por_nombre, crear_acompañante
from bd import crear_viaje, crear_viaje_destino, crear_carga
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#para iniciar el programa: uvicorn main:app --reload
#Uvicorn running on http://127.0.0.1:8000


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/viajes")
def listar_viajes():
    conexion=conectar_bd()
    datos=obtener_viajes(conexion)
    conexion.close()
    return datos

@app.get("/destino")
def destinos():
    conexion=conectar_bd()
    datos=obtener_destino(conexion)
    conexion.close()
    return datos

@app.post("/destino")
def guardar_destino(datos: dict):
    nombre = datos["nombre"].strip()
    kilometros = datos["kilometros"]

    conexion = conectar_bd()
    existe = buscar_destino_por_nombre(conexion, nombre)

    if existe:
        conexion.close()
        return existe

    nuevo_id = crear_destino(conexion, nombre, kilometros)
    conexion.close()

    return {
        "id": nuevo_id,
        "nombre": nombre,
        "kilometros": kilometros
    }

@app.get("/comprador")
def compradores():
    conexion=conectar_bd()
    datos=obtener_compradores(conexion)
    conexion.close()
    return datos


@app.post("/comprador")
def guardar_comprador(datos: dict):
    nombre = datos["nombre"].strip()

    conexion = conectar_bd()
    existe = buscar_comprador_por_nombre(conexion,nombre)

    if existe:
        conexion.close()
        return existe

    nuevo_id = crear_comprador(conexion,nombre)
    conexion.close()

    return {
        "id": nuevo_id,
        "nombre": nombre
    }


#conexion con pescados

@app.get("/pescado")
def pescados():
    conexion = conectar_bd()
    datos = obtener_pescados(conexion)
    conexion.close()
    return datos


@app.get("/pescado/buscar")
def buscar_pescados(nombre: str):
    conexion = conectar_bd()
    datos = buscar_pescado_por_nombre(conexion, nombre)
    conexion.close()
    return datos


@app.post("/pescado")
def guardar_pescado(datos: dict):
    nombre = datos["nombre"].strip()

    conexion = conectar_bd()
    coincidencias = buscar_pescado_por_nombre(conexion, nombre)

    existe = next(
        (p for p in coincidencias if p["nombre"].lower() == nombre.lower()),
        None
    )

    if existe:
        conexion.close()
        return existe

    nuevo_id = crear_pescado(conexion, nombre)
    conexion.close()

    return {
        "id": nuevo_id,
        "nombre": nombre
    }


@app.get("/acompañante")
def acompañantes():
    conexion = conectar_bd()
    datos = obtener_acompañantes(conexion)
    conexion.close()
    return datos


@app.get("/acompañante/buscar")
def buscar_acompañantes(nombre: str):
    conexion = conectar_bd()
    datos = buscar_acompañante_por_nombre(conexion, nombre)
    conexion.close()
    return datos


@app.post("/acompañante")
def guardar_acompañante(datos: dict):
    nombre = datos["nombre"].strip()

    conexion = conectar_bd()
    coincidencias = buscar_acompañante_por_nombre(conexion, nombre)

    existe = next(
        (a for a in coincidencias if a["nombre"].lower() == nombre.lower()),
        None
    )

    if existe:
        conexion.close()
        return existe

    nuevo_id = crear_acompañante(conexion, nombre)
    conexion.close()

    return {
        "id": nuevo_id,
        "nombre": nombre
    }

@app.post("/viajes")
def guardar_viaje(datos: dict):
    conexion = conectar_bd()

    try:
        id_viaje = crear_viaje(
            conexion,
            datos["fecha"],
            datos["km"],
            datos["dinero_bruto"],
            datos["gastos"],
            datos.get("id_acompañante")
        )

        for destino in datos["destinos"]:
            id_destino = buscar_destino_por_nombre(
                conexion, destino["nombre"]
            )

            if id_destino:
                id_destino = id_destino[0]["id"]
            else:
                id_destino = crear_destino(
                    conexion, destino["nombre"], None
                )

            id_viaje_destino = crear_viaje_destino(
                conexion, id_viaje, id_destino
            )

            for carga in destino.get("cargas", []):
                coincidencias = buscar_pescado_por_nombre(
                    conexion, carga["pescado"]
                )

                pescado = next(
                    (p for p in coincidencias
                     if p["nombre"].casefold() == carga["pescado"].strip().casefold()),
                    None
                )

                if pescado:
                    id_pescado = pescado["id"]
                else:
                    id_pescado = crear_pescado(
                        conexion, carga["pescado"].strip().capitalize()
                    )

                crear_carga(
                    conexion,
                    carga["kg"],
                    id_pescado,
                    id_viaje_destino
                )

        conexion.commit()
        return {"mensaje": "Viaje guardado", "id_viaje": id_viaje}

    except Exception as error:
        conexion.rollback()
        return {"error": str(error)}

    finally:
        conexion.close()