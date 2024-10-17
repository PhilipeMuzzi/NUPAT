let currentIndex = 0;

function moveCarousel(direction) {
    const carousel = document.querySelector('.photos');
    const items = document.querySelectorAll('.profilesec');
    const itemWidth = items[0].offsetWidth + 20;
    const totalItems = items.length;

    currentIndex += direction;

    if (currentIndex >= totalItems) {
        carousel.style.transition = 'none';
        currentIndex = 0;
        carousel.style.transform = `translateX(0px)`;
        setTimeout(() => {
            carousel.style.transition = 'transform 0.5s ease-in-out';
            carousel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
        }, 50); 
    } else if (currentIndex < 0) {
        carousel.style.transition = 'none';
        currentIndex = totalItems - 1;
        carousel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
        setTimeout(() => {
            carousel.style.transition = 'transform 0.5s ease-in-out';
            carousel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
        }, 50); 
    } else {
        carousel.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
    }
}

window.onload = () => {
    const carousel = document.querySelector('.photos');
    const items = document.querySelectorAll('.profilesec');
    const clone = carousel.innerHTML;
    carousel.innerHTML += clone;
    const itemWidth = items[0].offsetWidth + 20; 
    carousel.style.width = `${items.length * 2 * itemWidth}px`;
    carousel.style.transform = `translateX(0px)`;
};


document.querySelector('.sb-ab-ft-maior').addEventListener('click', () => moveCarousel(1));
document.querySelector('.sb-ab-ft-menor').addEventListener('click', () => moveCarousel(-1));



/*Ativando função de voltar ao topo:*/
function subiraoTopo() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
/* encerrado */