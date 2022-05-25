# Telebot 1.0

Criei esse bot com o objetivo de ampliar meus conhecimentos em Python, venho estudando essa linguagem há um tempo e queria saber até onde poderia chegar com ela. 
O bot, que chamo de Zeta, foi meu primeiro grande projeto solo, o que me fez por em prática muitos conhecimentos e aprender muitas outras coisas. A principio não pretendo atualizar esse código, irei buscar outros projetos, porém sigo ciente de que há muito em que melhorar e maneiras melhores de escrever algumas funções.

Zeta foi inspirado em um bot que vi no whatsapp uma vez, era desenvolvido baseado em uma biblioteca de node.js, criei o Zeta com funções parecidas pois meus amigos acharam bem divertidas. 

**Atenção:**

_Embora alguns códigos sejam citados, o objetivo desse README.md não é o de ensinar a utilizar a API do Telegram._


## Sumário:

** 1. [Comandos](https://github.com/M-de-Mateus/telebot#comandos) **
** 2. [Funções](https://github.com/M-de-Mateus/telebot#funcoes) **

## Comandos

Zeta possui vários comandos que podem ser usados no chat do telegram, eles estão listados aqui: [Comandos](botfunc/comandosgerais.txt)

## Funções

### /comandos

Lê um arquivo .txt e envia uma mensagem que contem todos os comandos listados do bot.

### /pesquisa ([imagesearch](botfunc/imagemsearch.py))

Decidi criar algumas funções legais para o Zeta, a primeira delas era a de procurar imagens e depois retorná-las para o chat do telegram.

Para isso utilizei o `Selenium` para pesquisar imagens no google. O código acessa a página do google passando o termo da pesquisa por url, após isso ele percorre os containers da página e baixa 10 imagens (valor ajustável) para meu computador e as armazenando na pasta 'image'. Antes de baixar cada imagem o Zeta espera 10 segundos para que ela carregue na sua máxima resolução, caso esse tempo acabe o Zeta ignora a imagem e passa para a próxima. Após isso, o Zeta sorteia uma imgem aleatória dentre as 10 que pesquisou e a retorna no chat respondendo o usuário que deu o comando. Por fim, ele exclui as imagens para que não pesem no meu computador. Além de `Selenium`, também utilizo as bibliotecas `bs4`, `requests`, `os`, `time` e `random`.

_Uma possível melhora no desempenho dessa função seria fazer ela escolher randomicamente o link da imagem que iria baixar, poupando o trabalho de baixar todas as imagens e depois escolher uma para enviar. Será um possível ponto de mudança caso volte a trabalhar nesse projeto._

### /anime _1_ ([imagesearch](botfunc/imagemsearch.py))

Esse comando foi escrito em duas partes. Ele retorna a imagem de um anime pesquisado juntamente com o Título, Tipo (anime ou OVA), Popularidade e Sinopse do anime.
A primeira parte do comando é responsável por pegar a imagem da pesquisa do site [Kitsu](https://kitsu.io/anime). Para isso utilizo as bibliotecas `bs4` e a `requests`.

### /anime _2_ ([Main](main.py))

A segunda parte da função está no meu arquivo main. Para retornar as informações necessárias sobre o anime pesquisado utilizei uma API assíncrona chamada `kitsu.py`, desenvolvida pelo site de onde retiro a imagem do anime. Como não tenho muita experiência nesse tipo de programação, acabei não tendo sucesso em criar uma classe que trabalhasse fora do meu código principal, então escrevi essa função no começo do arquivo. Também não encontrei muitas informações para essa API. Ela retorna um objeto em JSON de onde extraio o Título, Tipo (anime ou OVA), Popularidade e Sinopse do anime.

### /clima ([Clima](botfunc/clima.py))

Criei essa classe para retornar o clima de uma cidade, bairro ou municipio. Para isso utilizo uma API JSON do Open Weather Map e extraio todas as informações necessárias do objeto JSON que minha requisição retorna. Essa classe foi escrita com diversas funções que poderiam se resumir em uma, foi criada dessa forma porque achei que poderia usar essas funções separadamente em algum momento.

### /insta ([Insta](botfunc/textsearch.py))

Aqui temos mais um pouco de web scraping. Utilizo o `selenium` e o `bs4` para pesquisar um termo no site [All Hashtag](https://www.all-hashtag.com/) e retornar essa pesquisa no chat. Criei essa função para minha namorada que não tinha muita paciência para criar hashtags em suas postagens.

## Comando Genéricos ([Comandos](botfunc/comandos.py))

Apesar da complexidade de algumas funções citadas acima, a criação dos **Comandos genéricos** foi a mais legal para mim. Esses comandos abrem a possibilidade do usuário criar seu próprio comando que tem como resposta um texto simples ou um texto com variáveis. O bot que vi no whatsapp tinha essa função, foi a parte mais legal para mim e para todos os meus amigos. Consegui recriar essa função com algumas melhorias.

### Criando comandos genéricos (/cmdadd)

O primeiro desafio era armazenar os comandos criados, como não pretendia levar esse bot muito a frente não criei um banco de dados para ele, então usei arquivos .txt para essa função.

Para chamar um comando primeiramente tenho que definir um decorator e passar o parâmetro `commands`. Dentro desse parâmetro devo passar uma lista de palavras que serão utilizadas para chamar o comando, que por padrão, devem ser chamadas no chat com uma '/' na frente:

```
@bot.message_handler(commands=['cmdadd'])
```

Todo arquivo .txt de comando criado é nomeado com o ID do chat e nome do comando, assim evitando que outros chats diferentes possam acessar o comando. Como pode ser observado na pasta [Generic](generic).

*Ocultei o ID do chat por motivos de segurança*

*Ao chamar esse comando e seguir as instruções presentes no arquivo [Comandos](botfunc/comandosgerais.txt) o usuário cria seu comando.*

### Criando comandos genéricos (Variáveis especiais)

Essas variáveis são palavras entre {} que são substitituidas por outros valores sempre que o usuário chamar o comando.
Por exemplo, se um usuário criar um comando com a variável {smallRandom}, sempre que esse comando for chamado essa variácel será substítuida por um número entre 0 e 10:

```
Comando -> A estrada tem {smallRandom} km!
Retorno -> A estrada tem 4 km!
```

*O usuário pode usar mais de uma variável por comando/resposta. A função de chamar o comando conta com um `while` que só para quando substitui todas as variáveis especiais*

Para mais variáveis especiais acesse o documento [Comandos](botfunc/comandosgerais.txt)

### Chamando o comando genérico (!nomedocomando)

O decorator nos permite passar como parâmetro uma função personalizada para a chamada dos comandos. No Whatsapp os comandos eram chamados por uma '!' no começo da palavra. No telegram a '/' faz essa função. Apesar disso, como forma de diferenciar os comandos genéricos dos principais, optei por utilizar '!' ao invés da '/' para chamar o comando. Para isso utilizei uma `lambda` com uma função que verificava se na primeira posição do texto de cada mensagem havia uma '!':

```
@bot.message_handler(func=lambda mensagem: True if mensagem.text[0] == '!' else False)
```

Com isso o usuário poderia chamar o comando apenas com uma '!' + nomedocomando.

### Adicionando respostas ao comando genérico (/cmdaddres)

Outra função bastante interessante era a de adicionar várias respostas possíveis para o mesmo comando, quando há mais de uma resposta o Zeta escolhe uma aleatoriamente e a envia para o usuário, o que pode render jogos bem engraçados. Não há limite de respostas para serem adicionadas, todas as respostas são armazenadas no arquivo .txt, toda vez que uma resposta é adicionada o Zeta abre o arquivo, adiciona as respostas já existentes a uma lista, depois adiciona a nova resposta na mesma lista e escreve novamente o arquivo. O que preserva as respostas antigas e adiciona a nova.

*Ao chamar esse comando e seguir as instruções presentes no arquivo [Comandos](botfunc/comandosgerais.txt) o usuário adiciona uma resposta nova ao seu comando genérico.*


### Listando respostas do comando genéricos (/listares)

Uma melhoria em relação ao bot no qual me inspirei. Os usuários não sabiam quais respostas tinham em cada comando, o que pode ser legal, mas para os criadores dos comandos (quem o desenvolvedor permitir que crie) pode ser uma opção interessante. O comando /listares lista todas as respostas e seus index atuais dentro de um comando genérico.

*Ao chamar esse comando e seguir as instruções presentes no arquivo [Comandos](botfunc/comandosgerais.txt) o usuário lista as respostas do comando genérico.*

### Removendo comandos genéricos (/cmdremove)

*Ao chamar esse comando e seguir as instruções presentes no arquivo [Comandos](botfunc/comandosgerais.txt) o usuário remove um comando genérico.*

### Removendo respostas de um comando genérico (/cmddelres)

Esse comando remove uma respostas dentro de um comando genérico, para isso o usuário precisará do index da resposta que pode ser obtido pelo comando `/listares`.
O comando deve ter ao menos uma resposta.

*Ao chamar esse comando e seguir as instruções presentes no arquivo [Comandos](botfunc/comandosgerais.txt) o usuário remove uma resposta do comando genérico.*

### Listando comandos genéricos (/lista)

*Ao chamar esse comando e seguir as instruções presentes no arquivo [Comandos](botfunc/comandosgerais.txt) o usuário lista os comandos genéricos presentes no chat.*
