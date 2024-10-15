// window.addEventListener ('scroll', function(){
//     let scroll = document.querySelector ('.btn-voltaraoTopo')
//         scroll.classList.toggle ('active', window.scrollY > 450)
// })

function subiraoTopo (){
    window.scrollTo({
        top: 0,
        behavior: 'smooth'   
    })
}


