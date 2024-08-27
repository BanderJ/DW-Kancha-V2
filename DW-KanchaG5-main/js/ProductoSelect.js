document.querySelectorAll('.thumbnail-item img').forEach(item => {
    item.addEventListener('click', event => {
        const mainImage = document.getElementById('mainImage');
        const newSrc = event.target.getAttribute('src');
        mainImage.src = newSrc;
    });
});

document.querySelectorAll('.thumbnail-item img').forEach(item => {
    item.addEventListener('click', event => {
        const mainImage = document.getElementById('mainImage2');
        const newSrc = event.target.getAttribute('src');
        mainImage.src = newSrc;
    });
});
