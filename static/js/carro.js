function actualizarCantidad(idProducto, idProducto, idCarrito, accion) {
    const cantidadSpan = document.getElementById(`cantidad-${idProducto}`);
    const subtotalSpan = document.getElementById(`subtotal-${idProducto}`);
    const cantidadActual = parseInt(cantidadSpan.textContent);

    // Crear el FormData para enviar al servidor
    const formData = new FormData();
    formData.append('id_producto', idProducto);
    formData.append('id_carrito', idCarrito);
    formData.append('accion', accion);  // 'mas' o 'menos'

    fetch('/actualizar_cantidad', {  // Ajusta el endpoint
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Mostrar modal con mensaje de error si hay
            mostrarModalError(data.error);
        } else {
            // Actualizar la cantidad y el subtotal en el frontend
            cantidadSpan.textContent = data.nueva_cantidad;
            subtotalSpan.textContent = (data.precio_unitario * data.nueva_cantidad).toFixed(2);
            actualizarTotalCarrito();
        }
    })
    .catch(error => console.error('Error:', error));
}

function mostrarModalError(mensaje) {
    const modalErrorBody = document.getElementById('modalErrorCantidadBody');
    modalErrorBody.textContent = mensaje;
    const modal = new bootstrap.Modal(document.getElementById('modalErrorCantidad'));
    modal.show();
}

function actualizarTotalCarrito() {
    let total = 0;
    document.querySelectorAll('span[id^="subtotal-"]').forEach(subtotalSpan => {
        total += parseFloat(subtotalSpan.textContent);
    });
    document.getElementById('total-carrito').textContent = total.toFixed(2);
}
