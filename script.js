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

function agregarCarga(destino) {
    const contenedorCargas = destino.querySelector(".cargas");
    const nuevaCarga = document.createElement("div");

    nuevaCarga.innerHTML = `
        <input type="text" placeholder="Clase de pescado" class="pescado">
        <input type="number" placeholder="Kg" class="kg" min="1">
        <input type="text" placeholder="Comprador" class="comprador">
    `;

    contenedorCargas.appendChild(nuevaCarga);
}

function configurarDestino(destino) {
    const botonCarga = destino.querySelector(".agregar-carga");

    botonCarga.addEventListener("click", function() {
        agregarCarga(destino);
    });
}

// Configurar el primer destino que ya está en el HTML
document.querySelectorAll(".destino").forEach(destino => {
    configurarDestino(destino);
});

function crearDestino() {
    const nuevoDestino = document.createElement("div");
    nuevoDestino.classList.add("destino");

    nuevoDestino.innerHTML = `
        <input type="text" placeholder="Destino" list="lista_destinos">

        <div class="cargas"></div>

        <button type="button" class="agregar-carga">
            AGREGAR CARGA
        </button>
    `;

    configurarDestino(nuevoDestino);

    return nuevoDestino;
}

botonAgregar.addEventListener("click", function() {
    contenedorDestinos.appendChild(crearDestino());
});

// GUARDAR VIAJE
const formulario = document.querySelector("form");

formulario.addEventListener("submit", async function(event) {
    event.preventDefault();

    const destinos = [];

    document.querySelectorAll(".destino").forEach(destino => {
        const nombre = destino.querySelector('input[type="text"]').value.trim();

        const cargas = [];

        destino.querySelectorAll(".cargas > div").forEach(carga => {
            const pescado = carga.querySelector(".pescado").value.trim();
            const kg = carga.querySelector(".kg").value;

            const comprador = carga.querySelector(".comprador").value.trim();

            if (pescado && kg) {
                cargas.push({
                    pescado: pescado,
                    kg: Number(kg),
                    comprador: comprador
                });
            }
        });

        if (nombre) {
            destinos.push({
                nombre: nombre,
                cargas: cargas
            });
        }
    });

    const datos = {
        fecha: document.getElementById("fecha").value,
        km: Number(document.getElementById("km").value),
        dinero_bruto: Number(document.getElementById("dinero_bruto").value),
        gastos: Number(document.getElementById("gasto").value),
        acompañante: document.getElementById("acomp").value.trim(),
        destinos: destinos
    };

    try {
        const respuesta = await fetch("http://127.0.0.1:8000/viajes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok || resultado.error) {
            alert("Error al guardar: " + (resultado.error || "Error desconocido"));
            return;
        }

        alert("¡Viaje guardado correctamente!");

        formulario.reset();
        contenedorDestinos.innerHTML = `
            <div class="destino">
                <input type="text" placeholder="Destino" list="lista_destinos">
                <div class="cargas"></div>
                <button type="button" class="agregar-carga">AGREGAR CARGA</button>
            </div>
        `;

        configurarDestino(contenedorDestinos.querySelector(".destino"));

        await cargarViajes();

    } catch (error) {
        alert("No se pudo conectar con el servidor.");
        console.error(error);
    }
});

const botonCalcular = document.getElementById("calcular");

botonCalcular.addEventListener("click", async function() {

    const destinos = [];

    document.querySelectorAll(".destino").forEach(destino => {
        const nombre = destino.querySelector('input[type="text"]').value.trim();

        if (nombre) {
            destinos.push({ nombre: nombre });
        }
    });

    if (destinos.length === 0) {
        alert("Ingresá al menos un destino");
        return;
    }

    botonCalcular.disabled = true;
    botonCalcular.textContent = "CALCULANDO...";

    try {
        const respuesta = await fetch("http://127.0.0.1:8000/calcular-km", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ destinos: destinos })
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok || resultado.error) {
            alert(resultado.error || "No se pudo calcular el recorrido");
            return;
        }

        document.getElementById("km").value = Math.round(resultado.km);

        alert("Kilómetros calculados correctamente: " + resultado.km);

    } catch (error) {
        alert("No se pudo conectar con el servidor");
        console.error(error);

    } finally {
        botonCalcular.disabled = false;
        botonCalcular.textContent = "CALCULAR";
    }
});