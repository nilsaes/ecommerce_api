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