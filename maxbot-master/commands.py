import datetime
import json
import requests
import urllib.parse
import urllib.request
import socket

# APIs do AccuWeather, tem essas 3 pelo fato do limite de requisições p/ dia ser só 50 em cada uma
API = "5EHm0OouVq2MYsFa91FGKPadu6raFZEF"   #API 1
#API = "nnvBpHyP6BUcWPiePvvGcPdtTkUOhrz8"   #API 2
#API = "vBkVX41ZeQvmP2li5Z0AjQRSHfiVfvdz"    #API 3

# APIs do Yandex tradutor
API_T = 'trnsl.1.1.20190927T202249Z.ae7d6ae63ea79bdc.69b6616a32a45b1f3412c33ac2de768277b6515c'
urlt = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

def devs():
    """
    Funcao que retorna os nomes dos desenvolvedores
    :return answer: uma string com os nomes
    """
    answer = "[DEVS] Developers: \n1 - Gustavo Rodrigues \n2 - Igor Capeletti"
    return answer


def dataHora():
    """
    funcao que solicita o horarioo local da maquina
    :return answer: uma string com o horario atual
    """
    time = datetime.datetime.now()
    answer = "[TIME] Data e hora atual: " + str(time)
    return answer


def help(argument):
    """
    funcao que retorna a lista de comandos disponiveis
    :param argument: string que representa o comando que se deseja mais informacoes
    :return: string com os comandos disponiveis ou mais informacoes sobre um comando
    """
    if argument != "":
        argument = argument.upper()
        if argument == "DEVS":
            answer = "[HELP] O comando \devs contem informacoes sobre os desenvolvedores do MAX."
        elif argument == "DATAHORA":
            answer = "[HELP] O comando \datahora informa a data e hora atual."
        elif argument == "WEATHER":
            answer = "[HELP] O comando \weather espera uma cidade como parametro e retorna a temperatura atual desta localizacao."
        elif argument == "WEATHERWEEK":
            answer = "[HELP] O comando \weatherweek espera uma cidade como parametro e retorna a respectiva previsao do tempo num periodo de 5 dias."
        elif argument == "HELP":
            answer = "[???] LOOOOOOOPP"
        else:
            answer = "[ERROR] Desculpe, nao reconheco o comando \help" + argument
    else:
        answer = "[HELP] Comandos:\n \devs\n \datahora\n \weather <cidade>\n \weatherweek <cidade>\n \help <comando>"
        print(answer)

    return answer


def weather(argument):
    """
    funcao que recebe como parametro o comando e testa se possui os parametros corretos
    caso tenha parametro certo, requisita ao servico de metereologia, via http (POST e GET) e retorna a temperatura
    atual da cidade requisitada

    :param argument: string que eh a cidade a ser pesquisada
    :return: condicao climatica atual da localizacao ou uma mensagem de erro caso a cidade nao tenha sido informada
    """
    if argument != "":
        print("[LOG] Pesquisando previsao...")

        sockOpenWeather = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)  # abre conexao com o servidor do Openweather
        sockOpenWeather.connect(("api.openweathermap.org", 80))  # conecta com a api
        request = (
                    'GET /data/2.5/weather?q=' + argument +
                    '&appid=778c214add5c6263ad53043ba7bf546d HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n')
        sockOpenWeather.sendall(request.encode())  # envia request GET http para a api
        requisicao = sockOpenWeather.recv(1024).decode()
        sockOpenWeather.close()  # fecha conexao

        requisicao = requisicao.split('{', 1)  # divide a string em 2
        js = requisicao[1]  # pega apenas  a parte que eh o json
        js = '{' + js  # readiciona uma { no inicio da string q eh o json
        tempo = json.loads(js)

        status = tempo['weather'][0]['description']     # recebe descricao do tempo em ingles dentro do dict 'tempo'
        qChuva = 0
        if tempo['weather'][0]['main'] == "Rain" and 'rain' in tempo:   # verifica se existe palavra no dict 'tempo' e busca quantidade de chuva
            qChuva = list(tempo['rain'].values())[0]    #quantidade de chuva previsto

        print("[LOG] Traduzindo...")
        params = dict(key=API_T, text=status, lang='en-pt')     #parametros para requisicao com API de traducao
        res = requests.get(urlt, params=params)     #busca com uma API a traducao da previsão do tempo, retornando um json
        jsonT = res.json()      # transforma para dict o json recebido da API
        status = str(jsonT['text'][0])  #pega string traduzida da API

        #variavel com todas as informacoes atuais do tempo
        answer = "[FORECAST] Cidade " + argument + "\nStatus atual: " + status + "\nPrevisao de chuva: " + str(
            qChuva) + "mm\nTemperatura atual: " + str(
            round((float(tempo['main']['temp'])) - 273.15)) + "oC\nUmidade em " + str(
            tempo['main']['humidity']) + "porcento\nVelocidade do vento em " + str(
            round((float(tempo['wind']['speed'])) * 3.6)) + " km/h"
    else:
        answer = "[ERROR] Comando \weather necessita de uma localizacao. Digite \help para saber mais"

    return answer


