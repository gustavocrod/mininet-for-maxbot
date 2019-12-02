import argparse

def makeArgs():
    """
    funcao que utiliza o argparse para receber o ip e porta de conexao para o servidor do max
    :return: lista com os argumentos passados
    """
    parser = argparse.ArgumentParser(description="client max")

    parser.add_argument("--ip", "-ip", action="store", dest="host", help="Endereco ip do servidor")
    parser.add_argument("--port", "-port", default='127.0.0.1', type=int, action="store", dest="port", help="Porta onde o servidor roda")

    args = parser.parse_args()

    return args

def printMax():
    print(" ____    ____       _       ____  ____")
    print("|_   \  /   _|     / \     |_  _||_  _| ")
    print("  |   \/   |      / _ \      \ \  / /")
    print("  | |\  /| |     / ___ \      > `' <   ")
    print(" _| |_\/_| |_  _/ /   \ \_  _/ /'`\ \_ ")
    print("|_____||_____||____| |____||____||____| ")

def printHelpClient():
    print("[HELP] Digite \help para listar os comandos disponiveis do M.A.X\n")
    print("[HELP] Aperte 'q' e de enter para sair\n")