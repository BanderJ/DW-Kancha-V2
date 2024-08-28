document.addEventListener("DOMContentLoaded", function () {
    let totalAcumulado = 0;
    const tabla = document.getElementById('tabla').getElementsByTagName('tbody')[0];
    cargarCarrito();
    actualizarTotal();

    function cargarCarrito() {
        // Cargar productos desde localStorage al cargar la página
        let productos = JSON.parse(localStorage.getItem('productos')) || [];
        productos.forEach(producto => agregarFila(producto.imagen, producto.nombre, producto.precio, producto.cantidad));
    }

    function agregarFila(imagen, nombre, precio, cantidad) {
        let productoExistente = false;

        for (let i = 0; i < tabla.rows.length; i++) {
            const fila = tabla.rows[i];
            if (fila.cells[1].textContent === nombre) {
                const cantidadExistente = parseInt(fila.cells[3].textContent, 10);
                const nuevaCantidad = cantidadExistente + Number(cantidad);
                fila.cells[3].textContent = nuevaCantidad;

                const precioUnitario = parseFloat(fila.cells[2].textContent.replace('s/', ''));
                const totalProducto = precioUnitario * nuevaCantidad;
                fila.cells[4].textContent = "s/" + totalProducto.toFixed(2);

                productoExistente = true;
                totalAcumulado += precioUnitario * cantidad;
                actualizarTotal();
                break;
            }
        }

        if (!productoExistente) {
            const nuevaFila = tabla.insertRow();

            const celdaImagen = nuevaFila.insertCell(0);
            const celdaNombre = nuevaFila.insertCell(1);
            const celdaPrecio = nuevaFila.insertCell(2);
            const celdaCantidad = nuevaFila.insertCell(3);
            const celdaTotal = nuevaFila.insertCell(4);
            const celdaEliminar = nuevaFila.insertCell(5);

            const img = document.createElement('img');
            img.src = imagen;
            img.width = 50;
            celdaImagen.appendChild(img);

            celdaNombre.textContent = nombre;
            celdaPrecio.textContent = "s/" + precio.toFixed(2);
            celdaCantidad.textContent = cantidad;
            const totalProducto = precio * cantidad;
            celdaTotal.textContent = "s/" + totalProducto.toFixed(2);

            const botonEliminar = document.createElement('button');
            botonEliminar.textContent = 'Eliminar';
            botonEliminar.addEventListener('click', () => {
                const totalProductoActual = parseFloat(celdaTotal.textContent.replace('s/', ''));
                totalAcumulado -= totalProductoActual;
                tabla.deleteRow(nuevaFila.rowIndex - 1);
                actualizarTotal();

                let productos = JSON.parse(localStorage.getItem('productos')) || [];
                productos = productos.filter(p => p.nombre !== nombre);
                localStorage.setItem('productos', JSON.stringify(productos));

                if (productos.length === 0) {
                    localStorage.removeItem('productos');
                    window.location.href = 'carrito.html';
                }
            });
            celdaEliminar.appendChild(botonEliminar);

            totalAcumulado += totalProducto;
            actualizarTotal();
        }
    }

    function actualizarTotal() {
        const totalElement = document.getElementById("total");
        console.log("Total acumulado:", totalAcumulado);  // Depuración
        totalElement.textContent = `Total: s/${totalAcumulado.toFixed(2)}`;
    }
});
