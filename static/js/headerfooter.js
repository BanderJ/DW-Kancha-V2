function loadHTML(elementID, filePath, callback) {
    fetch(filePath)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar ' + filePath);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById(elementID).innerHTML = data;
            if (callback) callback();  // Ejecuta el callback después de cargar el contenido
        })
        .catch(error => console.log(error));
}

// Inicializar los dropdowns y sus funcionalidades
function initializeDropdown() {
    // Carrito
    const basketIcon = document.getElementById('basket-icon');
    const basketDropdown = document.getElementById('basket-dropdown');
    const closeButton = document.getElementById('close-basket');

    if (basketIcon) {
        basketIcon.addEventListener('click', function() {
            basketDropdown.style.display = 'block';
        });
    }

    if (closeButton) {
        closeButton.addEventListener('click', function() {
            ocultarCarrito();
        });
    }
    addRemoveItemListeners();
    addQuantityChangeListeners();
    updateBasketSummary();
    // Usuario
    const userDropdownButton = document.getElementById('user-dropdown-button');
    const userDropdownContent = document.getElementById('user-dropdown-content');

    if (userDropdownButton) {
        userDropdownButton.addEventListener('click', function() {
            if (userDropdownContent.style.display === "block") {
                userDropdownContent.style.display = "none";
            } else {
                userDropdownContent.style.display = "block";
            }
        });
    }

    window.addEventListener('click', function(event) {
        if (!event.target.matches('#user-dropdown-button')) {
            const dropdowns = document.getElementsByClassName("user-dropdown-content");
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.style.display === "block") {
                    openDropdown.style.display = "none";
                }
            }
        }
    });
}

// Funcionalidad para mostrar y ocultar el carrito
function mostrarCarrito() {
    document.getElementById('basket-dropdown').style.display = 'block';
}

function ocultarCarrito() {
    document.getElementById('basket-dropdown').style.display = 'none';
}

// Funcionalidad para eliminar ítems del carrito
function addRemoveItemListeners() {
    document.querySelectorAll('.remove-item').forEach(function(button) {
        button.addEventListener('click', function() {
            const basketItem = this.closest('.basket-item');
            basketItem.remove();
            updateBasketSummary();
        });
    });
}

// Función para actualizar el subtotal, total y la barra de progreso
function updateBasketSummary() {
    let subtotal = 0;
    const basketItems = document.querySelectorAll('.basket-item');
    const emptyBasketMessage = document.getElementById('empty-basket-message');

    if (basketItems.length === 0) {
        emptyBasketMessage.style.display = 'block';
    } else {
        emptyBasketMessage.style.display = 'none';
    }

    basketItems.forEach(function(basketItem) {
        const priceElement = basketItem.querySelector('.item-price');
        const quantityInput = basketItem.querySelector('.quantity-input');
        const price = parseFloat(priceElement.innerText.replace('S/', '').replace(',', ''));
        const quantity = parseInt(quantityInput.value);
        subtotal += price * quantity;
    });
    
    const delivery = subtotal >= 500 ? 0 : 20;
    const total = subtotal + delivery;
    
    document.getElementById('subtotal').innerText = `S/${subtotal.toFixed(2)}`;
    document.getElementById('delivery').innerText = `S/${delivery.toFixed(2)}`;
    document.getElementById('total').innerText = `S/${total.toFixed(2)}`;
    
    // Actualizar la barra de progreso
    const progress = Math.min((subtotal / 500) * 100, 100);
    document.getElementById('basket-progress').style.width = `${progress}%`;
    
    // Actualizar el mensaje de #shipping-price
    const shippingMsg = document.getElementById('shipping-price');
    if (subtotal >= 500) {
        shippingMsg.innerText = 'Tu envío será completamente gratis';
    } else {
        const restante = 500 - subtotal;
        shippingMsg.innerText = `Faltan S/${restante.toFixed(2)} para que el envío sea gratis`;
    }
}

// Escuchar cambios en las cantidades
function addQuantityChangeListeners() {
    document.querySelectorAll('.quantity-input').forEach(function(input) {
        input.addEventListener('change', function() {
            updateBasketSummary();
        });
    });
}
// Cargar header, footer y desplegable en las páginas
document.addEventListener('DOMContentLoaded', () => {
    loadHTML('header', 'header.html', initializeDropdown);
    loadHTML('footer', 'footer.html', initializeDropdown);
    loadHTML('carrito', 'carrito.html', initializeDropdown);
    loadHTML('usuario', 'opcionesUsuario.html', initializeDropdown);
});
