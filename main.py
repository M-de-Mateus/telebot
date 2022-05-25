import os
import random
import time
import kitsu
import asyncio
import telebot as tb
from botfunc.clima import Clima
from botfunc.imagesearch import Gimage
from botfunc.comandos import Comando
from botfunc.textsearch import Insta


async def anime_search(pesquisa):
    client = kitsu.Client()
    entries = await client.search_anime(pesquisa, limit=10)
    if not entries:
        print(f'Sem resultados para: {pesquisa}')
    itens = {}
    title = []
    subtypes = []
    synopsis = []
    popularity = []
    try:
        for i, anime in enumerate(entries, 1):
            if anime.subtype == 'TV' or anime.subtype == 'OVA':
                title.append(str(anime.canonical_title))
                itens['Title'] = title
                subtypes.append(str(anime.subtype))
                itens['Sub-type'] = subtypes
                synopsis.append(str(anime.synopsis))
                itens['Anime synopsis'] = synopsis
                popularity.append(str(anime.popularity_rank))
                itens['Popularity'] = popularity
    except TypeError:
        title.append(str(entries.canonical_title))
        itens['Title'] = title
        subtypes.append(str(entries.subtype))
        itens['Sub-type'] = subtypes
        synopsis.append(str(entries.synopsis))
        itens['Anime synopsis'] = synopsis
        popularity.append(str(entries.popularity_rank))
        itens['Popularity'] = popularity
    await client.close()
    return itens


chave_api = '5358034494:AAHTw8hu0aNBktOBKjy3oGCzJLdTApFBLTE'
bot = tb.TeleBot(chave_api)


@bot.message_handler(commands=['anime'])
def buscar_anime(mensagem):
    busca_imagem = Gimage()
    msg = mensagem.text
    try:
        comando, pesquisa = msg.split(" ", 1)
        busca_imagem.imagem_anime(pesquisa)
        resultado = asyncio.new_event_loop()
        asyncio.set_event_loop(resultado)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        resultado = resultado.run_until_complete(anime_search(pesquisa))
        print(resultado)
        image = open(f'images/{pesquisa}.jpg', 'rb')
        bot.send_photo(mensagem.chat.id, photo=image, caption=f"Title: {resultado['Title'][0]}\n"
                                                              f"Sub-type: {resultado['Sub-type'][0]}\n"
                                                              f"Popularity: {resultado['Popularity'][0]}\n")
        bot.send_message(mensagem.chat.id, f"Synopsis: {resultado['Anime synopsis'][0]}")
        image.close()
        busca_imagem.remover_imagem(pesquisa)
    except ValueError:
        bot.reply_to(mensagem, 'Insira o nome de um anime')
    except (NameError, Exception):
        bot.reply_to(mensagem, 'Erro de conexão ou Anime não existe! Tente novamente!')


@bot.message_handler(commands=['insta'])
def buscar_hashtag(mensagem):
    hashtag = Insta()
    msg = mensagem.text
    try:
        comando, pesquisa = msg.split(" ", 1)
        if '#' in pesquisa:
            bot.reply_to(mensagem, 'Não é necessário incluir # na pesquisa! Tente novamente sem o #!')
        else:
            bot.send_message(mensagem.chat.id, 'Pesquisando em: https://www.all-hashtag.com/')
            bot.reply_to(mensagem, f'{hashtag.pesquisar(pesquisa)}')

    except (ValueError, Exception):
        bot.reply_to(mensagem, 'Algo aconteceu, verifique o termo pesquisado e tente novamente!')


@bot.message_handler(commands=['roleta'], chat_types=['group', 'supergroup', 'channel'])
def roleta_russa(mensagem):
    pistola = ['Click!', 'Click!', 'Bang!']
    if random.choice(pistola) == 'Click!':
        bot.reply_to(mensagem, 'Click! 😥🔫 Ta safe, mas fica esperto!')
    else:
        bot.reply_to(mensagem, 'Ultimas palavras?')
        time.sleep(2)
        bot.send_message(mensagem.chat.id, 'Bang! 💥🔫')
        time.sleep(1)
        bot.kick_chat_member(mensagem.chat.id, mensagem.from_user.id)


@bot.message_handler(commands=['comandos'])
def comandos_bot(mensagem):
    with open(os.path.relpath(f'botfunc/comandosgerais.txt'), 'r', encoding='utf-8') as file:
        bot.reply_to(mensagem, file.read())


@bot.message_handler(commands=['cmdadd'])
def adicionar_comando(mensagem):
    comando = Comando()
    msg = mensagem.text
    try:
        cmd, comando_user, resposta = msg.split(" ", 2)
        if comando_user[0] != '!':
            bot.reply_to(mensagem, 'É necessário que o comando comece com "!" e não tenha espaços!')
        else:
            if comando.verificar_comando(comando_user, mensagem.chat.id):
                bot.reply_to(mensagem, 'Comando já existe!')
            else:
                comando.criar_comando(comando_user, resposta, mensagem.chat.id)
                bot.reply_to(mensagem, f'Comando {comando_user} foi adicionado com sucesso!')
    except ValueError:
        bot.reply_to(mensagem, 'Você deve adicionar uma resposta ao comando!')
    except OSError:
        bot.reply_to(mensagem, r'O comando não pode conter caracteres especiais do tipo \/:*"?<>|')
    except (NameError, Exception):
        bot.reply_to(mensagem, 'Algo aconteceu. Não consegui criar seu comando!')


