// // Selección de elementos
// const modal = document.getElementById('confirmationModal');
// const confirmButton = document.getElementById('confirmButton');
// const cancelButton = document.getElementById('cancelButton');

// // Mostrar el modal al hacer clic en el botón "Guardar"
// document.querySelectorAll('.openModalButton').forEach(button => {
//     button.addEventListener('click', () => {
//         const formId = button.getAttribute('data-form-id');
//         const form = document.getElementById(formId);
        
//         // Verificar si el formulario es válido
//         if (form.checkValidity()) {
//             modal.style.display = 'block'; // Muestra el modal si el formulario es válido
//         } else {
//             form.reportValidity(); // Muestra mensajes de error de validación en caso de que haya campos vacíos
//         }
        
//         // Almacenar el ID del formulario en el modal para el envío
//         modal.setAttribute('data-form-id', formId);
//     });
// });

// // Confirmar acción y enviar el formulario
// confirmButton.addEventListener('click', () => {
//     const formId = modal.getAttribute('data-form-id');
//     document.getElementById(formId).submit(); // Envía el formulario correspondiente
// });

// // Cancelar la acción y cerrar el modal
// cancelButton.addEventListener('click', () => {
//     modal.style.display = 'none';
// });

// // Cerrar el modal si se hace clic fuera del contenido
// window.addEventListener('click', (event) => {
//     if (event.target === modal) {
//         modal.style.display = 'none';
//     }
// });


// // Selección de elementos
// const modal = document.getElementById('confirmationModal');
// const confirmButton = document.getElementById('confirmButton');
// const cancelButton = document.getElementById('cancelButton');

// // Variable para almacenar el ID del formulario de eliminación
// let deleteFormId = '';

// // Mostrar el modal al hacer clic en el botón "Guardar" o "Eliminar"
// document.querySelectorAll('.openModalButton').forEach(button => {
//     button.addEventListener('click', () => {
//         // Verificar si es un botón de eliminación o de guardar
//         if (button.closest('form').classList.contains('delete-form')) {
//             deleteFormId = button.closest('form').getAttribute('data-id');
//             modal.querySelector('h2').innerText = '¿Estás seguro de eliminar esta marca?';
//             modal.querySelector('p').innerText = 'Esta acción no se puede deshacer.';
//             modal.style.display = 'block'; // Muestra el modal
//         } else {
//             const formId = button.getAttribute('data-form-id');
//             const form = document.getElementById(formId);
            
//             // Verificar si el formulario es válido
//             if (form.checkValidity()) {
//                 modal.style.display = 'block'; // Muestra el modal si el formulario es válido
//                 modal.querySelector('h2').innerText = '¿Estás seguro de guardar?';
//                 modal.querySelector('p').innerText = 'Por favor, confirme su acción.';
//             } else {
//                 form.reportValidity(); // Muestra mensajes de error de validación
//             }
            
//             // Almacenar el ID del formulario en el modal para el envío
//             modal.setAttribute('data-form-id', formId);
//         }
//     });
// });

// // Confirmar acción y enviar el formulario de eliminación o el de guardar
// confirmButton.addEventListener('click', () => {
//     if (deleteFormId) {
//         // Si hay un ID de formulario de eliminación, envía la solicitud de eliminación
//         document.querySelector(`.delete-form[data-id="${deleteFormId}"]`).submit();
//         deleteFormId = ''; // Reinicia la variable después de usarla
//     } else {
//         // Envío del formulario de guardar
//         const formId = modal.getAttribute('data-form-id');
//         document.getElementById(formId).submit();
//     }
// });

// // Cancelar la acción y cerrar el modal
// cancelButton.addEventListener('click', () => {
//     modal.style.display = 'none';
// });

// // Cerrar el modal si se hace clic fuera del contenido
// window.addEventListener('click', (event) => {
//     if (event.target === modal) {
//         modal.style.display = 'none';
//     }
// });


// // Selección de elementos
// const modal = document.getElementById('confirmationModal');
// const confirmButton = document.getElementById('confirmButton');
// const cancelButton = document.getElementById('cancelButton');
// let deleteFormId = ''; // Variable para almacenar el ID del formulario de eliminación

// // Mostrar el modal al hacer clic en el botón "Guardar" o "Eliminar"
// document.querySelectorAll('.openModalButton').forEach(button => {
//     button.addEventListener('click', () => {
//         if (button.closest('form').classList.contains('delete-form')) {
//             deleteFormId = button.closest('form').getAttribute('data-id');
//             modal.querySelector('h2').innerText = '¿Estás seguro de eliminar esta marca?';
//             modal.querySelector('p').innerText = 'Esta acción no se puede deshacer.';
//             modal.style.display = 'block';
//         } else {
//             const formId = button.getAttribute('data-form-id');
//             const form = document.getElementById(formId);
//             if (form.checkValidity()) {
//                 modal.style.display = 'block';
//                 modal.querySelector('h2').innerText = '¿Estás seguro de guardar?';
//                 modal.querySelector('p').innerText = 'Por favor, confirme su acción.';
//             } else {
//                 form.reportValidity(); 
//             }
//             modal.setAttribute('data-form-id', formId);
//         }
//     });
// });

// // Confirmar acción y enviar el formulario de eliminación o el de guardar
// confirmButton.addEventListener('click', () => {
//     if (deleteFormId) {
//         // Enviar solicitud de eliminación mediante AJAX
//         const formData = new FormData();
//         formData.append("id", deleteFormId);
        
