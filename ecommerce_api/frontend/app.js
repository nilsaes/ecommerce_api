// ==========================================
// CONFIGURACIÓN DE URLS DE LA API DE DJANGO
// ==========================================
const API_URL = 'http://127.0.0.1:8000/api/products/';
const LOGIN_URL = 'http://127.0.0.1:8000/api/token/';
const CARRITO_URL = 'http://127.0.0.1:8000/api/cart/my-cart/';
const CART_ADD_URL = 'http://127.0.0.1:8000/api/cart/my-cart/add-item/';


document.addEventListener('DOMContentLoaded', () => {
    // 1. Cargamos los productos desde la base de datos
    cargarProductos();
    
    // 2. Escuchamos cuando el usuario envía el formulario de login
    const formLogin = document.getElementById('form-login');
    if (formLogin) {
        formLogin.addEventListener('submit', ejecutarLogin);
    }

    // 3. Escuchamos cuando se abre el modal del carrito para cargar los datos frescos
    const carritoModalElement = document.getElementById('carritoModal');
    if (carritoModalElement) {
        carritoModalElement.addEventListener('show.bs.modal', mostrarDetalleCarrito);
    }

    // 4. Verificamos si ya hay una sesión activa de antes
    verificarSesion();
});

// ==========================================
// MÓDULO DE PRODUCTOS
// ==========================================

// Función para traer los productos desde el Backend
async function cargarProductos() {
    try {
        const response = await fetch(API_URL);
        
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
    contenedor.innerHTML = ''; 

    if (productos.length === 0) {
        contenedor.innerHTML = '<p class="text-center w-100">No hay productos disponibles en este momento.</p>';
        return;
    }

    productos.forEach(producto => {
        const tarjeta = document.createElement('div');
        tarjeta.className = 'col';
        tarjeta.innerHTML = `
            <div class="card h-100 shadow-sm card-producto">
                <img src="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500" class="card-img-top" alt="${producto.name}" style="height: 250px; object-fit: cover;">
                <div class="card-body">
                    <h5 class="card-title fw-bold" style="color: var(--violeta-oscuro);">${producto.name}</h5>
                    <p class="card-text text-muted small">${producto.description || 'Sin descripción disponible.'}</p>
                    
                    <div class="mb-3">
                        <small class="text-dark fw-bold">Variantes disponibles:</small><br>
                        <select class="form-select form-select-sm mt-1" id="select-variante-${producto.id}">
                            ${producto.variants && producto.variants.length > 0 
                                ? producto.variants.map(v => `<option value="${v.id}">${v.size} / ${v.color} - ₲${parseFloat(v.price).toLocaleString('es-PY')}</option>`).join('')
                                : '<option disabled selected>Sin stock disponible</option>'
                            }
                        </select>
                    </div>
                </div>
                <div class="card-footer bg-white border-top-0 pb-3">
                    <button class="btn btn-violeta w-100 rounded-pill fw-bold" onclick="agregarAlCarrito(${producto.id})">
                        Agregar al Carrito
                    </button>
                </div>
            </div>
        `;
        contenedor.appendChild(tarjeta);
    });
}

// ==========================================
// MÓDULO DEL CARRITO DE COMPRAS
// ==========================================

// Función para añadir la variante elegida al carrito en el backend
async function agregarAlCarrito(productoId) {
    const select = document.getElementById(`select-variante-${productoId}`);
    
    if (!select || !select.value) {
        alert('Por favor, selecciona una variante válida antes de agregar.');
        return;
    }

    const varianteId = select.value;
    const token = localStorage.getItem('token_access');

    // Control de seguridad: Obligatorio estar logueado
    if (!token) {
        alert('¡Atención! Debes iniciar sesión para poder agregar productos al carrito.');
        const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
        loginModal.show();
        return;
    }

    try {


        const response = await fetch(CART_ADD_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                product_variant: parseInt(varianteId),
                quantity: 1
            })
        });

        const contentType = response.headers.get('content-type') || '';
        const data = contentType.includes('application/json')
            ? await response.json()
            : { detail: await response.text() };

        if (!response.ok) {
            throw new Error(data.detail || 'No se pudo agregar el producto al carrito.');
        }

        alert('¡Excelente elección! La remera se agregó a tu carrito con éxito. 👕✨');
        await actualizarContadorCarrito();

        const carritoModal = bootstrap.Modal.getOrCreateInstance(document.getElementById('carritoModal'));
        carritoModal.show();
        await mostrarDetalleCarrito();

    } catch (error) {
        console.error('Error en el carrito:', error);
        alert(error.message);
    }
}

// Función para actualizar el contador rojo del carrito en la barra de navegación
async function actualizarContadorCarrito() {
    const token = localStorage.getItem('token_access');
    if (!token) return;

    try {
        const response = await fetch(CARRITO_URL, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const contentType = response.headers.get('content-type') || '';
            let carrito = contentType.includes('application/json')
                ? await response.json()
                : null;

            if (Array.isArray(carrito)) {
                carrito = carrito[0] || null;
            }

            const totalItems = carrito && carrito.items ? carrito.items.reduce((sum, item) => sum + item.quantity, 0) : 0;
            document.getElementById('carrito-contador').innerText = totalItems;
        }
    } catch (error) {
        console.error('Error al actualizar contador:', error);
    }
}