@bot.message_handler(func=lambda mensagem: True if mensagem.text[0] == '!' else False)
def chamar_comando(mensagem):
    comando = Comando()
    try:
        if comando.verificar_comando(mensagem.text, mensagem.chat.id):
            bot.reply_to(mensagem, comando.chamar_comando(mensagem.text, mensagem, mensagem.chat.id))
        else:
            bot.reply_to(mensagem, 'Comando não existe!')
    except (ValueError, Exception):
        bot.reply_to(mensagem, 'Algo aconteceu, verifique se escreveu corretamente!')


@bot.message_handler(commands=['cmdaddres'])
def resposta_comando(mensagem):
    comando = Comando()
    msg = mensagem.text
    try:
        cmd, comando_user, resposta = msg.split(" ", 2)
        if comando_user[0] != '!':
            bot.reply_to(mensagem, 'É necessário que o comando comece com "!" e não tenha espaços!')
        else:
            if comando.verificar_comando(comando_user, mensagem.chat.id):
                comando.add_resposta_comando(comando_user, resposta, mensagem.chat.id)
                bot.reply_to(mensagem, 'Resposta adicionada com sucesso!')
            else:
                bot.reply_to(mensagem, 'Comando não existe!')
    except ValueError:
        bot.reply_to(mensagem, 'Você deve adicionar uma resposta ao comando!')


@bot.message_handler(commands=['lista'])
def listar_comandos(mensagem):
    comando = Comando()
    bot.reply_to(mensagem, comando.listar_comando(mensagem.chat.id))


@bot.message_handler(commands=['listares'])
def listar_respostas(mensagem):
    respostas = Comando()
    msg = mensagem.text
    try:
        cmd, comando = msg.split(" ", 1)
        reply = respostas.listar_resposta(comando, mensagem.chat.id)
        bot.send_message(mensagem.chat.id, f'Essas são as respostas para o comando {comando}:')
        for i, l in enumerate(reply):
            bot.send_message(mensagem.chat.id, f'{i + 1} - {reply[i]}')
    except ValueError:
        bot.reply_to(mensagem, 'Você deve informar um comando!')
    except FileNotFoundError:
        bot.reply_to(mensagem, 'Comando não existe!')


@bot.message_handler(commands=['cmddelres'])
def remover_resposta(mensagem):
    comandos = Comando()
    try:
        msg = mensagem.text
        cmd, comando, num_resp = msg.split(" ", 2)
        num_resp = int(num_resp)
        num_resp = num_resp - 1
        if comandos.excluir_resposta(comando, mensagem.chat.id, num_resp):
            bot.reply_to(mensagem, f'Resposta excluida do comando {comando}.')
        else:
            bot.reply_to(mensagem, 'O comando deve conter ao menos uma resposta!')
    except ValueError:
        bot.reply_to(mensagem, 'Você deve informar um comando e o número da resposta!')
    except FileNotFoundError:
        bot.reply_to(mensagem, 'Esse comando não existe!')
    except IndexError:
        bot.reply_to(mensagem, f'Não existe esse número de resposta no comando!')


@bot.message_handler(commands=['cmdremove'])
def remover_comando(mensagem):
    comando = Comando()
    msg = mensagem.text
    try:
        cmd, comando_user = msg.split(" ", 1)
        if comando_user[0] != '!':
            bot.reply_to(mensagem, 'É necessário que o comando comece com "!" e não tenha espaços!')
        else:
            if comando.verificar_comando(comando_user, mensagem.chat.id):
                comando.remover_comando(comando_user, mensagem.chat.id)
                bot.reply_to(mensagem, f'O comando {comando_user} foi removido com sucesso!')
            else:
                bot.reply_to(mensagem, 'Comando não existe!')
    except (ValueError, Exception):
        bot.reply_to(mensagem, f'Ocorreu algum erro, verifique o nome do comando!')


@bot.message_handler(commands=['pesquisa'])
def image_search(mensagem):
    procurar = Gimage()
    msg = mensagem.text
    try:
        comando, pesquisa = msg.split(" ", 1)
        procurar.pesquisar(pesquisa)
        image = open(f'images/{procurar.sortear_imagem(pesquisa)}', 'rb')
        bot.send_photo(chat_id=mensagem.chat.id, reply_to_message_id=mensagem.id, photo=image, caption=f"{pesquisa}",
                       protect_content=True)
        image.close()
        procurar.remover_imagem(pesquisa)
    except (ValueError, Exception):
        bot.reply_to(mensagem,
                     'Não consegui achar essa imagem! Verifique se informou o termo da pesquisa corretamente!')


@bot.message_handler(commands=['clima'])
def send_clima(mensagem):
    consulta = Clima()
    msg = mensagem.text
    try:
        comando, cidade = msg.split(" ", 1)
        if consulta.consultar_temperatura(cidade) == '404':
            bot.reply_to(mensagem, 'Cidade não encontrada!')
        else:
            bot.reply_to(mensagem,
                         f"Clima: {cidade}\nTemperatura: {consulta.consultar_temperatura(cidade)}\nMáxim"
                         f"a: {consulta.consultar_tempmax(cidade)}\nMínima:{consulta.consultar_tempmin(cidade)}\nTemp"
                         f"o: {consulta.consultar_descricao(cidade)}\nUmidade: {consulta.consultar_umidade(cidade)}")
    except ValueError:
        bot.reply_to(mensagem, 'Preencha com o nome de uma cidade!')


@bot.message_handler(commands=['amigo'])
def amigo(mensagem):
    bot.reply_to(mensagem, f'Não sou seu amigo!')


@bot.message_handler(commands=['start', 'help', 'info'])
def responder(mensagem):
    print(mensagem)
    bot.send_message(mensagem.chat.id, f"Olá {mensagem.from_user.first_name}, aqui é o Zeta! 🤖\nPara saber mais digite"
                                       f" ou clique em /comandos")


bot.infinity_polling()
