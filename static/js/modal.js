// Selección de elementos
const modal = document.getElementById('customModal');
const closeModalButton = document.querySelector('.close-btn');

// Lógica para abrir el modal después del envío del formulario
document.getElementById('categoriaForm').addEventListener('submit', function (event) {
  event.preventDefault(); // Evita el envío normal del formulario para mostrar el modal

  // Aquí puedes realizar un fetch o llamada AJAX para enviar el formulario si lo deseas
  modal.style.display = 'block'; // Mostrar el modal

  // Simulación del envío con éxito (opcional: reemplazar con lógica real)
  setTimeout(() => {
    this.submit(); // Envía el formulario después de mostrar el modal
  }, 2000);
});

// Cerrar el modal al hacer clic en la "X"
closeModalButton.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Cerrar el modal si se hace clic fuera del contenido
window.addEventListener('click', (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});
