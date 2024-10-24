document.getElementById('btn1').addEventListener('click', function () {
  if (validateSection('collapseOne')) {
    document.getElementById('collapseOne').classList.remove('show');
    document.getElementById('collapseTwo').classList.add('show');
    document.getElementById('toggleOne').classList.remove('d-none');
    updateProgress(1);
  }
});

document.getElementById('btn2').addEventListener('click', function () {
  if (validateSection('collapseTwo')) {
    document.getElementById('collapseTwo').classList.remove('show');
    document.getElementById('collapseThree').classList.add('show');
    document.getElementById('toggleTwo').classList.remove('d-none');
    updateProgress(2);
  }
});

document.getElementById('btn3').addEventListener('click', function () {
  if (validateSection('collapseThree')) {

  }
});

function updateProgress(step) {
  const progress = document.getElementById('progress');
  const progressSteps = document.querySelectorAll('.progress-step');
  progressSteps.forEach((stepEl, idx) => {
    if (idx <= step) {
      stepEl.classList.add('progress-step-active');
    } else {
      stepEl.classList.remove('progress-step-active');
    }
  });
  progress.style.width = ((step) / (progressSteps.length - 1)) * 100 + '%';
}

function validateSection(sectionId) {
  const section = document.getElementById(sectionId);
  const inputs = section.querySelectorAll('input');
  let isValid = true;

  inputs.forEach(input => {
    if (input.value.trim() === '') {
      input.style.borderColor = 'red';
      isValid = false;
    } else {
      input.style.borderColor = '';
      if (isNumericField(input) && !isValidNumber(input.value)) {
        input.style.borderColor = 'red';
        isValid = false;
      } else {
        input.style.borderColor = '';
      }
    }
  });

  return isValid;
}

function isNumericField(input) {
  const numericFields = ['dni', 'movil', 'ntarj', 'codeSeg', 'exp-month', 'exp-year'];
  return numericFields.includes(input.id);
}

function isValidNumber(value) {
  return /^\d+$/.test(value);
}

// Inicializar la barra de progreso
updateProgress(0);

// Eventos para ajustar la barra de progreso al abrir un acordeón
document.getElementById('collapseOne').addEventListener('shown.bs.collapse', function () {
  updateProgress(0);
});

document.getElementById('collapseTwo').addEventListener('shown.bs.collapse', function () {
  updateProgress(1);
});

document.getElementById('collapseThree').addEventListener('shown.bs.collapse', function () {
  updateProgress(2);
});


// Selección de elementos
const confirmationModal = document.getElementById('confirmationModal');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');

// Mostrar el modal al hacer clic en el botón "Finalizar compra"
document.querySelector('#btn3').addEventListener('click', (e) => {
    e.preventDefault();  // Evitar que el formulario se envíe inmediatamente
    confirmationModal.style.display = 'block';
});

// Confirmar la compra
confirmButton.addEventListener('click', () => {
    // Enviar el formulario de compra aquí
    document.querySelector('form').submit();
    confirmationModal.style.display = 'none';
});

// Cancelar la compra y cerrar el modal
cancelButton.addEventListener('click', () => {
    confirmationModal.style.display = 'none';
});



// Cerrar el modal si se hace clic fuera del contenido
window.addEventListener('click', (event) => {
    if (event.target === confirmationModal) {
      confirmationModal.style.display = 'none';
    }
});
