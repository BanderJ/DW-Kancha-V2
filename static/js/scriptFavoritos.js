function toggleFavorite(icon) {
    const idProducto = icon.dataset.id; 
    const idCliente = icon.getAttribute('cliente-id'); 
    console.log("ID del Cliente:", idCliente); 
    console.log(idCliente); 

    const corazonLleno = icon.dataset.corazonLleno;
    const corazonVacio = icon.dataset.corazonVacio;

    if (icon.src.includes('corazonLleno.svg')) {
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
    const idProducto = icon.dataset.id; 
    const idCliente = icon.getAttribute('cliente-id');
    console.log("ID del Cliente:", idCliente);
    console.log("ID del Producto:", idProducto); 

    const img = icon.querySelector('img'); 
    const corazonLleno = img.dataset.corazonLleno; 
    const corazonVacio = img.dataset.corazonVacio; 

    if (img.src.includes('corazonLleno.svg')) {
        img.src = corazonVacio;

        fetch('/eliminar_favorito', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idCliente, idProducto })
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

        img.src = corazonLleno;

        fetch('/agregar_favorito', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idCliente, idProducto }) 
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
