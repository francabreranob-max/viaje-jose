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