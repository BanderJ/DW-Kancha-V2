document.addEventListener('DOMContentLoaded', function () {
    fetch('../Json/productos.json')
        .then(response => response.json())
        .then(data => {
            const productContainer = document.getElementById('productContainer');
            const filtersContainer = document.getElementById('filtersContainer');
            const toggleButton = document.getElementById('toggleFilters');
            const closeFiltersButton = document.getElementById('closeFilters');
            const clearFiltersButton = document.getElementById('clearFilters');
            const precioRange = document.getElementById('precioRange');
            const precioValue = document.getElementById('precioValue');
            const sortBy = document.getElementById('sortBy');
            const tituloSeccion = document.getElementById('tituloSeccion');
            const paginationContainer = document.querySelector('.pagination');

            const maxProductsPerPage = 12;
            let currentPage = 1;
            let filteredProducts = data;

            function renderProducts(products, page = 1) {
                productContainer.innerHTML = '';
                const startIndex = (page - 1) * maxProductsPerPage;
                const endIndex = page * maxProductsPerPage;
                products.slice(startIndex, endIndex).forEach(product => {
                    const productCard = `
                        <div class="col-4 p-0 px-1 extrac product-card col-md-4 col-lg-3 col-sm-6 col-6">
                            <div class="heart-container">
                                <img src="../img/corazonVacio.svg" class="heart-icon" alt="heart">
                            </div>
                            <a href="${product.id}" target="_blank"><img class="img-fluid pb-2" src="${product.imagen}" alt="${product.nombre}"></a>
                            <div class="row">
                                <div class="col-12 mb-1">
                                    <p>${product.nombre}</p>
                                </div>
                                <div class="col-6 pe-0">
                                    <p class="text-start"><b>S/ ${product.precio.toFixed(2)}</b></p>
                                </div>
                                <div class="col-6 ps-0">
                                    <p class="text-end"><b><s>S/ ${product.precio.toFixed(2)}</s></b></p>
                                </div>
                                <div class="col-8 pe-0 my-1">
                                    <p class="text-start l-rojo-k"><b>S/ ${product.precioKancha.toFixed(2)}</b></p>
                                </div>
                                <div class="col-4 ps-0 d-flex justify-content-end my-1">
                                    <img class="klo" src="../img/logo_kancha_club.svg" alt="Logo pequeño">
                                </div>
                            </div>
                        </div>
                    `;
                    productContainer.insertAdjacentHTML('beforeend', productCard);
                });

                document.querySelectorAll('.heart-icon').forEach((icon, index) => {
                    icon.addEventListener('click', function (event) {
                        event.preventDefault();
                        const product = products[startIndex + index];
                        if (this.src.includes('orazonVacio.svg')) {
                            this.src = '../img/corazonLleno.svg';
                            // Agregar producto a favoritos (aquí puedes implementar tu lógica de favoritos)
                        } else {
                            this.src = '../img/corazonVacio.svg';
                            // Eliminar producto de favoritos (aquí puedes implementar tu lógica de favoritos)
                        }
                    });
                });
            }

            function updatePagination(totalProducts) {
                paginationContainer.innerHTML = '';
                const totalPages = Math.ceil(totalProducts / maxProductsPerPage);
                for (let i = 1; i <= totalPages; i++) {
                    const pageItem = document.createElement('li');
                    pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
                    pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                    pageItem.addEventListener('click', function (event) {
                        event.preventDefault();
                        currentPage = i;
                        renderProducts(filteredProducts, currentPage);
                        updatePagination(filteredProducts.length);
                    });
                    paginationContainer.appendChild(pageItem);
                }
            }

            function updateTitle() {
                const selectedDeporte = document.querySelector('input[name="deporte"]:checked')?.value;
                if (selectedDeporte) {
                    tituloSeccion.textContent = `Zapatillas para ${selectedDeporte}`;
                } else {
                    tituloSeccion.textContent = 'Zapatillas';
                }
            }

            function applyFiltersAndSort() {
                const selectedFilters = {
                    genero: document.querySelector('input[name="genero"]:checked')?.value,
                    deporte: document.querySelector('input[name="deporte"]:checked')?.value,
                    precio: parseInt(precioRange.value),
                    color: document.querySelector('input[name="color"]:checked')?.value,
                    marca: document.querySelector('input[name="marca"]:checked')?.value,
                };

                filteredProducts = data.filter(product => {
                    return (!selectedFilters.genero || product.genero === selectedFilters.genero)
                        && (!selectedFilters.deporte || product.deporte === selectedFilters.deporte)
                        && (!selectedFilters.color || product.color === selectedFilters.color)
                        && (!selectedFilters.marca || product.marca === selectedFilters.marca)
                        && (!selectedFilters.precio || product.precio <= selectedFilters.precio);
                });

                const sortValue = sortBy.value;
                if (sortValue === 'precio-asc') {
                    filteredProducts.sort((a, b) => a.precio - b.precio);
                } else if (sortValue === 'precio-desc') {
                    filteredProducts.sort((a, b) => b.precio - a.precio);
                }

                currentPage = 1; // Reset to the first page when filters are applied
                renderProducts(filteredProducts, currentPage);
                updatePagination(filteredProducts.length);
                updateTitle();
            }

            renderProducts(data, currentPage);
            updatePagination(data.length);
            updateTitle();

            // Toggle filtros para dispositivos grandes
            toggleButton.addEventListener('click', function () {
                if (window.innerWidth <= 990) {
                    filtersContainer.classList.add('show');
                } else {
                    filtersContainer.classList.toggle('hidden');
                    const productContainerCol = productContainer.parentNode;
                    if (filtersContainer.classList.contains('hidden')) {
                        productContainerCol.classList.remove('col-md-9');
                        productContainerCol.classList.add('col-md-12');
                    } else {
                        productContainerCol.classList.remove('col-md-12');
                        productContainerCol.classList.add('col-md-9');
                    }
                }
            });

            // Cerrar filtros en dispositivos móviles
            closeFiltersButton.addEventListener('click', function () {
                filtersContainer.classList.remove('show');
            });

            // Limitar selección de filtros a uno por sección y aplicar filtros
            document.querySelectorAll('.form-check-input').forEach(input => {
                input.addEventListener('change', function () {
                    applyFiltersAndSort();
                });
            });

            // Actualizar rango de precio
            precioRange.addEventListener('input', function () {
                precioValue.textContent = this.value;
                applyFiltersAndSort();
            });

            // Ordenar productos
            sortBy.addEventListener('change', function () {
                applyFiltersAndSort();
            });

            // Eliminar todos los filtros
            clearFiltersButton.addEventListener('click', function () {
                document.querySelectorAll('.form-check-input').forEach(input => {
                    input.checked = false;
                });
                precioRange.value = 2000;
                precioValue.textContent = 2000;
                applyFiltersAndSort();
            });
        })
        .catch(error => console.error('Error al cargar los productos:', error));
});