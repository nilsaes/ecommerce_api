// La URL de tu API de Django (el endpoint de productos que armaste)
const API_URL = 'http://127.0.0.1:8000/api/products/';

// Esperamos a que la página cargue por completo
document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
});

// Función para traer los productos desde el Backend
async function cargarProductos() {
    try {
        // Hacemos la petición a Django
        const response = await fetch(API_URL);
        
        // Si la respuesta no es correcta, lanzamos un error
        if (!response.ok) {
            throw new Error('Error al conectar con la API');
        }

        const productos = await response.json();
        dibujarProductos(productos);

    } catch (error) {
        console.error('Hubo un problema:', error);
        document.getElementById('contenedor-productos').innerHTML = `
            <div class="alert alert-danger w-100 text-center" role="alert">
                No se pudieron cargar los productos. Asegurate de que el backend esté corriendo.
            </div>
        `;
    }
}

// Función para pintar las remeras en el HTML de forma dinámica
function dibujarProductos(productos) {
    const contenedor = document.getElementById('contenedor-productos');
    contenedor.innerHTML = ''; // Limpiamos por si hay algo

    if (productos.length === 0) {
        contenedor.innerHTML = '<p class="text-center w-100">No hay productos disponibles en este momento.</p>';
        return;
    }

    // Recorremos cada producto que nos devolvió Django
    productos.forEach(producto => {
        // Creamos una tarjeta de Bootstrap para cada uno
        const tarjeta = document.createElement('div');
        tarjeta.className = 'col';
        tarjeta.innerHTML = `
            <div class="card h-100 shadow-sm">
                <img src="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500" class="card-img-top" alt="${producto.name}" style="height: 250px; object-fit: cover;">
                <div class="card-body">
                    <h5 class="card-title">${producto.name}</h5>
                    <p class="card-text text-muted">${producto.description || 'Sin descripción disponible.'}</p>
                    
                    <div class="mb-3">
                        <small class="text-dark fw-bold">Variantes disponibles:</small><br>
                        <select class="form-select form-select-sm mt-1" id="select-variante-${producto.id}">
                            ${producto.variants && producto.variants.length > 0 
                                ? producto.variants.map(v => `<option value="${v.id}">${v.size} / ${v.color} - ₲${parseFloat(v.price).toLocaleString('es-PY')}</option>`).join('')
                                : '<option disabled>Sin stock</option>'
                            }
                        </select>
                    </div>
                </div>
                <div class="card-footer bg-white border-top-0 pb-3">
                    <button class="btn btn-dark w-100" onclick="agregarAlCarrito(${producto.id})">
                        Agregar al Carrito
                    </button>
                </div>
            </div>
        `;
        contenedor.appendChild(tarjeta);
    });
}

// Función provisional para el botón (la completaremos más adelante)
function agregarAlCarrito(productoId) {
    const select = document.getElementById(`select-variante-${productoId}`);
    const varianteSeleccionada = select ? select.value : 'Ninguna';
    alert(`¡Remera añadida! ID Producto: ${productoId}, ID Variante: ${varianteSeleccionada}. (Pronto la conectaremos al carrito real)`);
}

// URL para obtener el Token JWT que configuraste en Django
const LOGIN_URL = 'http://127.0.0.1:8000/api/token/';

document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
    
    // Escuchamos cuando el usuario envía el formulario de login
    const formLogin = document.getElementById('form-login');
    if (formLogin) {
        formLogin.addEventListener('submit', ejecutarLogin);
    }

    // Verificamos si ya hay una sesión activa al cargar la página
    verificarSesion();
});

// Función para procesar el inicio de sesión
async function ejecutarLogin(e) {
    e.preventDefault(); // Evitamos que la página se recargue

    const usernameInput = document.getElementById('login-username').value;
    const passwordInput = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');

    errorDiv.classList.add('d-none'); // Ocultamos errores anteriores

    try {
        const response = await fetch(LOGIN_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: usernameInput,
                password: passwordInput
            })
        });

        const data = await response.json();

        if (!response.ok) {
            // Si Django nos rebota, mostramos el error
            throw new Error(data.detail || 'Usuario o contraseña incorrectos.');
        }

        // ¡Éxito! Guardamos los tokens en el navegador
        localStorage.setItem('token_access', data.access);
        localStorage.setItem('token_refresh', data.refresh);
        localStorage.setItem('username', usernameInput);

        // Cerramos la ventana flotante (Modal) de Bootstrap de forma limpia
        const modalElement = document.getElementById('loginModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();

        // Actualizamos la barra de navegación para darle la bienvenida
        verificarSesion();
        alert(`¡Bienvenido de vuelta, ${usernameInput}!`);

    } catch (error) {
        errorDiv.innerText = error.message;
        errorDiv.classList.remove('d-none'); // Mostramos el cartel rojo de error
    }
}

// Función para comprobar si el usuario está logueado y cambiar los botones
function verificarSesion() {
    const username = localStorage.getItem('username');
    const btnLogin = document.getElementById('btn-login');

    if (username && btnLogin) {
        // Si está logueado, transformamos el botón de login en su nombre y un botón de salir
        btnLogin.outerHTML = `
            <div class="dropdown" id="user-menu">
                <button class="btn btn-violeta px-4 rounded-pill dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    👤 ${username}
                </button>
                <ul class="dropdown-menu dropdown-menu-end shadow">
                    <li><a class="dropdown-item text-danger" href="#" onclick="cerrarSesion()">Cerrar Sesión</a></li>
                </ul>
            </div>
        `;
    }
}

// Función para limpiar los tokens y cerrar sesión
function cerrarSesion() {
    localStorage.clear(); // Borra todo lo guardado
    alert('Sesión cerrada correctamente.');
    location.reload(); // Recargamos la página para restaurar los botones originales
}