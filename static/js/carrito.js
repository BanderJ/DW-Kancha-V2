// Obtener el carrito del localStorage o inicializarlo vacío
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Referencias a los elementos del DOM
const itemCountEl = document.getElementById('item-count');
const subtotalEl = document.getElementById('subtotal');
const deliveryEl = document.getElementById('delivery');
const totalEl = document.getElementById('total');
const basketsummary = document.getElementById('cuentas');
const basketItemsEl = document.querySelector('.basket-items');
const emptyMessageEl = document.getElementById('empty-basket-message');
const basketDropdownEl = document.getElementById('basket-dropdown');

// Configuración para el costo de entrega y umbral de envío gratuito
const deliveryCost = 20.00;
const freeShippingThreshold = 500.00;

// Mostrar y ocultar el carrito
document.getElementById('basket-icon').addEventListener('click', function() {
    mostrarCarrito();
    updateBasketSummary()
});

document.getElementById('close-basket').addEventListener('click', function() {
    ocultarCarrito();
});

function mostrarCarrito() {
    basketDropdownEl.style.display = 'block';
}

function ocultarCarrito() {
    basketDropdownEl.style.display = 'none';
}

// Función para renderizar el carrito en el DOM
function renderizarCarrito() {
    basketItemsEl.innerHTML = '';  // Limpiar el contenido previo

    if (carrito.length === 0) {
        emptyMessageEl.style.display = 'block';
    } else {
        emptyMessageEl.style.display = 'none';
        carrito.forEach((producto, index) => {
            const productoHTML = `
                <div class="basket-item d-flex align-items-center" data-id="${producto.id}">
                    <img src="${producto.imagen}" alt="${producto.nombre}" class="item-img">
                    <div class="item-details flex-grow-1">
                        <p class="item-name">${producto.nombre}</p>
                        <p class="item-size">Talla: ${producto.talla}</p>
                        <div class="item-quantity d-flex align-items-center">
                            <label for="quantity" class="mb-0 mr-2">Cantidad</label>
                            <input type="number" class="form-control quantity-input" value="${producto.cantidad}" min="1" data-index="${index}">
                        </div>
                    </div>
                    <p class="item-price mb-0">S/${(producto.precio).toFixed(2)}</p>
                    <button class="remove-item btn btn-link" data-index="${index}">X</button>
                </div>
            `;
            basketItemsEl.insertAdjacentHTML('beforeend', productoHTML);
        });

        // Actualizar los event listeners para eliminar productos y cambiar cantidades
        addRemoveItemListeners();
        addQuantityChangeListeners();

        // Actualizar los totales
        updateBasketSummary();
    }
}

// Funcionalidad para eliminar ítems del carrito
function addRemoveItemListeners() {
    document.querySelectorAll('.remove-item').forEach(function(button) {
        button.addEventListener('click', function() {
            const index = this.dataset.index;
            carrito.splice(index, 1);  // Eliminar el producto del carrito
            localStorage.setItem('carrito', JSON.stringify(carrito));  // Guardar el carrito actualizado
            renderizarCarrito();  // Volver a renderizar el carrito
            updateBasketSummary();
        });
    });
}

// Escuchar cambios en las cantidades
function addQuantityChangeListeners() {
    document.querySelectorAll('.quantity-input').forEach(function(input) {
        input.addEventListener('change', function() {
            const index = input.dataset.index;
            const nuevaCantidad = parseInt(input.value);
            if (nuevaCantidad > 0) {
                carrito[index].cantidad = nuevaCantidad;
                localStorage.setItem('carrito', JSON.stringify(carrito));  // Guardar el carrito actualizado
                updateBasketSummary();  // Actualizar el resumen
            } else {
                alert('La cantidad no puede ser menor a 1.');
            }
        });
    });
}

// Función para actualizar el subtotal, total y la barra de progreso
function updateBasketSummary() {
    let subtotal = 0;
    const basketItems = document.querySelectorAll('.basket-item');
    
    if (basketItems.length === 0) {
        emptyMessageEl.style.display = 'block';
        basketsummary.style.display = 'none';
    } else {
        emptyMessageEl.style.display = 'none';
        basketsummary.style.display = 'block';
    }

    carrito.forEach(function(producto) {
        subtotal += producto.precio * producto.cantidad;
    });
    
    const delivery = subtotal >= freeShippingThreshold ? 0 : deliveryCost;
    const total = subtotal + delivery;

    // Actualizar los valores en el DOM
    subtotalEl.innerText = `S/${subtotal.toFixed(2)}`;
    deliveryEl.innerText = `S/${delivery.toFixed(2)}`;
    totalEl.innerText = `S/${total.toFixed(2)}`;
    itemCountEl.innerText = carrito.length;

    // Actualizar la barra de progreso
    const progress = Math.min((subtotal / freeShippingThreshold) * 100, 100);
    document.getElementById('basket-progress').style.width = `${progress}%`;
    
    // Actualizar el mensaje de #shipping-price
    const shippingMsg = document.getElementById('shipping-price');
    if (subtotal >= freeShippingThreshold) {
        shippingMsg.innerText = 'Tu envío será completamente gratis';
    } else {
        const restante = freeShippingThreshold - subtotal;
        shippingMsg.innerText = `Faltan S/${restante.toFixed(2)} para que el envío sea gratis`;
    }
}

// Función para agregar un producto al carrito de manera dinámica
function agregarProductoAlCarrito(id, nombre, precio, imagen, talla) {
    // Verificar si el producto ya está en el carrito
    const productoExistente = carrito.find(producto => producto.id === id);

    if (productoExistente) {
        productoExistente.cantidad++;  // Incrementar la cantidad si ya está en el carrito
    } else {
        carrito.push({ id, nombre, precio, imagen, talla, cantidad: 1 });  // Agregar nuevo producto
    }

    // Guardar el carrito en el localStorage
    localStorage.setItem('carrito', JSON.stringify(carrito));

    // Renderizar el carrito actualizado
    renderizarCarrito();
}

// Escuchar los clics en los botones de "Agregar al carrito"
document.querySelectorAll('.agregar-carrito').forEach(function(button) {
    button.addEventListener('click', function() {
        const id = parseInt(button.getAttribute('data-id'));
        const nombre = button.getAttribute('data-nombre');
        const precio = parseFloat(button.getAttribute('data-precio'));
        const imagen = button.getAttribute('data-imagen');
        const talla = button.getAttribute('data-talla');
        
        // Llamar a la función para agregar el producto al carrito
        agregarProductoAlCarrito(id, nombre, precio, imagen, talla);
    });
});

// Inicializar la funcionalidad del carrito
renderizarCarrito();
