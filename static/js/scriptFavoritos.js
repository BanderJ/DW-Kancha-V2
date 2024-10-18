const productos = [
    {
      id: "#1",
      imagen: `${STATIC_URL}img/foto (112).avif`,
      nombre: "F50 Elite",
      marca: "Adidas",
      precio: 1709.90,
      precioKancha: 1679.90,
      deporte: "Fútbol",
      genero: "Masculino",
      color: "Blanco",
      tipo: "Chimpunes"
    },
    {
      id: "#2",
      imagen: `${STATIC_URL}img/foto (27).avif`,
      nombre: "KD17 'Sunrise'",
      marca: "Puma",
      precio: 309.00,
      precioKancha: 289.00,
      deporte: "Fútbol",
      genero: "Masculino",
      color: "Negro",
      tipo: "Chimpunes"
    },
    {
      id: "#3",
      imagen: `${STATIC_URL}img/foto (30).avif`,
      nombre: "KD1zxc7 'Sunrise'",
      marca: "Puma",
      precio: 309.00,
      precioKancha: 289.00,
      deporte: "Fútbol",
      genero: "Masculino",
      color: "Rosado",
      tipo: "Chimpunes"
    }
  ];
  
  const favoritosContainer = document.getElementById('losfavoritos');
  
  // Insertar los productos en el carrusel
  productos.forEach(producto => {
    const item = document.createElement('div');
    item.classList.add('item');
  
    item.innerHTML = `
      <img src="${producto.imagen}" alt="${producto.nombre}">
      <h5>${producto.nombre}</h5>
      <p>Marca: ${producto.marca}</p>
      <p>Deporte: ${producto.deporte}</p>
      <p>Género: ${producto.genero}</p>
      <p>Color: ${producto.color}</p>
      <p>Precio: <span class="price">S/${producto.precio}</span> 
        <span class="kancha-price">S/${producto.precioKancha}</span></p>
    `;
    favoritosContainer.appendChild(item);
  });
  
  // Control del carrusel
  let currentPosition = 0;
  
  const updateCarousel = () => {
    const items = document.querySelector('.items');
    items.style.transform = `translateX(${-currentPosition * 100}%)`;
  };
  
  document.getElementById('prevButton').addEventListener('click', () => {
    if (currentPosition > 0) {
      currentPosition--;
      updateCarousel();
    }
  });
  
  document.getElementById('nextButton').addEventListener('click', () => {
    if (currentPosition < productos.length - 1) {
      currentPosition++;
      updateCarousel();
    }
  });
  