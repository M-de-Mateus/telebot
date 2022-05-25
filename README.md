# Telebot 1.0

Criei esse bot com o objetivo de ampliar meus conhecimentos em Python, venho estudando essa linguagem há um tempo e queria saber até onde poderia chegar com ela. 
O bot, que chamo de Zeta, foi meu primeiro grande projeto solo, o que me fez por em prática muitos conhecimentos e aprender muitas outras coisas. A principio não pretendo atualizar esse código, irei buscar outros projetos, porém sigo ciente de que há muito em que melhorar e maneiras melhores de escrever algumas funções.

Zeta foi inspirado em um bot que vi no whatsapp uma vez, era desenvolvido baseado em uma biblioteca de node.js, criei o Zeta com funções parecidas pois meus amigos acharam bem divertidas. 

**Atenção:**

_Embora alguns códigos sejam citados, o objetivo desse README.md não é o de ensinar a utilizar a API do Telegram._

## Comandos

Zeta possui vários comandos que podem ser usados no chat do telegram, eles estão listados aqui: [Comandos](botfunc/comandosgerais.txt)

## Funções

### /pesquisa ([imagesearch](botfunc/imagemsearch.py))

Decidi criar algumas funções legais para o Zeta, a primeira delas era a de procurar imagens e depois retorná-las para o chat do telegram.

Para isso utilizei o Selenium para pesquisar imagens no google. O código acessa a página do google passando o termo da pesquisa por url, após isso ele percorre os containers da página e baixa 10 imagens (valor ajustável) para meu computador, as armazenando na pasta 'image'. Antes de baixar cada imagem o Zeta espera 10 segundos para que ela carregue na sua máxima resolução, caso esse tempo acabe o Zeta ignora a imagem e passa para a próxima. Após isso, o Zeta sorteia uma imgem aleatória dentre as 10 que pesquisou e a retorna no chat respondendo o usuário que deu o comando. Por fim, ele exclui as imagens para que não pesem no meu computador.

### /anime _1_ ([imagesearch](botfunc/imagemsearch.py))

Esse comando foi escrito em duas partes. Ele retorna a imagem de um anime pesquisado juntamente com o Título, Tipo (anime ou OVA), Popularidade e Sinopse do anime.
A primeira parte do comando é responsável por pegar a imagem da pesquisa do site [Kitsu](https://kitsu.io/anime)

### /clima ([Clima](botfunc/clima.py))

Criei essa classe para retornar o clima de uma cidade, bairro ou municipio. Para isso utilizo uma API JSON do Open Weather Map e extraio todas as informações necessárias do objeto JSON que minha requisição retorna. Essa classe foi escrita com diversas funções que poderiam se resumir em uma, foi criada dessa forma porque achei que poderia usar essas funções separadamente em algum momento.

