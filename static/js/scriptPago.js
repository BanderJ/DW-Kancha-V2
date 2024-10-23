document.getElementById('btn1').addEventListener('click', function () {
  
    document.getElementById('collapseOne').classList.remove('show');
    document.getElementById('collapseTwo').classList.add('show');
    document.getElementById('toggleOne').classList.remove('d-none');
    updateProgress(1);
  
});

document.getElementById('btn2').addEventListener('click', function () {
    document.getElementById('collapseTwo').classList.remove('show');
    document.getElementById('collapseThree').classList.add('show');
    document.getElementById('toggleTwo').classList.remove('d-none');
    updateProgress(2);
});

document.getElementById('btn3').addEventListener('click', function () {
    // Aquí puedes agregar la lógica para finalizar la compra
    alert('Compra finalizada!');
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


// -------------------------------------------------------------------------------------------------------------------------
