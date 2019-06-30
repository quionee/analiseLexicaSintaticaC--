# -*- coding: utf-8 -*-

class CodigoTresEnderecos:
    def __init__(self, tokens, tabelaDeSimbolos):
        self.listaComandos = []  # lista de todos os comandos de atribuição
        self.tabelaCodigos = []
        self.percorreTokens(tokens, tabelaDeSimbolos)
        self.constroiTabela()
    
    def percorreTokens(self, tokens, tabelaDeSimbolos):
        i = 0
        while (i < len(tokens)):
            if (tokens[i].valor == "="):
                listaComando = []
                listaComando.append(tabelaDeSimbolos[tokens[i - 1].valor-1][1])
                listaComando.append(tokens[i].valor)
                j = i + 1
                while (tokens[j].valor != ";"):
                    if (tokens[j].tipo == "constNumerica" or tokens[j].tipo == "identificador"):
                        listaComando.append(tabelaDeSimbolos[tokens[j].valor-1][1])
                    elif (tokens[j].valor != "(" and tokens[j].valor != ")"):
                        listaComando.append(tokens[j].valor)
                    j += 1
                print("NAO ENTREI")
                self.listaComandos.append(listaComando)
                i = j
            i += 1

    def constroiTabela(self):
        idT = 0
        for comando in self.listaComandos:
            if (len(comando) == 5):
                comando.remove('=')
                self.tabelaCodigos.append(comando)  
            elif (len(comando) < 5):
                for i in range (4 - len(comando)):
                    comando.append(' ')
                self.tabelaCodigos.append(comando)
            elif (len(comando) > 5):
                comando.remove("=")
                while (len(comando) > 4):
                    ehVezes = False
                    indice = 0
                    aux = []
                    i = 0
                    while ((i < len(comando) - 1) and (not ehVezes)):
                        if ((comando[i] == "*") or (comando[i] == "/")):
                            aux.append('t' + str(idT))
                            aux.append(comando[i - 1])
                            aux.append(comando[i])
                            aux.append(comando[i + 1])
                            ehVezes = True
                            indice = i
                            print("AUX",aux)
                        i += 1
                    if (not ehVezes):
                        for i in range(len(comando)):
                            if((comando[i] == "+") or (comando[i] == "-")):
                                aux.append('t' + str(idT))
                                aux.append(comando[i - 1])
                                aux.append(comando[i])
                                aux.append(comando[i + 1])
                                indice = i

                    self.tabelaCodigos.append(aux)
                    #aux.remove(aux[0])
                    print("INDICE: ", indice)
                    comando[indice - 1] = 't' + str(idT)
                    #comando = list(comando - aux)
                    for token in comando:
                        if token in aux:
                            comando.remove(token)
                    #print("COMANDO", comando)
                    idT += 1
                comando[indice-1] = 't' + str(idT - 1)
                self.tabelaCodigos.append(comando)
       # print(self.tabelaCodigos)

        for comando in self.tabelaCodigos:
            print("\n",comando)
    
        