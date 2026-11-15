async function cargarViajes() {
    const respuesta = await fetch("http://127.0.0.1:8000/viajes");
    const viajes = await respuesta.json();

    const tabla = document.getElementById("tabla-viajes");
    tabla.innerHTML = "";

    viajes.forEach(viaje => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${viaje.fecha}</td>
            <td>${viaje.destinos ?? "—"}</td>
            <td>${viaje.km_hechos ?? "—"}</td>
            <td>${viaje.acompañante ?? "—"}</td>
            <td>${viaje.compradores ?? "—"}</td>
            <td>${viaje.cargas ?? "—"}</td>
            <td>${viaje.dinero_bruto_total ?? "—"}</td>
            <td>${viaje.gastos_viaje ?? "—"}</td>
            <td>${viaje.total ?? "—"}</td>
        `;

        tabla.appendChild(fila);
    });
}

cargarViajes();
const contenedorDestinos = document.getElementById("destinos");
const botonAgregar = document.getElementById("agregar-destino");

function crearDestino() {
    const nuevoDestino = document.createElement("div");
    nuevoDestino.classList.add("destino");

    nuevoDestino.innerHTML = `
        <input type="text" name="destino" placeholder="Destino" list="lista_destinos">

        <div class="cargas"></div>

        <button type="button" class="agregar-carga">
            AGREGAR CARGA
        </button>
    `;

    const botonCarga = nuevoDestino.querySelector(".agregar-carga");
    const contenedorCargas = nuevoDestino.querySelector(".cargas");

    botonCarga.addEventListener("click", function() {
        const nuevaCarga = document.createElement("div");

        nuevaCarga.innerHTML = `
            <input type="text" placeholder="Clase de pescado">
            <input type="number" placeholder="Kg">
        `;

        contenedorCargas.appendChild(nuevaCarga);
    });

    return nuevoDestino;
}

botonAgregar.addEventListener("click", function() {
    contenedorDestinos.appendChild(crearDestino());
});