//         fetch("/eliminar_marca", {
//             method: "POST",
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === "error") {
//                 // Mostrar mensaje de error en el modal
//                 modal.querySelector('h2').innerText = 'Error al eliminar';
//                 modal.querySelector('p').innerText = data.message;
//             } else {
//                 // Si se elimina correctamente, recargar la página
//                 window.location.reload();
//             }
//         })
//         .catch(error => {
//             console.error('Error al eliminar la marca:', error);
//         });

//         deleteFormId = ''; // Reinicia la variable después de usarla
//     } else {
//         const formId = modal.getAttribute('data-form-id');
//         document.getElementById(formId).submit();
//     }
// });

// // Cancelar la acción y cerrar el modal
// cancelButton.addEventListener('click', () => {
//     modal.style.display = 'none';
// });

// // Cerrar el modal si se hace clic fuera del contenido
// window.addEventListener('click', (event) => {
//     if (event.target === modal) {
//         modal.style.display = 'none';
//     }
// });

// // Selección de elementos
// const modal = document.getElementById('confirmationModal');
// const confirmButton = document.getElementById('confirmButton');
// const cancelButton = document.getElementById('cancelButton');
// let deleteFormId = ''; // Variable para almacenar el ID del formulario de eliminación

// // Mostrar el modal al hacer clic en el botón "Guardar" o "Eliminar"
// document.querySelectorAll('.openModalButton').forEach(button => {
//     button.addEventListener('click', () => {
//         if (button.closest('form').classList.contains('delete-form')) {
//             deleteFormId = button.closest('form').getAttribute('data-id');
//             modal.querySelector('h2').innerText = '¿Estás seguro de eliminar esta marca?';
//             modal.querySelector('p').innerText = 'Esta acción no se puede deshacer.';
//             confirmButton.style.display = 'block'; // Mostrar el botón de confirmar
//             modal.style.display = 'block';
//         } else {
//             const formId = button.getAttribute('data-form-id');
//             const form = document.getElementById(formId);
//             if (form.checkValidity()) {
//                 modal.style.display = 'block';
//                 modal.querySelector('h2').innerText = '¿Estás seguro de guardar?';
//                 modal.querySelector('p').innerText = 'Por favor, confirme su acción.';
//             } else {
//                 form.reportValidity(); 
//             }
//             modal.setAttribute('data-form-id', formId);
//         }
//     });
// });

// // Confirmar acción y enviar el formulario de eliminación o el de guardar
// confirmButton.addEventListener('click', () => {
//     if (deleteFormId) {
//         // Enviar solicitud de eliminación mediante AJAX
//         const formData = new FormData();
//         formData.append("id", deleteFormId);
        
//         fetch("/eliminar_marca", {
//             method: "POST",
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === "error") {
//                 // Mostrar mensaje de error en el modal
//                 modal.querySelector('h2').innerText = 'Error al eliminar';
//                 modal.querySelector('p').innerText = data.message;
//                 confirmButton.style.display = 'none'; // Ocultar el botón de eliminar
//             } else {
//                 // Si se elimina correctamente, recargar la página
//                 window.location.reload();
//             }
//         })
//         .catch(error => {
//             console.error('Error al eliminar la marca:', error);
//         });

//         deleteFormId = ''; // Reinicia la variable después de usarla
//     } else {
//         const formId = modal.getAttribute('data-form-id');
//         document.getElementById(formId).submit();
//     }
// });

// // Cancelar la acción y cerrar el modal
// cancelButton.addEventListener('click', () => {
//     modal.style.display = 'none';
// });

// // Cerrar el modal si se hace clic fuera del contenido
// window.addEventListener('click', (event) => {
//     if (event.target === modal) {
//         modal.style.display = 'none';
//     }
// });

// Selección de elementos
const modal = document.getElementById('confirmationModal');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');
let deleteFormId = ''; // Variable para almacenar el ID del formulario de eliminación

// Mostrar el modal al hacer clic en el botón "Guardar" o "Eliminar"
document.querySelectorAll('.openModalButton').forEach(button => {
    button.addEventListener('click', () => {
        const form = button.closest('form');

        if (form && form.classList.contains('delete-form')) {
            deleteFormId = button.closest('form').getAttribute('data-id');
            modal.querySelector('h2').innerText = '¿Estás seguro de eliminar esta marca?';
            modal.querySelector('p').innerText = 'Esta acción no se puede deshacer.';
            confirmButton.style.display = 'block'; // Mostrar el botón de confirmar
            modal.style.display = 'block';
        } else {
            const formId = button.getAttribute('data-form-id');
            const form = document.getElementById(formId);

            // Verificar si el formulario es válido
            if (form && form.checkValidity()) {
                modal.querySelector('h2').innerText = '¿Estás seguro de guardar?';
                modal.querySelector('p').innerText = 'Por favor, confirme su acción.';
                confirmButton.style.display = 'block'; // Mostrar el botón de confirmar
                modal.style.display = 'block';
            } else if (form) {
                form.reportValidity(); // Mostrar mensajes de error de validación
            }

            modal.setAttribute('data-form-id', formId);
        }
    });
});

// Confirmar acción y enviar el formulario de eliminación o el de guardar
confirmButton.addEventListener('click', () => {
    if (deleteFormId) {
        // Enviar solicitud de eliminación mediante AJAX
        const formData = new FormData();
        formData.append("id", deleteFormId);
        
        fetch("/eliminar_marca", {
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
            console.error('Error al eliminar la marca:', error);
        });

        deleteFormId = ''; // Reinicia la variable después de usarla
    } else {
        const formId = modal.getAttribute('data-form-id');
        const form = document.getElementById(formId);
        form.submit(); // Envía el formulario correspondiente para guardar
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


