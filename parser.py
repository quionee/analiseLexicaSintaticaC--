# -*- coding: utf-8 -*-

class Parser:
    def __init__(self, tokens, tabelaDeSimbolos):
        self.tokens = tokens # lista de todos os tokens lidos do arquivo
        self.tokenAtual = "" # token sendo analisado no momento
        self.posicaoAtual = 0 # posição do token atual na lista "tokens"
        self.errosAtuais = [] # lista utilizada para guardar os erros encontrados
        self.tabelaDeSimbolos = tabelaDeSimbolos # tabela de símbolos
        self.paraExcluir = [] # indíces da tabela de símbolos que serão excluídos

    # método auxilizar que verifica se o token esperado pelo analisado é o token a ser analisado,
    # retorna True se sim, False se não
    def match(self, tokenEsperado):
        if (self.tokenAtual == tokenEsperado):
            return True
        return False

    # método auxiliar que faz a leitura do próximo token
    def proximoToken(self):
        if ((self.posicaoAtual >= len(self.tokens)) or self.posicaoAtual == -1):
            self.posicaoAtual = -1
            return False
        else:
            if ((self.tokens[self.posicaoAtual].tipo == "identificador") or (self.tokens[self.posicaoAtual].tipo == "constNumerica")):
                self.tokenAtual = self.tabelaDeSimbolos[self.tokens[self.posicaoAtual].valor - 1][1]
            else:
                self.tokenAtual = self.tokens[self.posicaoAtual].valor
            self.posicaoAtual += 1

    # método auxiliar que adiciona os erros encontrado em self.errosAtuais
    def erro(self):
        if ((self.tokens[self.posicaoAtual - 1].tipo == "identificador") or
            (self.tokens[self.posicaoAtual - 1].tipo == "constNumerica")):
            self.errosAtuais.append("Erro sintático na linha " + str(self.tokens[self.posicaoAtual - 1].linha)
                                    + " e coluna " + str(self.tokens[self.posicaoAtual - 1].coluna) + " : "
                                    + str(self.tabelaDeSimbolos[int(self.tokens[self.posicaoAtual - 1].valor) - 1][1]))
        else:
            self.errosAtuais.append("Erro sintático na linha " + str(self.tokens[self.posicaoAtual - 1].linha)
                                    + " e coluna " + str(self.tokens[self.posicaoAtual - 1].coluna) + " : "
                                    + str(self.tokens[self.posicaoAtual - 1].valor))

    # método auxiliar para remover erros repetidos de self.errosAtuais
    def removeErrosRepetidos(self):
        self.errosAtuais = list(set(self.errosAtuais)) # remove elementos repetidos

    # método auxiliar para verificar se o expoente ao qual um número está elevado está correto,
    # retorna True se sim, False se não
    def verificaExpoente(self, indiceExpoente, expoente):
        indice = self.posicaoAtual
        self.proximoToken()
        indiceExpoente[0] = int(self.tokens[self.posicaoAtual - 1].valor - 1)
        numero = self.tokenAtual
        expoente[0] = numero
        self.tokenAtual = numero[0]
        if ((self.match("+")) or (self.match("-")) or (self.digito())):
            i = 1
            if not(self.digito()):
                self.tokenAtual = numero[1]
                i += 1
            if (self.digito()):
                aux = True
                while (i < len(numero)):
                    self.tokenAtual = numero[i]
                    if not(self.digito()):
                        # GENTE, acredito que ele nunca vá entrar aqui
                        aux = False
                    i += 1
                return aux
        else:
            self.voltaPosicao(indice)
            return False

    # método auxiliar para verificar se um número com vírgula (utilizamos '.' na representação)
    # está correto, retorna True se sim, False se não
    def verificaPontoFlutuante(self, indiceMantissa, mantissa):
        self.proximoToken()
        indiceMantissa[0] = int(self.tokens[self.posicaoAtual - 1].valor - 1)
        i = 1
        numero = self.tokenAtual
        mantissa[0] = numero
        self.tokenAtual = numero[0]

        if (self.digito()):
            aux = True
            while (i < len(numero)):
                self.tokenAtual = numero[i]
                if not(self.digito()):
                    # GENTE, acredito que ele nunca vá entrar aqui
                    aux = False
                i += 1

        indice = self.posicaoAtual
        self.proximoToken()
        if (self.match("E")):
            expoente = [0]
            indiceExpoente = [0]
            if (self.verificaExpoente(indiceExpoente, expoente)):
                mantissa[0] = mantissa[0] + "E" + expoente[0]
                self.paraExcluir.append(indiceExpoente[0])
                return True
            return False

        else:
            self.voltaPosicao(indice)
            return aux

    # método auxiliar utilizado para retornar a uma posição da lista de tokens, isso acontece durante
    # as tentativas de métodos para encontrar algum que encaixe na sequência de tokens
    def voltaPosicao(self, indice):
        self.posicaoAtual = indice - 1
        self.proximoToken()

    def programa(self):
        print()
        self.proximoToken()
        if (self.declaracaoLista()):
            print("\n\nO código do arquivo não contém erros sintáticos\n")
            self.paraExcluir.sort(key = int, reverse = True)
            for i in range(len(self.paraExcluir)):
                del self.tabelaDeSimbolos[self.paraExcluir[i]]
        else:
            print("\n\nO código do arquivo contém erros sintáticos\n")
            # self.removeErrosRepetidos()
            # for i in range(len(self.errosAtuais)):
            #     print(self.errosAtuais[i])

    def declaracaoLista(self):
        continuaDeclaracao = self.declaracao()
        if (True):
            self.proximoToken()
            aux = True
            while (self.posicaoAtual != -1):
                continuaDeclaracao = self.declaracao()
                if not(continuaDeclaracao):
                    if ((self.tokens[self.posicaoAtual - 1].tipo == "identificador")
                        or (self.tokens[self.posicaoAtual - 1].tipo == "constNumerica")):
                        print("Erro sintático na linha " + str(self.tokens[self.posicaoAtual - 1].linha)
                              + " e coluna " + str(self.tokens[self.posicaoAtual - 1].coluna) + " : "
                              + str(self.tabelaDeSimbolos[int(self.tokens[self.posicaoAtual - 1].valor) - 1][1]))
                    else:
                        print("Erro sintático na linha " + str(self.tokens[self.posicaoAtual - 1].linha)
                              + " e coluna " + str(self.tokens[self.posicaoAtual - 1].coluna) + " : "
                              + str(self.tokens[self.posicaoAtual - 1].valor))
                    aux = False
                    self.proximoToken()
                    while (((self.tokenAtual != "{") and (self.tokenAtual != ";") and (self.tokenAtual != "}"))
                           and (self.posicaoAtual != -1)):
                        self.proximoToken()
                    continuaDeclaracao = True
                self.proximoToken()
            return aux
        else:
             return False

    def declaracao(self):
        indice = self.posicaoAtual
        if (self.var_declaracao()):
            return True
        
        self.voltaPosicao(indice)
        if (self.fun_declaracao()):
            return True
        
        return False

    def var_declaracao(self):
        indice = self.posicaoAtual
        if (self.tipo_especificador()):
            self.proximoToken()
            if (self.ident()):
                self.proximoToken()
                if (self.match(";")):
                    return True
                elif (self.abre_colchete()):
                    self.proximoToken()
                    if (self.num_int()):
                        self.proximoToken()
                        if (self.fecha_colchete()):
                            self.proximoToken()
                            if (self.match(";")):
                                return True
                            while (self.abre_colchete()):
                                self.proximoToken()
                                if (self.num_int()):
                                    self.proximoToken()
                                    if (self.fecha_colchete()):
                                        self.proximoToken()
                                        return self.match(";")
                                    else:
                                        self.erro()
                                        return False
                                else:
                                    self.erro()
                                    return False
                            else:
                                self.erro()
                                return False
                        else:
                            self.erro()
                            return False
                    else:
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False
    
    def tipo_especificador(self):
        if ((self.match("int")) or (self.match("float")) or (self.match("char")) or (self.match("void"))):
            return True
        elif (self.match("struct")):
            self.proximoToken()
            if (self.ident()):
                self.proximoToken()
                if (self.abre_chave()):
                    self.proximoToken()
                    if (self.atributos_declaracao()):
                        if (self.fecha_chave()):
                            return True
                        else:
                            self.erro()
                            return False
                    else:
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False

    def atributos_declaracao(self):
        retorno = self.var_declaracao()
        self.proximoToken()
        while (retorno):
            if (self.tokenAtual == "}"):
                return True
            retorno = self.var_declaracao()
            self.proximoToken()
        return retorno

    def fun_declaracao(self):
        if (self.tipo_especificador()):
            self.proximoToken()
            if (self.ident()):
                self.proximoToken()
                if (self.match("(")):
                    self.proximoToken()
                    if (self.params()):
                        if (self.match(")")):
                            self.proximoToken()
                            if (self.composto_decl()):
                                return True
                            else:
                                self.erro()
                                return False
                        else:
                            self.erro()
                            return False
                    else:
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False

    def params(self):
        indice = self.posicaoAtual
        if (self.param_lista()):
            return True

        self.posicaoAtual = indice - 1
        self.proximoToken()
        
        if (self.match("void")):
            self.proximoToken()
            return True

        self.erro()
        return False

    def param_lista(self):
        if (self.param()):
            while (self.match(",")):
                self.proximoToken()
                if not(self.param()):
                    self.erro()
                    return False
            return True
        else:
            self.erro()
            return False

    def param(self):
        if (self.tipo_especificador()):
            self.proximoToken()
            if (self.ident()):
                self.proximoToken()
                if (self.abre_colchete()):
                    self.proximoToken()
                    if (self.fecha_colchete()):
                        self.proximoToken()
                        return True
                    else:
                        self.erro()
                        return False
                else:
                    return True
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False

    def composto_decl(self):
        if (self.abre_chave()):
            self.proximoToken()
            if (self.local_declaracoes()):
                if (self.comando_lista()):
                    self.proximoToken()
                    if (self.fecha_chave()):
                        return True
                    else: 
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else: 
            self.erro()
            return False

    def local_declaracoes(self):
        continua = self.var_declaracao()
        while (continua):
            indice = self.posicaoAtual
            self.proximoToken()
            continua = self.var_declaracao()
            if not(continua):
                self.posicaoAtual = indice - 1
                self.proximoToken()
        return True

    def comando_lista(self):
        continua = self.comando()
        while (continua):
            indice = self.posicaoAtual
            self.proximoToken()
            continua = self.comando()
            if not(continua):
                self.posicaoAtual = indice - 1
                self.proximoToken()
        return True
        
    def comando(self):
        indice = self.posicaoAtual
        if (self.expressao_decl()):
            return True

        self.voltaPosicao(indice)
        if (self.composto_decl()):
            return True
        
        self.voltaPosicao(indice)
        if (self.selecao_decl()):
            return True

        self.voltaPosicao(indice)
        if (self.iteracao_decl()):
            return True

        self.voltaPosicao(indice)
        if (self.retorno_decl()):
            return True

        self.erro()
        return False
    
    def expressao_decl(self):
        indice = self.posicaoAtual
        if (self.expressao()):
            if (self.match(";")):
                return True
            else:
                self.erro()
                return False

        self.voltaPosicao(indice)
        if (self.match(";")):
            return True
        
        self.erro()
        return False

    def selecao_decl(self):
        if (self.match("if")):
            self.proximoToken()
            if (self.match("(")):
                self.proximoToken()
                if (self.expressao()):
                    if (self.match(")")):
                        self.proximoToken()
                        if (self.comando()):
                            indice = self.posicaoAtual
                            self.proximoToken()
                            if (self.match("else")):
                                self.proximoToken()
                                if (self.comando()):
                                    return True
                                else:
                                    self.erro()
                                    return False
                            else:
                                self.voltaPosicao(indice)
                                return True
                        else:
                            self.erro()
                            return False
                    else:
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False

    def iteracao_decl(self):
        if (self.match("while")):
            self.proximoToken()
            if (self.match("(")):
                self.proximoToken()
                if (self.expressao()):
                    if (self.match(")")):
                        self.proximoToken()
                        if (self.comando()):
                            return True
                        else:
                            self.erro()
                            return False
                    else:
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False

    def retorno_decl(self):
        if (self.match("return")):
            self.proximoToken()
            if (self.match(";")):
                return True
            elif (self.expressao()):
                if (self.match(";")):
                    return True
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False
    
    def expressao(self):
        indice = self.posicaoAtual
        if (self.var()):
            self.proximoToken()
            if (self.match("=")):
                self.proximoToken()
                if (self.expressao()):
                    return True
                else: 
                    self.erro()
                    return False
            else:
                self.erro()
        
        self.voltaPosicao(indice)
        if (self.expressao_simples()):
            return True
        else:
            self.erro()
            return False
    
    def var(self):
        if (self.ident()):
            indice = self.posicaoAtual
            self.proximoToken()
            if (self.abre_colchete()):
                self.proximoToken()
                if (self.expressao()):
                    if (self.fecha_colchete()):
                        indice = self.posicaoAtual
                        self.proximoToken()
                        while (self.abre_colchete()):
                            self.proximoToken()
                            if (self.expressao()):
                                self.proximoToken()
                                if not(self.fecha_colchete()):
                                    return False
                            else:
                                return False
                        self.voltaPosicao(indice)
                        return True
                    else:
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.voltaPosicao(indice)
                return True
        else:
            self.erro()
            return False

    def expressao_simples(self):
        if (self.expressao_soma()):
            indice = self.posicaoAtual
            if (self.relacional()):
                self.proximoToken()
                if (self.expressao_soma()):
                    return True
                else:
                    self.erro()
                    return False
            else:
                return True
        else:
            self.erro()
            return False

    def relacional(self):
        if ((self.match("<=")) or (self.match("<")) or (self.match(">"))
           or (self.match(">=")) or (self.match("==")) or (self.match("!="))):
            return True
        else:
            self.erro()
            return False

    def expressao_soma(self):
        if (self.termo()):
            self.proximoToken()
            continua = self.soma()
            if (continua):
                while (continua):
                    self.proximoToken()
                    if not(self.termo()):
                        self.erro()
                        return False
                    self.proximoToken()
                    continua = self.soma()
                return True
            else:
                return True
        else:
            self.erro()
            return False
    
    def soma(self):
        if ((self.match("+")) or (self.match("-"))):
            return True
        else:
            self.erro()
            return False

    def termo(self):
        if (self.fator()):
            indice = self.posicaoAtual
            self.proximoToken()
            continua = self.mult()
            if (continua):
                indice1 = self.posicaoAtual
                while (continua):
                    indice = self.posicaoAtual
                    self.proximoToken()
                    if not(self.fator()):
                        self.erro()
                        return False
                    self.proximoToken()
                    continua = self.mult()

                self.voltaPosicao(indice + 1)
                return True
            else:
                self.voltaPosicao(indice)
                return True
        else:
            self.erro()
            return False

    def mult(self):
        if ((self.match("*")) or (self.match("/"))):
            return True
        else:
            self.erro()
            return False

    def fator(self):
        indice = self.posicaoAtual
        if (self.match("(")):
            self.proximoToken()
            if (self.expressao()):
                if (self.match(")")):
                    return True
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False

        if (self.ativacao()):
            return True

        self.voltaPosicao(indice)
        if (self.var()):
            return True
        
        self.voltaPosicao(indice)
        if (self.num()):
            return True

        self.voltaPosicao(indice)
        if (self.num_int()):
            return True

        self.erro()
        return False

    def ativacao(self):
        if (self.ident()):
            self.proximoToken()
            if (self.match("(")):
                self.proximoToken()
                if (self.match(")")):
                    return True
                elif (self.args()):
                    if (self.match(")")):
                        return True
                    else:
                        self.erro()
                        return False
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False

    def args(self):
        return self.arg_lista()
        
    def arg_lista(self):
        if (self.expressao()):
            while (self.match(",")):
                self.proximoToken()
                if not(self.expressao()):
                    self.erro()
                    return False
            return True
        else:
            self.erro()
            return False
    
    def num(self): 
        numero = self.tokenAtual
        self.tokenAtual = numero[0]
        if ((self.match("+")) or (self.match("-")) or (self.digito())):
            i = 1
            if not(self.digito()):
                self.tokenAtual = numero[1]
                i += 1
            
            indiceTabela = int(self.tokens[self.posicaoAtual - 1].valor - 1)
            
            if (self.digito()):
                aux = True
                while (i < len(numero)):
                    self.tokenAtual = numero[i]
                    if not(self.digito()):
                        # GENTE, acredito que ele nunca vá entrar aqui
                        aux = False
                    i += 1

                indice = self.posicaoAtual
                self.proximoToken()
                if (self.match(".")):
                    mantissa = [0]
                    indiceMantissa = [0]
                    if (self.verificaPontoFlutuante(indiceMantissa, mantissa)):
                        self.tabelaDeSimbolos[indiceTabela][1] = numero + "." + mantissa[0]
                        self.paraExcluir.append(indiceMantissa[0])
                        return True
                    self.erro()
                    return False

                elif (self.match("E")):
                    expoente = [0]
                    indiceExpoente = [0]
                    if (self.verificaExpoente(indiceExpoente, expoente)):
                        self.tabelaDeSimbolos[indiceTabela][1] = numero + "E" + expoente[0]
                        self.paraExcluir.append(indiceExpoente[0])
                        return True
                    self.erro()
                    return False

                else:
                    self.voltaPosicao(indice)
                    return aux
            else:
                self.erro()
                return False
        else:
            self.erro()
            return False

    def num_int(self):
        i = 1
        numero = self.tokenAtual
        self.tokenAtual = numero[0]
        if (self.digito()):
            aux = True
            while (i < len(numero)):
                self.tokenAtual = numero[i]
                if not(self.digito()):
                    aux = False
                i += 1
            return aux
        else:
            self.erro()
            return False

    def digito(self):
        if ((self.match("0")) or (self.match("1")) or (self.match("2")) or (self.match("3"))
           or (self.match("4")) or (self.match("5")) or (self.match("6")) or (self.match("7"))
           or (self.match("8")) or (self.match("9"))):
            return True
        else:
            self.erro()
            return False
    
    def ident(self):
        i = 1
        palavra = self.tokenAtual
        palavra = str(palavra)
        self.tokenAtual = palavra[0]
        if (self.letra()):
            aux = True
            while (i < len(palavra)):
                self.tokenAtual = palavra[i]
                if not((self.letra()) or (self.digito())):
                    aux = False
                i += 1
            return aux
        else:
            self.erro()
            return False
        
    def letra(self):
        if ((self.match("a")) or (self.match("b")) or (self.match("c")) or (self.match("d")) or (self.match("e"))
           or (self.match("f")) or (self.match("g")) or (self.match("h")) or (self.match("i")) or (self.match("j"))
           or (self.match("k")) or (self.match("l")) or (self.match("m")) or (self.match("n")) or (self.match("o"))
           or (self.match("p")) or (self.match("q")) or (self.match("r")) or (self.match("s")) or (self.match("t"))
           or (self.match("u")) or (self.match("v")) or (self.match("w")) or (self.match("x")) or (self.match("y"))
           or (self.match("z"))):
            return True
        else:
            self.erro()
            return False

    def abre_chave(self):
        if not(self.match("{")):
            self.erro()
            return False
        return True

    def fecha_chave(self):
        if not(self.match("}")):
            self.erro()
            return False
        return True

    def abre_colchete(self):
        if not(self.match("[")):
            self.erro()
            return False
        return True
    
    def fecha_colchete(self):
        if not(self.match("]")):
            self.erro()
            return False
        return True