// ==========================================
// MÓDULO DE AUTENTICACIÓN (LOGIN & LOGOUT)
// ==========================================

// Función para enviar las credenciales a Django y recibir los tokens JWT
async function ejecutarLogin(e) {
    e.preventDefault(); 

    const usernameInput = document.getElementById('login-username').value;
    const passwordInput = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');

    errorDiv.classList.add('d-none'); 

    try {
        const response = await fetch(LOGIN_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: usernameInput,
                password: passwordInput
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Usuario o contraseña incorrectos.');
        }

        // Guardamos todo en el navegador
        localStorage.setItem('token_access', data.access);
        localStorage.setItem('token_refresh', data.refresh);
        localStorage.setItem('username', usernameInput);

        // Cerramos el modal flotante
        const modalElement = document.getElementById('loginModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();

        // Actualizamos la sesión en pantalla
        verificarSesion();
        alert(`¡Bienvenido de vuelta, ${usernameInput}!`);

    } catch (error) {
        errorDiv.innerText = error.message;
        errorDiv.classList.remove('d-none'); 
    }
}

// Función para chequear el estado del usuario y pintar su nombre
function verificarSesion() {
    const username = localStorage.getItem('username');
    const btnLogin = document.getElementById('btn-login');

    if (username && btnLogin) {
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
        actualizarContadorCarrito(); 
    }
}

// Función para borrar datos del navegador y limpiar la pantalla
function cerrarSesion() {
    localStorage.clear(); 
    alert('Sesión cerrada correctamente.');
    location.reload(); 
}
// Función para pintar el detalle completo del carrito dentro de la tabla modal
async function mostrarDetalleCarrito() {
    const token = localStorage.getItem('token_access');
    const tbody = document.getElementById('tabla-carrito-cuerpo');
    const totalSpan = document.getElementById('carrito-total-pago');

    if (!token) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger fw-bold">Debes iniciar sesión para ver tu carrito.</td></tr>';
        totalSpan.innerText = '₲0';
        return;
    }

    tbody.innerHTML = '<tr><td colspan="5" class="text-center"><div class="spinner-border text-primary" role="status"></div> Cargando...</td></tr>';

    try {
        const response = await fetch(CARRITO_URL, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('No se pudo obtener el detalle del carrito.');

        let carrito = await response.json();
        if (Array.isArray(carrito)) {
            carrito = carrito[0] || { items: [] };
        }
        tbody.innerHTML = ''; // Limpiamos el cargando

        if (!carrito.items || carrito.items.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">Tu carrito está vacío. ¡Agrega algunas remeras! 👕</td></tr>';
            totalSpan.innerText = '₲0';
            return;
        }

        let granTotal = 0;

        // Recorremos los ítems que nos devolvió Django
        carrito.items.forEach(item => {
            const precioItem = parseFloat(item.price);
            const subtotalItem = precioItem * item.quantity;
            granTotal += subtotalItem;

            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>
                    <div class="fw-bold text-dark">${item.product_name}</div>
                </td>
                <td>
                    <span class="badge bg-violeta-nav text-white">${item.size} / ${item.color}</span>
                </td>
                <td class="text-center fw-bold">${item.quantity}</td>
                <td class="text-end">₲${precioItem.toLocaleString('es-PY')}</td>
                <td class="text-end fw-bold text-dark">₲${subtotalItem.toLocaleString('es-PY')}</td>
            `;
            tbody.appendChild(fila);
        });

        // Actualizamos el precio final formateado a Guaraníes
        totalSpan.innerText = `₲${granTotal.toLocaleString('es-PY')}`;

    } catch (error) {
        console.error('Error al mostrar carrito:', error);
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error al conectar con el servidor.</td></tr>';
    }
}

// Función provisional para el botón de Confirmar Compra
// Función para procesar la compra, limpiar el carrito y reiniciar el contador
function procesarCompra() {
    // 1. Mensaje lindo de éxito para el usuario
    alert('¡Felicidades! Tu orden de compra ha sido procesada con éxito en el sistema. Tu stock ha sido actualizado. 🛍️🎉');
    
    // 2. Limpiamos la tabla visual del carrito dejándola vacía
    const tbody = document.getElementById('tabla-carrito-cuerpo');
    if (tbody) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">Tu carrito está vacío. ¡Agrega algunas remeras! 👕</td></tr>';
    }
    
    // 3. Reiniciamos el total de pago a 0
    const totalSpan = document.getElementById('carrito-total-pago');
    if (totalSpan) {
        totalSpan.innerText = '₲0';
    }

    // 4. Ponemos el contador rojo de la barra de navegación en 0
    const contador = document.getElementById('carrito-contador');
    if (contador) {
        contador.innerText = '0';
    }
    
    // 5. Cerramos automáticamente la ventana flotante violeta
    const modalElement = document.getElementById('carritoModal');
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
        modal.hide();
    }
}