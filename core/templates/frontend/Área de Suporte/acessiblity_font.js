var tamanho_padrao = 16;
var tamanho_minimo = 12;
var tamanho_maximo = 22;
var tamanho_fonte = tamanho_padrao;

document.querySelector(".sb-ab-ft-maior").addEventListener("click", function(){
    if (tamanho_fonte < tamanho_maximo) {
        tamanho_fonte++;
        document.body.style.fontSize = tamanho_fonte + "px";
    }
});

document.querySelector(".sb-ab-ft-menor").addEventListener("click", function(){
    if (tamanho_fonte > tamanho_minimo) {
        tamanho_fonte--;
        document.body.style.fontSize = tamanho_fonte + "px";
    }
});

document.querySelector(".sb-ab-ft-normal").addEventListener("click", function(){
    tamanho_fonte = tamanho_padrao;
    document.body.style.fontSize = tamanho_padrao + "px";
});
