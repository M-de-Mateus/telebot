import os
import random


class Comando:

    @staticmethod
    def verificar_comando(comando, id_chat):
        comando = str(id_chat) + '-' + comando + '.txt'
        for _, _, arquivo in os.walk('generic'):
            for line in arquivo:
                if comando == line:
                    return True

    @staticmethod
    def criar_comando(comando, mensagem, id_chat):
        respostas = [mensagem]
        with open(f'generic/{id_chat}-{comando}.txt', 'w+', encoding='UTF-8', errors='replace') as file:
            for line in respostas:
                file.write(f'{str(line)}' + '%%')
        file.close()

    @staticmethod
    def add_resposta_comando(comando, mensagem, id_chat):
        with open(os.path.relpath(f'generic/{id_chat}-{comando}.txt'), 'r', encoding='UTF-8', errors='replace') as file:
            resposta = file.readline()
            resposta = resposta.split('%%')
            if '' in resposta:
                resposta.remove('')
            resposta.append(mensagem)
            file.close()
        with open(os.path.relpath(f'generic/{id_chat}-{comando}.txt'), 'w', encoding='UTF-8', errors='replace') as file:
            for line in resposta:
                file.write(f'{str(line)}' + '%%')
            file.close()

    @staticmethod
    def chamar_comando(comando, mensagem, id_chat):
        smallRandom = random.randint(1, 10)
        mediumRandom = random.randint(11, 100)
        largeRandom = random.randint(101, 1000)
        nome = mensagem.from_user.first_name
        with open(os.path.relpath(f'generic/{id_chat}-{comando}.txt'), 'r', encoding='UTF-8', errors='replace') as file:
            resposta = file.readline()
            resposta = resposta.split('%%')
            if '' in resposta:
                resposta.remove('')
            file.close()
            reply = random.choice(resposta)
            while '{smallRandom}' in reply or '{mediumRandom}' in reply or '{largeRandom}' in reply or '{nomeAutor}' \
                    in reply:
                if '{smallRandom}' in reply:
                    reply = reply.replace('{smallRandom}', f'{smallRandom}')
                elif '{mediumRandom}' in reply:
                    reply = reply.replace('{mediumRandom}', f'{mediumRandom}')
                elif '{largeRandom}' in reply:
                    reply = reply.replace('{largeRandom}', f'{largeRandom}')
                elif '{nomeAutor}' in reply:
                    reply = reply.replace('{nomeAutor}', f'{nome}')
            return reply

    @staticmethod
    def remover_comando(comando, id_chat):
        os.remove(os.path.relpath(f'generic/{id_chat}-{comando}.txt'))

    @staticmethod
    def listar_comando(comando_id):
        cmd = []
        lista = []
        for _, _, comandos in os.walk('generic'):
            if len(comandos) == 0:
                msg = 'Ainda não criaram comandos genéricos nesse chat!'
            else:
                for line in comandos:
                    if str(comando_id) in line:
                        line = line.replace(str(comando_id), '')
                        line = line.split('.txt')
                        cmd.append(line)
                for valor in cmd:
                    lista.append(valor[0])
                if '' in lista:
                    lista.remove('')
                msg = f'Esses são os comandos genéricos criados nesse chat:\n {lista}'
                msg = msg.replace(']', '')
                msg = msg.replace('[', '')
                msg = msg.replace("'", '')
                msg = msg.replace('-', '')
                msg = msg.replace(',', '\n')
            return msg

    @staticmethod
    def listar_resposta(comando, chat_id):
        with open(os.path.relpath(f'generic/{chat_id}-{comando}.txt'
                                  f''), 'r', encoding='UTF-8', errors='replace') as file:
            resposta = file.readline()
            resposta = resposta.split('%%')
            if '' in resposta:
                resposta.remove('')
            file.close()
        return resposta

    @staticmethod
    def excluir_resposta(comando, chat_id, num_resp):
        with open(os.path.relpath(f'generic/{chat_id}-{comando}.txt'
                                  f''), 'r', encoding='UTF-8', errors='replace') as file:
            resposta = file.readline()
            resposta = resposta.split('%%')
            if '' in resposta:
                resposta.remove('')
            if len(resposta) == 1:
                return False
            else:
                del (resposta[int(num_resp)])
            file.close()
        with open(os.path.relpath(f'generic/{chat_id}-{comando}.txt'), 'w', encoding='UTF-8',
                  errors='replace') as file:
            for line in resposta:
                file.write(f'{str(line)}' + '%%')
            file.close()
        return True
