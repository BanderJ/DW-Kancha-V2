// Selección de elementos
const modal = document.getElementById('confirmationModal');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');
let deleteFormId = ''; // Variable para almacenar el ID del formulario de eliminación

// Mostrar el modal al hacer clic en el botón "Eliminar"
document.querySelectorAll('.openModalButton').forEach(button => {
    button.addEventListener('click', () => {
        const form = button.closest('form');

        if (form && form.classList.contains('delete-form')) {
            deleteFormId = button.closest('form').getAttribute('data-id');
            modal.querySelector('h2').innerText = '¿Estás seguro de eliminar este producto?';
            modal.querySelector('p').innerText = 'Esta acción no se puede deshacer.';
            confirmButton.style.display = 'block'; // Mostrar el botón de confirmar
            modal.style.display = 'block';
        }
    });
});

// Confirmar acción y enviar el formulario de eliminación
confirmButton.addEventListener('click', () => {
    if (deleteFormId) {
        // Enviar solicitud de eliminación mediante AJAX
        const formData = new FormData();
        formData.append("id", deleteFormId);
        
        fetch("/eliminar_producto", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "error") {
                // Mostrar mensaje de error en el modal
                modal.querySelector('h2').innerText = 'Error al eliminar';
                modal.querySelector('p').innerText = data.message;
                confirmButton.style.display = 'none'; // Ocultar el botón de eliminar
            } else {
                // Si se elimina correctamente, recargar la página
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error al eliminar el producto:', error);
        });

        deleteFormId = ''; // Reinicia la variable después de usarla
    }
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
