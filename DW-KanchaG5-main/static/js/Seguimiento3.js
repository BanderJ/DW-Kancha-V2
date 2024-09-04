document.addEventListener("DOMContentLoaded", function () {
    function setProgress(step) {
        const steps = document.querySelectorAll(".seguimiento-progress-step");
        const progress = document.getElementById("seguimiento-progress");

        steps.forEach((stepElem, index) => {
            if (index < step) {
                stepElem.classList.add("seguimiento-progress-step-active");
            } else {
                stepElem.classList.remove("seguimiento-progress-step-active");
            }
        });

        const activeSteps = document.querySelectorAll(".seguimiento-progress-step-active");
        progress.style.width = ((activeSteps.length - 1) / (steps.length - 1)) * 100 + "%";
    }

    // Llama a esta función con el número del paso que quieres activar (empezando desde 0)
    setProgress(3); // Esto activará el segundo punto y moverá la barra de progreso a la mitad
});
