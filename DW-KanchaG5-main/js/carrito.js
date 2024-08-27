document.getElementById('basket-icon').addEventListener('click', function() {
    document.getElementById('basket-dropdown').style.display = 'block';
});

function mostrarCarrito() {
    document.getElementById('basket-dropdown').style.display = 'block';
}
function ocultarCarrito() {
    document.getElementById('basket-dropdown').style.display = 'none';
}
document.getElementById('close-basket').addEventListener('click', function() {
    ocultarCarrito();
});

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


// Inicializar los event listeners
addRemoveItemListeners();
addQuantityChangeListeners();

// Llamar a la función para actualizar el resumen del carrito al cargar la página
updateBasketSummary();
