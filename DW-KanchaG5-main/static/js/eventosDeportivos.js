document.addEventListener('DOMContentLoaded', function() {
    const proximosTab = document.getElementById('proximos-tab');
    const pasadosTab = document.getElementById('pasados-tab');
    const proximosContent = document.getElementById('proximos');
    const pasadosContent = document.getElementById('pasados');

    proximosTab.addEventListener('click', function() {
        proximosTab.classList.add('active');
        pasadosTab.classList.remove('active');
        proximosContent.style.display = 'block';
        pasadosContent.style.display = 'none';
    });

    pasadosTab.addEventListener('click', function() {
        pasadosTab.classList.add('active');
        proximosTab.classList.remove('active');
        proximosContent.style.display = 'none';
        pasadosContent.style.display = 'block';
    });

    const monthContainers = document.querySelectorAll('.month-container');
    monthContainers.forEach(container => {
        container.addEventListener('click', function() {
            const eventDetails = container.querySelector('.event-details');
            if (eventDetails.style.display === 'none' || eventDetails.style.display === '') {
                eventDetails.style.display = 'block';
            } else {
                eventDetails.style.display = 'none';
            }
        });
    });
});