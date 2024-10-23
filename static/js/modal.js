// Selección de elementos
const modal = document.getElementById('confirmationModal');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');

// Mostrar el modal al hacer clic en el botón "Guardar"
document.querySelectorAll('.openModalButton').forEach(button => {
    button.addEventListener('click', () => {
        const formId = button.getAttribute('data-form-id');
        const form = document.getElementById(formId);
        
        // Verificar si el formulario es válido
        if (form.checkValidity()) {
            modal.style.display = 'block'; // Muestra el modal si el formulario es válido
        } else {
            form.reportValidity(); // Muestra mensajes de error de validación en caso de que haya campos vacíos
        }
        
        // Almacenar el ID del formulario en el modal para el envío
        modal.setAttribute('data-form-id', formId);
    });
});

// Confirmar acción y enviar el formulario
confirmButton.addEventListener('click', () => {
    const formId = modal.getAttribute('data-form-id');
    document.getElementById(formId).submit(); // Envía el formulario correspondiente
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
