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


// função da acessibilidade (aumentar a fonte)

var tamanho_padrao = 16;
var tamanho_maximo = 18; 
var tamanho_minimo = 14; 
var tamanho_fonte = tamanho_padrao;

// Save font size to localStorage
function salvarTamanhoFonte(tamanho) {
    localStorage.setItem('nupat-tamanho-fonte', tamanho);
}

document.querySelector(".sb-ab-ft-maior").addEventListener("click", function(){
    if (tamanho_fonte < tamanho_maximo) {
        tamanho_fonte++;
        document.body.style.fontSize = tamanho_fonte + "px";
        salvarTamanhoFonte(tamanho_fonte);
    }
});

document.querySelector(".sb-ab-ft-menor").addEventListener("click", function(){
    if (tamanho_fonte > tamanho_minimo) {
        tamanho_fonte--;
        document.body.style.fontSize = tamanho_fonte + "px";
        salvarTamanhoFonte(tamanho_fonte);
    }
});

document.querySelector(".sb-ab-ft-normal").addEventListener("click", function(){
    tamanho_fonte = tamanho_padrao;
    document.body.style.fontSize = tamanho_padrao + "px";
    salvarTamanhoFonte(tamanho_fonte);
});

// Apply saved font size on page load
function aplicarTamanhoFonteAoCarregar() {
    const tamanhoSalvo = localStorage.getItem('nupat-tamanho-fonte');
    if (tamanhoSalvo) {
        tamanho_fonte = parseInt(tamanhoSalvo, 10);
        document.body.style.fontSize = tamanho_fonte + "px";
    }
}

aplicarTamanhoFonteAoCarregar();

function mudarTema(tema) {
    if (tema === 'escuro') {
        document.body.classList.add('dark-mode');
        localStorage.setItem('nupat-tema', 'escuro');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('nupat-tema', 'claro');
    }
}

function aplicarTemaAoCarregar() {
    const temaSalvo = localStorage.getItem('nupat-tema');
    if (temaSalvo === 'escuro') {
        document.body.classList.add('dark-mode');
    }
}

aplicarTemaAoCarregar();
