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


//script de noticias
function carregarNoticias() {
    const apiKey = '72dcdf0d822749b68d3d62b8bddcb653';
    const url = `https://newsapi.org/v2/top-headlines?country=br&apiKey=${apiKey}`;
  
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Não foi possível carregar as notícias.');
        }
        return response.json();
      })
      .then(data => {
        const noticiasLimitadas = data.articles.slice(0, 5);
        exibirNoticias(noticiasLimitadas);
      })
      .catch(error => {
        console.error('Erro ao carregar as notícias:', error);
        document.getElementById('noticias').innerHTML = '<p>Erro ao carregar as notícias. Verifique o console para mais detalhes.</p>';
      });
  }
  
  function exibirNoticias(articles) {
    let html = '';
  
    articles.forEach(article => {
      html += `
        <div class="noticia">
          <h4>${article.title}</h4>
          <a href="${article.url}" target="_blank">Leia mais</a>
        </div>
      `;
    });
  
    document.getElementById('noticias').innerHTML = html;
}
  
carregarNoticias();
