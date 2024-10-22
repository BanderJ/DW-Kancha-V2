// Selección de elementos
const modal = document.getElementById('confirmationModal');
const openModalButton = document.getElementById('openModalButton');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');

// Mostrar el modal al hacer clic en el botón "Guardar"
openModalButton.addEventListener('click', () => {
  modal.style.display = 'block';
});

// Confirmar acción y enviar el formulario
confirmButton.addEventListener('click', () => {
  document.getElementById('categoriaForm').submit(); // Envía el formulario
});

// Cancelar la acción y cerrar el modal
cancelButton.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Cerrar el modal si se hace clic fuera del contenido
window.addEventListener('click', (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});
