# -*- coding: utf-8 -*-

class CodigoTresEnderecos:
    def __init__(self, tokens, tabelaDeSimbolos):
        self.listaComandos = []  # lista para armazenar todos os comandos de atribuição
        self.tabelaCodigos = []  # tabela final com os códigos de três endereços
        self.percorreTokens(tokens, tabelaDeSimbolos)
        self.constroiTabela()
    
    def percorreTokens(self, tokens, tabelaDeSimbolos):
        i = 0
        while (i < len(tokens)): # lê todos os tokens
            if (tokens[i].valor == "="): # encontra comando que contém '=' (atribuição)
                comando = []
                comando.append(tabelaDeSimbolos[tokens[i - 1].valor-1][1]) # procura identificador ou constante na tabela de símbolos
                comando.append(tokens[i].valor)
                j = i + 1
                while (tokens[j].valor != ";"): # procura por mais termos até o ';' (fim do comando)
                    if (tokens[j].tipo == "constNumerica" or tokens[j].tipo == "identificador"):
                        comando.append(tabelaDeSimbolos[tokens[j].valor-1][1])
                    elif (tokens[j].valor != "(" and tokens[j].valor != ")"):
                        comando.append(tokens[j].valor) 
                    j += 1
                self.listaComandos.append(comando)
                i = j
            i += 1
    
    # formata os comandos em quádruplas e insere na tabela
    def constroiTabela(self):
        idExpressao = 0
        for comando in self.listaComandos:
            # transforma comando em quádrupla retirando o '='
            if (len(comando) == 5):
                comando.remove('=')
                self.tabelaCodigos.append(comando)  
            # transforma comando em quádrupla preenchendo com espaços
            elif (len(comando) < 5):
                for i in range (4 - len(comando)):
                    comando.append(' ') 
                self.tabelaCodigos.append(comando)
            # transforma comando em quádrupla criando outras quádruplas para os termos que estão sobrando
            elif (len(comando) > 5):
                comando.remove("=")
                while (len(comando) > 4):
                    ehVezes = False
                    indice = 0
                    aux = []
                    i = 0
                    while ((i < len(comando) - 1) and (not ehVezes)):
                        if ((comando[i] == "*") or (comando[i] == "/")):
                            aux.append('t' + str(idExpressao))
                            aux.append(comando[i - 1])
                            aux.append(comando[i])
                            aux.append(comando[i + 1])
                            ehVezes = True
                            indice = i
                        i += 1
                    if (not ehVezes):
                        i = 0
                        ehSoma = False
                        while ((i < len(comando) - 1) and (not ehSoma)):
                            if((comando[i] == "+") or (comando[i] == "-")):
                                aux.append('t' + str(idExpressao))
                                aux.append(comando[i - 1])
                                aux.append(comando[i])
                                aux.append(comando[i + 1])
                                ehSoma = True
                                indice = i
                            i += 1

                    self.tabelaCodigos.append(aux)
                    comando[indice] = 't' + str(idExpressao)
                    # remove a parte da expressão que foi colocada em outra quádrupla
                    for token in comando:
                        if (token in aux) and (token != "*") and (token != "+") and (token != "-") and (token != "/"):
                            comando.remove(token)
                    idExpressao += 1

                # parte que sobrou do comando inicial
                comando[indice - 1] = 't' + str(idExpressao - 1)
                self.tabelaCodigos.append(comando)
        #printa tabela códigos linha por linha
        for comando in self.tabelaCodigos:
            print("\n",comando)