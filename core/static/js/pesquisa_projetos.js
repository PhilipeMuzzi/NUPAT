const data = [
{
    titulo:"NUPAT",
    descricao: "Nucleo de Projeto em Acessibilidade e Tecnologia",
},
{
    titulo:"Testando title one",
    descricao:"Este é um arquivo de teste",
},
{
    titulo:"hij",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
},
{
    titulo:"",
    descricao:"",
}
]
const projetos = document.querySelector(".projetos");
const pesquisa = document.querySelector("#pesquisa");

const displayData = data => {
    projetos.innerHTML = "";
    data.forEach(element => {
        projetos.innerHTML += `
        <article class="projetos">
                <nav class="card1">
                    <div class="image">
                        <img src="/Atendimento Virtual/img/afinal-para-que-serve-um-nucleo-de-pesquisa-em-uma-faculdade-1024x683.jpeg"
                            alt="Imagem do projeto">
                    </div>
                    <div class="conteudo">
                        <a href="">
                            <h1>${element.titulo}</h1>
                            <p>${element.descricao}</p>
                        </a>
                    </div>
                </nav>
                </article>`
    });
}
window.addEventListener("load", displayData.bind(null,data))
pesquisa.addEventListener("keyup", (element) => {
    const search = data.filter(i => i.titulo.toLocaleLowerCase().includes(element.target.value.toLocaleLowerCase()));
    displayData(search);
})