def weatherWeek(argument):
    """
    funcao que recebe uma cidade como parametro e retorna a previsao do tempo para ela, no periodo de uma semana
    :param argument: string que representa a cidade a ser pesquisada
    :return: temperatura da semana
    """
    if argument != "":
        print("[LOG] Cidade " + argument + " recebida do cliente e ")
        city = urllib.parse.quote(str(argument))  # transforma string da cidade para formato URL p/ API reconhecer
        print("transformada para " + str(city) + " no formato URLs!")
        print("[LOG] Pesquisando previsao...")

        sockAccuWeather = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)  # abre conexao TCP com o servidor do AccuWeather
        sockAccuWeather.connect(("dataservice.accuweather.com", 80))  # conecta com a API AccuWeather

        # string de requisição
        request = ('GET /locations/v1/cities/search?apikey=' + API +
                   '&q=' + city + '&details=true HTTP/1.1\r\nHost: dataservice.accuweather.com\r\n\r\n')

        sockAccuWeather.sendall(request.encode('utf-8'))  # envia request GET http para a api
        requisicao = sockAccuWeather.recv(2048).decode()  # recebe string com resposta do servidor
        sockAccuWeather.close()  # fecha conexao com API AccuWeather

        requisicao = requisicao.split('[', 1)  # divide a string em 2
        requisicao = requisicao[1]  # pega segunda parte da string
        requisicao = requisicao.split(',"Country"', 1)  # separa string novamente
        requisicao = requisicao[0]  # pega primeira parte da string separada
        requisicao = requisicao + '}'  # acrescenta um caracter no final da string
        tempo = json.loads(requisicao)  # transforma toda resposta da API para dict
        location_key = tempo['Key']

        sockAccuWeather = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)  # abre conexao  com o servidor do AccuWeather
        sockAccuWeather.connect(("dataservice.accuweather.com", 80))  # conecta com a api

        # string de requisição
        request = ('GET /forecasts/v1/daily/5day/' + location_key + '?apikey=' + API +
                   '&details=true HTTP/1.1\r\nHost: dataservice.accuweather.com\r\n\r\n')

        sockAccuWeather.sendall(request.encode('utf-8'))  # envia request GET http para a api
        requisicao2 = sockAccuWeather.recv(2048).decode('utf-8')  # recebe string com resposta do servidor
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        requisicao2 = requisicao2 + sockAccuWeather.recv(2048).decode(
            'utf-8')  # acrescenta resposta anterior com esta nova
        sockAccuWeather.close()  # fecha conexao com API AccuWeather

        requisicao2 = requisicao2.split('{', 1)  # divide a string em 2
        requisicao2 = '{' + requisicao2[1]

        tempo = json.loads(requisicao2)  # transforma toda resposta da API para dict
        resp = ""
        print("[LOG] Traduzindo...")
        respStatus = []
        cont = 0

        # este for vai percorrer posições do dict dos dados de cada dia da previsão e colocar
        # todos os status em um dict para depois serem traduzidas
        # vai colocar todos os status do turno do dia e noite de cada dia em uma list
        for key1 in tempo['DailyForecasts']:
            status = key1['Day']['LongPhrase']
            respStatus.insert(cont, str(status))
            cont = cont + 1
            status = key1['Night']['LongPhrase']
            respStatus.insert(cont, str(status))
            cont = cont + 1

        params = dict(key=API_T, text=str(respStatus),
                      lang='en-pt')  # envia list anterior em formato string para API traduzir
        res = requests.get(urlt, params=params)  # recebe json da API com as palavras já traduzidas
        jsonT = res.json()  # transforma arquivo json recebido em dict
        status = str(jsonT['text'][0])
        string = status[1:len(status)]
        list = string.split("', '")
        list[0] = list[0][1:]
        list[9] = list[9][:-2]

        # este for vai buscar as temperaturas, chuva, vento e status de cada dia
        cont = 0
        for key1 in tempo['DailyForecasts']:
            tempMin = round(((key1['Temperature']['Minimum']['Value']) - 32) / 1.8000)
            tempMax = round(((key1['Temperature']['Maximum']['Value']) - 32) / 1.8000)

            # parte da temperatura durante o dia
            ventoD = round((key1['Day']['Wind']['Speed']['Value']) * 1.609)
            qChuvaD = round((key1['Day']['Rain']['Value']) * 25.4)
            statusD = list[cont]
            cont = cont + 1

            # parte da temperatura durante a noite---------------------------------------
            ventoN = round((key1['Night']['Wind']['Speed']['Value']) * 1.609)
            qChuvaN = round((key1['Night']['Rain']['Value']) * 25.4)
            statusN = list[cont]
            cont = cont + 1

            diaData = key1['Date']

            # resposta de cada dia que retorna para resposta prncipal dessa função
            resp = resp + ("\n-----------\nData: " + diaData[8:10] + "/" + diaData[5:7] + "/" + diaData[0:4] +
                           "\nTemperatura minima: " + str(tempMin) + "\nTemperatura maxima: " + str(tempMax) +
                           "\n--Durante o dia:" + "\nPrevisao do tempo: " + statusD + "\nChuva " +
                           str(qChuvaD) + "mm\nVento " + str(ventoD) +
                           "km/h\n--Durante a noite:" + "\nPrevisao do tempo: " + statusN + "\nChuva " +
                           str(qChuvaN) + "mm\nVento " + str(ventoN) + "km/h")

        # resposta principal que retornada para cliente
        answer = "[FORECAST] Previsao do tempo para " + argument + " durante os próximos dias:\n" + resp

    else:
        # retorna resposta se cliente deixou em branco o parâmetro de cidade
        answer = "[ERROR] Comando \weatherweek necessita de uma localizacao. Digite \help para saber mais"

    return answer  # retorna resposta da função
