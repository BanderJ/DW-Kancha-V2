document.addEventListener('DOMContentLoaded', function () {
    const basketButton = document.getElementById('basket-icon');
    const carrito = document.getElementById('carrito');

    basketButton.addEventListener('click', function () {
        carrito.classList.toggle('show'); // Alterna la clase 'show' para mostrar u ocultar el carrito
    });
});