document.addEventListener("DOMContentLoaded", function () {
    const formsMas = document.querySelectorAll("form[action*='actualizar_cantidad_mas']");
    const formsMenos = document.querySelectorAll("form[action*='actualizar_cantidad_menos']");
  
    // Añadir evento de submit para el botón de "incrementar" cantidad
    formsMas.forEach(form => {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        actualizarCantidad(form, 'mas');
      });
    });
  
    // Añadir evento de submit para el botón de "disminuir" cantidad
    formsMenos.forEach(form => {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        actualizarCantidad(form, 'menos');
      });
    });
  
    // Función para manejar la actualización de la cantidad
    function actualizarCantidad(form, tipo) {
      const formData = new FormData(form);
      const url = form.action;
  
      // Llamada a la API para actualizar la cantidad
      fetch(url, {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(result => {
          if (result.error) {
            // Mostrar el modal de error con el mensaje recibido
            mostrarModalError(result.error);
          } else {
            // Actualizamos la cantidad en el DOM
            const cantidadElem = tipo === 'mas' ? form.previousElementSibling : form.nextElementSibling;
            cantidadElem.textContent = result.nueva_cantidad;
  
            // Actualizar subtotal si es necesario
            const precioElem = form.closest('tr').querySelector('.precio');
            const subtotalElem = form.closest('tr').querySelector('.subtotal');
            const nuevoSubtotal = result.nueva_cantidad * parseFloat(precioElem.textContent);
            subtotalElem.textContent = nuevoSubtotal.toFixed(2); // Actualiza el subtotal
          }
        })
        .catch(error => {
          console.error("Error al actualizar la cantidad:", error);
        });
    }
  
    // Función para mostrar el modal con el mensaje de error
    function mostrarModalError(mensaje) {
      const modalBody = document.getElementById("modalErrorCantidadBody");
      modalBody.textContent = mensaje; // Insertar el mensaje en el modal
  
      const modal = new bootstrap.Modal(document.getElementById("modalErrorCantidad"));
      modal.show(); // Mostrar el modal
    }
  });
  