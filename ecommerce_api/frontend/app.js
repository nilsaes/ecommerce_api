// --- CONFIGURACIÓN Y ESTADO ---
const API_URL = "http://127.0.0.1:8000/api/";
let token = localStorage.getItem("token") || null;

// Ejecutar apenas carga la página
document.addEventListener("DOMContentLoaded", () => {
    cargarProductos();
    actualizarInterfazNavbar();
});

// --- 1. LÓGICA DE CARGA DE PRODUCTOS ---
async function cargarProductos() {
    const contenedor = document.getElementById("contenedor-productos");
    try {
        const response = await fetch(`${API_URL}products/`);
        const productos = await response.json();

        contenedor.innerHTML = ""; // Limpiamos el loader o mensaje previo

        productos.forEach(prod => {
            const precio = prod.variants.length > 0 ? prod.variants[0].price : "0";
            const imagen = prod.image || "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=600&q=80";
            
            contenedor.innerHTML += `
                <div class="col">
                    <div class="card card-producto-premium h-100">
                        <div class="product-image-wrapper">
                            <img src="${imagen}" alt="${prod.name}" class="img-fluid">
                        </div>
                        <div class="card-body p-4">
                            <h5 class="fw-bold">${prod.name}</h5>
                            <p class="text-muted small">${prod.description}</p>
                            <div class="fs-4 fw-extrabold" style="color: #6f42c1;">₲${Number(precio).toLocaleString('es-PY')}</div>
                            <button class="btn btn-premium-violet w-100 mt-3" onclick="alert('Funcionalidad de variantes activa')">Ver Detalle</button>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (error) {
        console.error("Error al obtener productos:", error);
    }
}

// --- 2. LÓGICA DE LOGIN Y AUTENTICACIÓN ---
const formLogin = document.getElementById("form-login");
if (formLogin) {
    formLogin.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const username = document.getElementById("login-username").value;
        const password = document.getElementById("login-password").value;
        const errorDiv = document.getElementById("login-error");

        try {
            const response = await fetch(`${API_URL}token/`, { 
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("token", data.access);
                token = data.access;
                
                // Cerrar modal y refrescar
                const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
                modal.hide();
                actualizarInterfazNavbar();
                alert("¡Bienvenida de nuevo, Nilsa!");
            } else {
                errorDiv.classList.remove("d-none");
                errorDiv.innerText = "Usuario o contraseña incorrectos.";
            }
        } catch (error) {
            errorDiv.classList.remove("d-none");
            errorDiv.innerText = "Error de conexión con el servidor.";
        }
    });
}

// --- 3. UTILIDADES DE UI ---
function actualizarInterfazNavbar() {
    const btnLogin = document.getElementById("btn-login");
    if (token) {
        btnLogin.innerHTML = "👤 Mi Perfil";
        btnLogin.classList.replace("btn-outline-light", "btn-light");
    }
}