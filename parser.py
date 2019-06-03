# -*- coding: utf-8 -*-

class Parser:
    def __init__(self, tokens, tabelaDeSimbolos):
        self.tokens = tokens # Lista de todos os tokens lidos do arquivo
        self.tokenAtual = "" # Token sendo analisado no momento
        self.posicaoAtual = 0 # Posição do token atual na lista "tokens"
        self.errosAtuais = []
        self.tabelaDeSimbolos = tabelaDeSimbolos

    def match(self, tokenEsperado): # OK
        if (self.tokenAtual == tokenEsperado):
            return True
        return False

    def proximoToken(self): # OK
        if ((self.posicaoAtual >= len(self.tokens)) or self.posicaoAtual == -1):
            self.posicaoAtual = -1
            return False
        else:
            if ((self.tokens[self.posicaoAtual].tipo == "identificador") or (self.tokens[self.posicaoAtual].tipo == "constNumerica")):
                self.tokenAtual = self.tabelaDeSimbolos[self.tokens[self.posicaoAtual].valor - 1][1]
            else:
                self.tokenAtual = self.tokens[self.posicaoAtual].valor
            self.posicaoAtual += 1
        # print("\nproximoToken(): ", self.tokenAtual, "\n")

    def erro(self): # sem OK, porque não sei como vamos fazer
        self.errosAtuais.append("Erro sintático na linha " + str(self.tokens[self.posicaoAtual - 1].linha)
                                + " e coluna " + str(self.tokens[self.posicaoAtual - 1].coluna) + " : "
                                + str(self.tokens[self.posicaoAtual - 1].valor))

    def removeErrosRepetidos(self): # sem OK, porque não sei como vamos fazer
        self.errosAtuais = list(set(self.errosAtuais)) # remove elementos repetidos

    def voltaPosicao(self, indice): # OK
        self.posicaoAtual = indice - 1
        self.proximoToken()

    def programa(self): # OK
        self.proximoToken()
        if (self.declaracaoLista()):
            print("TUDO CERTO")
        else:
            self.removeErrosRepetidos()
            for i in range(len(self.errosAtuais)):
                print(self.errosAtuais[i])
            print("TUDO ERRADO")

    def declaracaoLista(self): # OK
        if (self.declaracao()):
            self.proximoToken()
            aux = True
            while (self.posicaoAtual != -1):
                if not(self.declaracao()):
                    aux = False
                self.proximoToken()
            return aux
        else:
            return False

    def declaracao(self): # OK
        indice = self.posicaoAtual
        if (self.var_declaracao()):
            print("VAR_DECLARACAO")
            return True
        
        self.voltaPosicao(indice)
        if (self.fun_declaracao()):
            print("FUN_DECLARACAO()")
            return True
        return False

    def var_declaracao(self): # OK
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
                    self.errosAtuais.append(self.erro())
                    return False
        else:
            return False
    
    def tipo_especificador(self): # OK
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

    def atributos_declaracao(self): # OK
        retorno = self.var_declaracao()
        self.proximoToken()
        while (retorno):
            if (self.tokenAtual == "}"):
                return True
            retorno = self.var_declaracao()
            self.proximoToken()
        return retorno

    def fun_declaracao(self): # OK
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
        return False

    def params(self): # OK
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

    def param_lista(self): # OK
        if (self.param()):
            while (self.match(",")):
                self.proximoToken()
                if not(self.param()):
                    return False
            return True
        else:
            self.erro()
            return False

    def param(self): # OK
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

    def composto_decl(self): # Ok
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

    def local_declaracoes(self): # OK
        continua = self.var_declaracao()
        while (continua):
            indice = self.posicaoAtual
            self.proximoToken()
            continua = self.var_declaracao()
            if not(continua):
                self.posicaoAtual = indice - 1
                self.proximoToken()
        return True

    def comando_lista(self): # OK
        continua = self.comando()
        while (continua):
            indice = self.posicaoAtual
            self.proximoToken()
            continua = self.comando()
            if not(continua):
                self.posicaoAtual = indice - 1
                self.proximoToken()
        return True
        
    def comando(self): # OK
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
    
    def expressao_decl(self): # OK
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

    def selecao_decl(self): # OK
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

    def iteracao_decl(self): # OK
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

    def retorno_decl(self): # OK
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
    
    def expressao(self): # OK
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
    
    def var(self): # OK
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
                self.voltaPosicao(indice)
                return True
        else:
            return False

    def expressao_simples(self): # OK
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

    def relacional(self): # OK
        if ((self.match("<=")) or (self.match("<")) or (self.match(">"))
           or (self.match(">=")) or (self.match("==")) or (self.match("!="))):
            return True
        else:
            return False

    def expressao_soma(self): # OK
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
    
    def soma(self): # OK
        if ((self.match("+")) or (self.match("-"))):
            return True
        else:
            return False

    def termo(self): # OK
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

    def mult(self): # OK
        if ((self.match("*")) or (self.match("/"))):
            return True
        else:
            return False

    def fator(self): # OK
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
            # print("\n\n                   É ATIVAÇÃO\n\n")
            return True

        self.voltaPosicao(indice)
        if (self.var()):
            # print("\n\n                   É VAR\n\n")
            return True
        
        self.voltaPosicao(indice)
        if (self.num()):
            # print("\n\n                   É NÚMERO\n\n")
            return True

        self.voltaPosicao(indice)
        if (self.num_int()):
            # print("\n\n                   É NÚMERO INT\n\n")
            return True

        self.erro()
        return False

    def ativacao(self): # OK
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

    def args(self): # OK
        return self.arg_lista()
        
    def arg_lista(self): # OK
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
    
    def num(self): # A TERMINAR
        numero = self.tokenAtual
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

                indice = self.posicaoAtual
                self.proximoToken()
                if (self.match(".")):
                    self.proximoToken()
                    i = 1
                    numero = self.tokenAtual
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
                        numero = self.tokenAtual
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

                self.voltaPosicao(indice)
                return aux
            else:
                return False
        else:
            return False

    # [+ | -] <dígito> {<dígito>} [. <dígito> {<dígito>}] [E [+ | -] <dígito> {<dígito>}]

    def num_int(self): # OK
        i = 1
        numero = self.tokenAtual
        numero = str(numero)
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
            return False

    def digito(self): # OK
        if ((self.match("0")) or (self.match("1")) or (self.match("2")) or (self.match("3"))
           or (self.match("4")) or (self.match("5")) or (self.match("6")) or (self.match("7"))
           or (self.match("8")) or (self.match("9"))):
            return True
        else:
            self.erro()
            return False
    
    def ident(self): # OK
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
            return False
        
    def letra(self): # OK
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

    def abre_chave(self): # OK
        if not(self.match("{")):
            # self.erro()
            return False
        return True

    def fecha_chave(self): # OK
        if not(self.match("}")):
            # self.erro()
            return False
        return True

    def abre_colchete(self): # OK
        if not(self.match("[")):
            # self.erro()
            return False
        return True
    
    def fecha_colchete(self): # OK
        if not(self.match("]")):
            # self.erro()
            return False
        return True
