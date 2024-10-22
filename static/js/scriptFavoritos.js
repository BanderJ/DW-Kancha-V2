function toggleFavorite(icon) {
    const idProducto = icon.dataset.id; // Accede al id del producto
    const idCliente = icon.getAttribute('cliente-id'); // Cambiar 'element' a 'icon'
    console.log("ID del Cliente:", idCliente); // Imprimir el idCliente
    console.log(idCliente); // Imprimir idCliente nuevamente

    const corazonLleno = icon.dataset.corazonLleno;
    const corazonVacio = icon.dataset.corazonVacio;

    if (icon.src.includes('corazonLleno.svg')) {
        // Cambiar a corazón vacío y eliminar de favoritos
        icon.src = corazonVacio;

        fetch('/eliminar_favorito', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idCliente, idProducto })
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Error al eliminar de favoritos:', error));
    } else {
        // Cambiar a corazón lleno y agregar a favoritos
        icon.src = corazonLleno;

        fetch('/agregar_favorito', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idCliente, idProducto })
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Error al agregar a favoritos:', error));
    }
}

function toggleFavoritedp(icon) {
    const idProducto = icon.dataset.id; // Obtener el id del producto desde el atributo data-id
    const idCliente = icon.getAttribute('cliente-id'); // Obtener el id del cliente
    console.log("ID del Cliente:", idCliente);
    console.log("ID del Producto:", idProducto); // Mostrar el id del producto en la consola

    // Accede a la imagen dentro del botón
    const img = icon.querySelector('img'); // Asegúrate de que haya una imagen en el botón
    const corazonLleno = img.dataset.corazonLleno; // URL del corazón lleno
    const corazonVacio = img.dataset.corazonVacio; // URL del corazón vacío

    if (img.src.includes('corazonLleno.svg')) {
        // Cambiar a corazón vacío y eliminar de favoritos
        img.src = corazonVacio;

        fetch('/eliminar_favorito', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idCliente, idProducto }) // Enviar los datos en formato JSON
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red');
            }
            return response.json();
        })
        .then(data => console.log(data.message))
        .catch(error => console.error('Error al eliminar de favoritos:', error));
    } else {
        // Cambiar a corazón lleno y agregar a favoritos
        img.src = corazonLleno;

        fetch('/agregar_favorito', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idCliente, idProducto }) // Enviar los datos en formato JSON
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red');
            }
            return response.json();
        })
        .then(data => console.log(data.message))
        .catch(error => console.error('Error al agregar a favoritos:', error));
    }
}
