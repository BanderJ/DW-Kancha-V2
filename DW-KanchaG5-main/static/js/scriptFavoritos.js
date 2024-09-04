document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.querySelector('.items');
    const leftNav = document.querySelector('.nav.left');
    const rightNav = document.querySelector('.nav.right');
    const indicatorsContainer = document.querySelector('.indicators');
    let items;
    let totalItems;
    let currentIndex = 0;
    let itemsToShow = 3;

    // Cargar productos desde localStorage
    function loadProducts() {
        const productos = JSON.parse(localStorage.getItem('productosFavoritos')) || [];
        const contenedor = document.getElementById('losfavoritos');
        contenedor.innerHTML = ''; // Limpiar contenedor

        if (productos.length > 0) {
            productos.forEach(producto => {
                const divItem = document.createElement('div');
                divItem.classList.add('item');
                divItem.innerHTML = `
                    <img id="imagenCarrito" src="${producto.img}" alt="${producto.nombre}">
                    <p>${producto.nombre}</p>
                    <p>${producto.precio} | <span>${producto.precioOferta}</span></p>
                `;
                contenedor.appendChild(divItem);
            });
        }

        initializeCarousel();
    }

    function initializeCarousel() {
        items = document.querySelectorAll('.item');
        totalItems = items.length;
        console.log(`Total items: ${totalItems}`);
        updateItemsToShow();
        createIndicators();
        updateCarousel();
        attachEventListeners();
    }

    function updateItemsToShow() {
        const width = window.innerWidth;
        if (totalItems === 1) {
            itemsToShow = 1;
        } else if (totalItems === 2) {
            itemsToShow = 2;
        } else if (width <= 767) {
            itemsToShow = 1;
        } else if (width <= 1200) {
            itemsToShow = 2;
        } else {
            itemsToShow = 3;
        }
        updateItemsClass();
    }

    function updateItemsClass() {
        if (totalItems === 1) {
            carousel.classList.add('single-item');
            carousel.classList.remove('two-items');
        } else if (totalItems === 2) {
            carousel.classList.add('two-items');
            carousel.classList.remove('single-item');
        } else {
            carousel.classList.remove('single-item', 'two-items');
        }
    }

    function createIndicators() {
        indicatorsContainer.innerHTML = '';
        const totalIndicators = Math.ceil(totalItems / itemsToShow);
        for (let i = 0; i < totalIndicators; i++) {
            const indicator = document.createElement('span');
            indicator.classList.add('indicator');
            if (i === 0) {
                indicator.classList.add('active');
            }
            indicatorsContainer.appendChild(indicator);
        }
    }

    function updateIndicators() {
        const indicators = document.querySelectorAll('.indicator');
        indicators.forEach(indicator => {
            indicator.classList.remove('active');
        });

        const activeIndex = Math.floor(currentIndex / itemsToShow);
        if (indicators[activeIndex]) {
            indicators[activeIndex].classList.add('active');
        }
    }

    function updateCarousel() {
        const itemWidth = carousel.clientWidth / itemsToShow;
        carousel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
        updateIndicators();
    }

    function attachEventListeners() {
        leftNav.addEventListener('click', () => {
            currentIndex = (currentIndex === 0) ? totalItems - itemsToShow : currentIndex - 1;
            if (currentIndex < 0) currentIndex = 0;
            updateCarousel();
        });

        rightNav.addEventListener('click', () => {
            currentIndex = (currentIndex >= totalItems - itemsToShow) ? 0 : currentIndex + 1;
            if (currentIndex > totalItems - itemsToShow) currentIndex = totalItems - itemsToShow;
            updateCarousel();
        });

        window.addEventListener('resize', () => {
            updateItemsToShow();
            updateCarousel();
        });
    }

    // Cargar productos e inicializar el carrusel
    loadProducts();
});
