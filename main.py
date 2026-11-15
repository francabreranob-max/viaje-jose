from bd import conectar_bd,obtener_viajes,obtener_destino,buscar_destino_por_nombre,crear_destino,buscar_comprador_por_nombre,obtener_compradores,crear_comprador
from bd import obtener_pescados, buscar_pescado_por_nombre, crear_pescado
from bd import obtener_acompañantes, buscar_acompañante_por_nombre, crear_acompañante
from bd import crear_viaje, crear_viaje_destino, crear_carga
from fastapi import FastAPI
from logica import calcular_km_recorrido
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
        # Buscar o crear acompañante
        nombre_acompanante = datos.get("acompañante", "").strip()
        id_acompanante = None

        if nombre_acompanante:
            coincidencias = buscar_acompañante_por_nombre(
                conexion, nombre_acompanante
            )
            print("Nombre recibido:", repr(nombre_acompanante))
            print("Coincidencias:", coincidencias)

            acompanante = next(
                (a for a in coincidencias
                 if a["nombre"].casefold() == nombre_acompanante.casefold()),
                None
            )

            if acompanante:
                id_acompanante = acompanante["id"]
            else:
                id_acompanante = crear_acompañante(
                    conexion, nombre_acompanante
                )

        # Crear viaje
        id_viaje = crear_viaje(
            conexion,
            datos["fecha"],
            datos["km"],
            datos["dinero_bruto"],
            datos["gastos"],
            id_acompanante
        )

        # Recorrer destinos
        for destino in datos["destinos"]:
            coincidencias = buscar_destino_por_nombre(
                conexion, destino["nombre"]
            )

            destino_existente = next(
                (d for d in coincidencias
                 if d["nombre"].casefold() == destino["nombre"].strip().casefold()),
                None
            )

            if destino_existente:
                id_destino = destino_existente["id"]
            else:
                id_destino = crear_destino(
                    conexion, destino["nombre"], None
                )

            id_viaje_destino = crear_viaje_destino(
                conexion, id_viaje, id_destino
            )

            # Recorrer cargas
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

                # Buscar o crear comprador
                nombre_comprador = carga.get("comprador", "").strip()
                id_comprador = None

                if nombre_comprador:
                    coincidencias = buscar_comprador_por_nombre(
                        conexion, nombre_comprador
                    )

                    comprador = next(
                        (c for c in coincidencias
                         if c["nombre"].casefold() == nombre_comprador.casefold()),
                        None
                    )

                    if comprador:
                        id_comprador = comprador["id"]
                    else:
                        id_comprador = crear_comprador(
                            conexion, nombre_comprador
                        )

                crear_carga(
                    conexion,
                    carga["kg"],
                    id_pescado,
                    id_viaje_destino,
                    id_comprador
                )

        conexion.commit()

        return {"mensaje": "Viaje guardado", "id_viaje": id_viaje}

    except Exception as error:
        conexion.rollback()
        return {"error": str(error)}

    finally:
        conexion.close()

@app.post("/calcular-km")
def calcular_kilometros(datos: dict):
    destinos = [
        d["nombre"].strip()
        for d in datos["destinos"]
        if d["nombre"].strip()
    ]

    if not destinos:
        return {"error": "Ingresá al menos un destino"}

    km = calcular_km_recorrido(destinos)

    if km is None:
        return {"error": "No se pudo calcular el recorrido"}

    return {"km": km}