document.addEventListener("DOMContentLoaded", function () {
    let totalAcumulado = 0;

    var datos=document.getElementById("anadir");
    var tabladatos=document.getElementById('tabla');
    if(datos){
        document.getElementById("anadir").addEventListener('click', function () {
            var imgElement = document.getElementById("idImagen");
            var imgSrc = imgElement.src;
            
            var priceElement = document.getElementById("idPrecio");
            var priceText = priceElement.textContent;
            var price = parseFloat(priceText.replace(/[^0-9.-]+/g, ""));
            
            var titleElement = document.getElementById("idNombre");
            var title = titleElement.textContent;
            
            guardarDatos(imgSrc, title, price, 1);
        });
    
        function guardarDatos(imagen, nombre, precio, cantidad) {
            // Simulando el almacenamiento de datos en localStorage
            let productos = JSON.parse(localStorage.getItem('productos')) || [];
            productos.push({ imagen, nombre, precio, cantidad });
            localStorage.setItem('productos', JSON.stringify(productos));
        }
    }    
});