# -*- coding: utf-8 -*-
import socket
import threading
from util import makeArgs
from commands import *

# APIs do AccuWeather
# API = "5EHm0OouVq2MYsFa91FGKPadu6raFZEF"
API = "nnvBpHyP6BUcWPiePvvGcPdtTkUOhrz8"
ack = "ACK"
# APIs do Yandex tradutor
API_T = 'trnsl.1.1.20190927T202249Z.ae7d6ae63ea79bdc.69b6616a32a45b1f3412c33ac2de768277b6515c'
urlt = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


# parte de threads do servidor
def makeConnection(client, endereco):
    """
    Funcao que roda em cada thread, e eh responsavel por cada conexao de um cliente
    :param client: socket responsavel pela conexao com o cliente
    :param endereco: vetor que contem o ip e porta do cliente
    :return:
    """
    print("\n\n[LOG] Conectado com cliente " + str(endereco[0]) + ":" + str(endereco[1]))
    client.send(str(ack).encode())  # envia ACK para o cliente(confirmação de conexão com este servidor)
    print("[LOG] ACK enviada para cliente!")

    cont = 1
    while True:
        data = client.recv(4096).decode()  # aguarda até cliente enviar alguma mensagem e salva na variável data
        print("-------- Cliente " + str(endereco[0]) + ":" + str(endereco[1]) + " ---- Solicitacao " + str(
            cont) + " ----")
        cont = cont + 1

        if not data:
            print("[LOG] Cliente desconectou!")
            break

        isCommand = ord(data[0])  # pega o codigo ascii do primeiro character da string
        if isCommand == 92:  # entao eh um comando 92 == '\'
            data = data[1:]  # recebe string do segundo caracter ao ultimo - retira o \
            answer = ""

            if data.count(' ') == 0:
                command = data
                command = command.upper()  # transforma tudo em caixa alta
                print("[INFO] command: " + command)
                if command == "HELP":
                    answer = help("")
                elif command == "DATAHORA":
                    answer = dataHora()
                elif command == "DEVS":
                    answer = devs()
                elif command == "WEATHER":
                    answer = "[HELP] O comando \weather necessita de uma cidade como argumento. \help weather para saber mais"

                elif command == "WEATHERWEEK":
                    answer = "[HELP] O comando \weatherweek necessita de uma cidade como argumento. \help weatherweek para saber mais"
                else:
                    answer = "[ERROR] Comando invalido. Digite \help para saber mais"
            else:
                command = data.split(" ")[0]  # divide a string em espacos e pega o primeiro elemento
                argument = data.split(command + " ")[1]  # pega o restante da string, retirando o comando+space
                command = command.upper()  # transforma tudo em caixa alta
                print("comando: '" + command + "' argumento: '" + argument + "'")
                if command == "HELP":
                    answer = help(argument)
                elif command == "WEATHER":
                    answer = weather(argument)
                elif command == "WEATHERWEEK":
                    answer = weatherWeek(argument)
                elif command == "DATAHORA":
                    answer = "[HELP] O comando \datahora nao necessita de um argumento"
                elif command == "DEVS":
                    answer = "[HELP] O comando \devs nao necessita de um argumento"
                else:
                    answer = "[ERROR] Desculpe nao reconheci o comando '" + command + "'. Digite \help para saber mais"

            client.send(str(answer).encode('utf-8'))  # envia a resposta para o cliente, depois de processada pelo server
            print("[INFO] Resposta processada e enviada para cliente " + str(endereco[0]) + ":" + str(endereco[1]))
        else:
            answer = data
            client.send(str(answer).encode('utf-8'))  # envia para o cliente mesma coisa que ele mandou pois não é comando
            print("[ERROR] Mensagem de cliente nao e um comando, reenviada mesma mensagem para cliente")

    print("[LOG] Thread com cliente finalizada!")

def runServer(ip, port):
    """
    funcao responsavel pela iniclializacao do servidor e de criar conexoes com cada cliente
    :param ip: ip em qual rodara o servidor "localhost"
    :param port: porta em qual o servidor no max rodara
    :return:
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(0)


    print("[LOG] Escutando " + str(ip) + ":" + str(port) + "...\n")  # inicia servidor

    while True:
        client, endereco = server.accept()  # aceita conexão dos clientes
        threading.Thread(target=makeConnection, args=(client, endereco)).start()

def main():
    """
    Funcao main, responsavel por conferir os parametros passados e de inicializar o servidor
    :return:
    """
    args = makeArgs()
    if args.port:
        runServer(args.host, args.port)

if __name__ == "__main__":
    main()

