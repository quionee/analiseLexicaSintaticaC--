# função que lê o arquivo e retorna a tabela de lexemas
def leArquivo(nomeArquivo):
    # abrindo o arquivo
    arquivo = open(nomeArquivo)
    # variável que verifica se o arquivo terminou
    lendoArquivo = True
    # variável que armazena uma palavra lida do arquivo
    # uma palavra é um lexema
    palavra = ""
    # lista que armazena os lexemas encontrados no arquivo
    lexemas = []
    # variável que verifica se faz-se necessário a leitura de um caracter do arquivo
    lerCaracter = True
    # while roda enquanto há algo para ler do arquivo

    while (lendoArquivo):
        if (lerCaracter): # se "lerCaracter" == true, um caracter é lido
            caracter = arquivo.read(1)
        else: # se "lerCaracter" == false, nada é lido
            lerCaracter = True

        # condição usada para ignorar espaços em branco e quebras de linha
        # caso seja uma dessas opções, a palavra lida até então é armazenada na lista de lexemas
        if ((caracter == " ") or (caracter == "\n")):
            # condição utilizada para verificar se a palavra está vazia, caso não esteja,
            # ela é armazenada na lista de lexemas
            if (palavra != ""):
                lexemas.append(palavra)
                palavra = ""

        # condição usada para verificar os delimitadores "{", "[", "}", "]", ";",
        # e o operador aritmético "*"
        elif ((caracter == "{") or (caracter == "[") or (caracter == "}") or (caracter == "]")
        or (caracter == "*") or (caracter == ";")):
            if (palavra != ""):
                lexemas.append(palavra)
                palavra = ""
            lexemas.append(caracter)

        # condição usada para verificar os operadores relacionais ">=", "<=", ">", "<", "!=", "=="
        elif ((caracter == ">") or (caracter == "<") or (caracter == "=") or (caracter == "!")):
            if (palavra != ""):
                lexemas.append(palavra)
            palavra = caracter
            caracter = arquivo.read(1)
            # caso o caracter lido seja "=", o operador inteiro é armazado na lista de lexemas
            if (caracter == "="):
                palavra = palavra + caracter
                lexemas.append(palavra)
            else:
                lerCaracter = False
                lexemas.append(palavra)
            palavra = ""

        # condição usada para verificar o operador aritmético "/" para divisão
        elif (caracter == "/"):
            if (palavra != ""):
                lexemas.append(palavra)
                palavra = ""
            palavra = caracter
            caracter = arquivo.read(1)
            # caso o caracter seguinte a "/" seja "*" significa que temos um comentário,
            # dessa forma, nada lido até "*/" é considerado para a lista de lexemas
            if (caracter == "*"):
                terminouComentario = False
                while (not(terminouComentario)):
                    caracter = arquivo.read(1)
                    if (caracter == "*"):
                        caracter = arquivo.read(1)
                        while (caracter == "*"):
                            caracter = arquivo.read(1)
                            if (caracter == "/"):
                                terminouComentario = True
                        if (caracter == "/"):
                            terminouComentario = True
            else:
                lexemas.append(palavra)
            palavra = ""

        # condição usada para verificar os operadores aritméticos "+" e "-"
        elif ((caracter == "+") or (caracter == "-")):
            if (palavra != ""):
                lexemas.append(palavra)
                palavra = ""
            palavra = caracter
            caracter = arquivo.read(1)
            # entrar nesse if significa que o operador aritmético é para indicar se o número
            # lido posteriormente é positivo ou negativo
            if ((ord(caracter) >= ord("0")) and (ord(caracter) <= ord("9"))):
                lendoNumero = True
                palavra = palavra + caracter
                while (lendoNumero):
                    caracter = arquivo.read(1)
                    if ((ord(caracter) >= ord("0")) and (ord(caracter) <= ord("9"))):
                        palavra = palavra + caracter
                    else:
                        lendoNumero = False
                        lerCaracter = False
            else:
                lerCaracter = False
        # o caracter lido é concatenado à palavra caso não satisfaza nenhuma das condições anteriores
        else:
            palavra = palavra + caracter

        # se o caracter lido for vazio, significa que o arquivo terminou e o while então termina sua execução
        if (caracter == ""):
            if (palavra != ""):
                lexemas.append(palavra)
            lendoArquivo = False

    print(lexemas)
    return lexemas

def main():
    nomeArquivo = input("Nome arquivo: ")
    lexemas = leArquivo(nomeArquivo)

if __name__ == "__main__":
    main()