from tabelaDirecionada import *
from token import Token
from tabelaDeSimbolos import TabelaDeSimbolos

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
    lerCaracter = False
    # while roda enquanto há algo para ler do arquivo
    qtdLinhas = 1
    qtdColunas = -1

    caracterAux = "A"
    caracter = arquivo.read(1)
    while (lendoArquivo):
        if (lerCaracter): # se "lerCaracter" == true, um caracter é lido
            caracterAux = caracter
            caracter = arquivo.read(1)
            qtdColunas += 1
        else: # se "lerCaracter" == false, nada é lido
            lerCaracter = True

        print("caracterAux: ", caracterAux, "\ncaracter: ", caracter)

        # se o caracter lido for vazio, significa que o arquivo terminou e o while então termina sua execução
        if (caracter == ""):
            if (palavra != ""):
                lexemas.append(palavra)
            lendoArquivo = False

        # condição usada para ignorar espaços em branco e tabulações
        # caso seja uma dessas opções, a palavra lida até então é armazenada na lista de lexemas
        elif ((caracter == " ") or (caracter == "\t")):
            # condição utilizada para verificar se a palavra está vazia, caso não esteja,
            # ela é armazenada na lista de lexemas
            if (palavra != ""):
                lexemas.append(palavra)
                palavra = ""

        # condição usada para verificar quebras de linha
        # a variável qtdLinhas é incrementada
        elif (caracter == "\n"):
            qtdLinhas += 1
            qtdColunas -= 1
            # print ("qtdColunas: ", qtdColunas)
            # print ("qtdLinhas: ", qtdLinhas, "\n")
            qtdColunas = -1
            # condição utilizada para verificar se a palavra está vazia, caso não esteja,
            # ela é armazenada na lista de lexemas
            if (palavra != ""):
                lexemas.append(palavra)
                palavra = ""

        # condição usada para verificar os delimitadores "{", "[", "}", "]", ";",
        # e o operador aritmético "*"
        elif ((caracter == "{") or (caracter == "[") or (caracter == "}") or (caracter == "]")
        or (caracter == "(") or (caracter == ")") or (caracter == "*") or (caracter == ";")):
            if (palavra != ""):
                lexemas.append(palavra)
                palavra = ""
            lexemas.append(caracter)

        # condição usada para verificar os operadores relacionais ">=", "<=", ">", "<", "!=", "=="
        elif ((caracter == ">") or (caracter == "<") or (caracter == "=") or (caracter == "!")):
            if (palavra != ""):
                lexemas.append(palavra)
            palavra = caracter
            caracterAux = caracter
            caracter = arquivo.read(1)
            qtdColunas += 1
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

            if (caracter == "\n"):
                qtdLinhas += 1
                # print ("qtdColunas: ", qtdColunas)
                # print ("qtdLinhas: ", qtdLinhas, "\n")
                qtdColunas = -1
            else:
                qtdColunas += 1

            # caso o caracter seguinte a "/" seja "*" significa que temos um comentário,
            # dessa forma, nada lido até "*/" é considerado para a lista de lexemas
            if (caracter == "*"):
                terminouComentario = False
                caracter = arquivo.read(1)

                if (caracter == "\n"):
                    qtdLinhas += 1
                    # print ("qtdColunas: ", qtdColunas)
                    # print ("qtdLinhas: ", qtdLinhas, "\n")
                    qtdColunas = -1
                else:
                    qtdColunas += 1
                
                while (not(terminouComentario)):
                    caracterAux = caracter
                    caracter = arquivo.read(1)

                    if (caracter == "\n"):
                        qtdLinhas += 1
                        # print ("qtdColunas: ", qtdColunas)
                        # print ("qtdLinhas: ", qtdLinhas, "\n")
                        qtdColunas = -1
                    else:
                        qtdColunas += 1

                    if (caracterAux == "*"):
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

            qtdColunas += 1
            
            # entrar nesse if significa que o operador aritmético é para indicar se o número
            # lido posteriormente é positivo ou negativo
            if ((ord(caracter) >= ord("0")) and (ord(caracter) <= ord("9"))):
                lendoNumero = True
                palavra = palavra + caracter
                while (lendoNumero):
                    caracter = arquivo.read(1)
                    qtdColunas += 1
                    if ((ord(caracter) >= ord("0")) and (ord(caracter) <= ord("9"))):
                        palavra = palavra + caracter
                    else:
                        lendoNumero = False
                        lerCaracter = False
            else:
                lerCaracter = False

        elif ((ord(caracter) >= ord("a")) and (ord(caracter) <= ord("z"))):
            palavra = palavra + caracter
            caracter = arquivo.read(1)
            while (((ord(caracter) >= ord("0")) and (ord(caracter) <= ord("9"))) or ((ord(caracter) >= ord("a")) and (ord(caracter) <= ord("z")))):
                palavra = palavra + caracter
                caracter = arquivo.read(1)
            lerCaracter = False

        # condição usada para ler números e tratar erros léxicos
        elif (not((ord(caracter) >= ord("a")) and (ord(caracter) <= ord("z")))):
            print("CARALHOOOOOOOOOOOO")
            colunaAtual = qtdColunas
            if ((ord(caracter) >= ord("0")) and (ord(caracter) <= ord("9"))):
                palavra = palavra + caracter
                terminouNumero = False
                while (not(terminouNumero)):
                    caracter = arquivo.read(1)
                    qtdColunas += 1
                    if ((ord(caracter) >= ord("0")) and (ord(caracter) <= ord("9"))):
                        palavra = palavra + caracter
                    elif (((ord(caracter) >= ord("a")) and (ord(caracter) <= ord("z")))):
                        palavra = ""
                        terminou = False
                        while (not(terminou)):
                            caracter = arquivo.read(1)
                            qtdColunas += 1
                            if ((caracter == " ") or (caracter == "\t")):
                                terminou = True
                            elif ((caracter == "\n") or (caracter == "")):
                                qtdLinhas += 1
                                # print ("qtdColunas: ", qtdColunas)
                                # print ("qtdLinhas: ", qtdLinhas, "\n")
                                qtdColunas = -1
                                terminou = True
                        terminouNumero = True
                        print("\n*** Erro lexico na linha ", qtdLinhas, " coluna ", colunaAtual, " ***")
                    else:
                        lerCaracter = False
                        terminouNumero = True
                    

        # o caracter lido é concatenado à palavra caso não satisfaza nenhuma das condições anteriores
        else:
            palavra = palavra + caracter

    return lexemas

