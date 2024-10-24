// Selección de elementos
const modal = document.getElementById('confirmationModal');
const errorModal = document.getElementById('errorModal');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');
const errorMessage = document.getElementById('errorMessage');
const closeErrorButton = document.getElementById('closeErrorButton');
const openModalButtons = document.querySelectorAll('.openModalButton');

// Función para validar el formulario
function validateForm(form) {
    const imagenPrincipal = form.querySelector('input[name="imagenPrincipal"]').files.length;
    const imagenesSecundarias = form.querySelector('input[name="imagenesSecundarias"]').files.length;
    const precio = form.querySelector('input[name="precio"]').value;
    const stock = form.querySelector('input[name="stock"]').value;
    const idModelo = form.querySelector('select[name="idModelo"]').value;
    const idTalla = form.querySelector('select[name="idTalla"]').value;
    const idGenero = form.querySelector('select[name="idGenero"]').value;
    const idTipo = form.querySelector('select[name="idTipo"]').value;
    const descripcion = form.querySelector('textarea[name="descripcion"]').value;
    const colores = form.querySelector('select[name="colores"]').selectedOptions.length;
    const categorias = form.querySelector('select[name="categorias"]').selectedOptions.length;

    let errors = [];

    // Verificar que todos los campos estén completos y válidos
    if (imagenPrincipal === 0) errors.push("Debes cargar una imagen principal.");
    if (imagenesSecundarias !== 3) errors.push("Debes cargar exactamente 3 imágenes secundarias.");
    if (!precio) errors.push("El campo precio es obligatorio.");
    if (!stock) errors.push("El campo stock es obligatorio.");
    if (!idModelo) errors.push("Debes seleccionar un modelo.");
    if (!idTalla) errors.push("Debes seleccionar una talla.");
    if (!idGenero) errors.push("Debes seleccionar un género.");
    if (!idTipo) errors.push("Debes seleccionar un tipo de producto.");
    if (!descripcion) errors.push("El campo descripción es obligatorio.");
    if (colores === 0) errors.push("Debes seleccionar al menos un color.");
    if (categorias === 0) errors.push("Debes seleccionar al menos una categoría.");

    // Si hay errores, mostrar el mensaje en el modal de error
    if (errors.length > 0) {
        errorMessage.textContent = errors.join(' ');
        errorModal.style.display = 'block';
        return false;
    }

    return true; // El formulario es válido
}

// Mostrar el modal al hacer clic en "Guardar"
openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const formId = button.getAttribute('data-form-id');
        const form = document.getElementById(formId);

        // Verificar si el formulario es válido
        if (validateForm(form)) {
            modal.style.display = 'block'; // Muestra el modal si el formulario es válido
        }
    });
});

// Confirmar acción y enviar el formulario
confirmButton.addEventListener('click', () => {
    const formId = document.querySelector('.openModalButton').getAttribute('data-form-id');
    document.getElementById(formId).submit(); // Envía el formulario correspondiente
});

// Cancelar la acción y cerrar los modales
cancelButton.addEventListener('click', () => {
    modal.style.display = 'none';
});

closeErrorButton.addEventListener('click', () => {
    errorModal.style.display = 'none';
});

// Cerrar el modal si se hace clic fuera del contenido
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
    if (event.target === errorModal) {
        errorModal.style.display = 'none';
    }
});