def criaTokens(lexemas, tabelaDeTransicao, tabelaDeSimbolos):
    tokens = []

    for i in range(len(lexemas)): # verificação de todos do lexemas
        tipo = verifica(lexemas[i], tabelaDeTransicao)
        valor = lexemas[i]
        if (tipo == "identificador") or (tipo == "constNumerica"):
            valor = tabelaDeSimbolos.adiciona(lexemas[i], tipo)
        tokens.append(Token(tipo, valor))

    return tokens

def criaTabelaDeSimbolos():
    tabelaDeSimbolos = TabelaDeSimbolos()
    return tabelaDeSimbolos

def main():
    nomeArquivo = input("Nome arquivo: ")
    
    lexemas = leArquivo(nomeArquivo)
    print(lexemas)
    
    tabelaDeTransicao = geraTabelaDirecionada() # tabela preenchida
    #~ imprimeTabela(tabelaDeTransicao)
    
    tabelaDeSimbolos = criaTabelaDeSimbolos()
    
    tokens = criaTokens(lexemas, tabelaDeTransicao, tabelaDeSimbolos)
    print("\n\n  ----- Tokens -----\n")
    for i in range(len(tokens)):
        tokens[i].imprime()
       
    tabelaDeSimbolos.imprime()
    

if __name__ == "__main__":
    main()
