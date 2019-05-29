# -*- coding: utf-8 -*-

class Parser:
    def __init__(self, tokens, tabelaDeSimbolos):
        self.tokens = tokens # Lista de todos os tokens lidos do arquivo
        self.tokenAtual = "" # Token sendo analisado no momento
        self.posicaoAtual = 0 # Posição do token atual na lista "tokens"
        self.tabelaDeSimbolos = tabelaDeSimbolos

    def match(self, tokenEsperado):
        if (self.tokenAtual == tokenEsperado):
            return True
        return False

    def proximoToken(self):
        if (self.posicaoAtual >= len(self.tokens)):
            self.posicaoAtual = -1
        else:
            if (self.tokens[self.posicaoAtual].tipo == "identificador"):
                self.tokenAtual = self.tabelaDeSimbolos[self.tokens[self.posicaoAtual].valor - 1][1]
            else:
                self.tokenAtual = self.tokens[self.posicaoAtual].valor
            self.posicaoAtual += 1

    def programa(self):
        self.proximoToken()
        if (self.declaracaoLista()):
            print("TUDO CERTO")
        else:
            print("TUDO ERRADO")

    def declaracaoLista(self):
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

    def declaracao(self):
        indice = self.posicaoAtual
        if (self.var_declaracao()):
            print("VAR_DECLARACAO")
            return True
        elif (self.fun_declaracao()):
            self.posicaoAtual = indice
            print("FUN_DECLARACAO()")
            return True
        else:
            return False

    def var_declaracao(self):
        if (self.tipo_especificador()):
            self.proximoToken()
            if (self.ident()):
                self.proximoToken()
                if (self.match(";")):
                    print("A")
                    return True
                elif (self.abre_colchete()):
                    print("B")
                    self.proximoToken()
                    if (self.num_int()):
                        print("C")
                        self.proximoToken()
                        if (self.fecha_colchete()):
                            print("D")
                            self.proximoToken()
                            while (self.abre_colchete()):
                                print("E")
                                self.proximoToken()
                                if (self.num_int()):
                                    print("F")
                                    self.proximoToken()
                                    if (self.fecha_colchete()):
                                        print("G")
                                        self.proximoToken()
                                        return self.match(";")
        #~ return False
    
    def tipo_especificador(self):
        if ((self.match("int")) or (self.match("float")) or (self.match("char")) or (self.match("void"))):
            return True
        elif (self.match("struct")):
            if (self.ident()):
                if (self.abre_chave()):
                    if (self.atributos_declaracao()):
                        if (self.fecha_chave()):
                            print("NADA")
        else:
            return False

    # def atributos_declaracao(self):
        


    # def fun_declaracao(self):
    #     self.tipo_especificador()
    #     self.proximoToken()
    #     self.ident()
    #     self.proximoToken()
    #     if (self.match("(")):
    #         self.proximoToken()
    #         self.params()
    #         self.proximoToken()
    #         if (self.match(")")):
    #             self.proximoToken()
    #             self.composto_decl()

    # def params(self):
        
    # def param_lista(self):

    # def param(self):

    # def composto_decl(self):
    #     if (self.abre_chave()):
    #         self.proximoToken()
    #         self.local_declaracoes()
    #         self.proximoToken()
    #         self.comando_lista()
    #         self.proximoToken()
    #         self.fecha_chave()

    
    # def local_declaracoes(self):

    # def comando_lista(self):
        
    # def comando(self):
    
    # def expressao_decl(self):

    # def selecao_decl(self):

    # def iteracao_decl(self):

    # def retorno_decl(self):

    # def expressao(self):
    
    def var(self):
        ident()
        self.proximoToken()
        if (self.abre_colchete()):
            self.proximoToken()
            if (self.expressao()):
                self.proximoToken()
                if (self.fecha_colchete()):
                    self.proximoToken()
                    while (self.abre_colchete()):
                        self.proximoToken()
                        if (self.expressao()):
                            self.proximoToken()
                            if not(self.fecha_colchete()):
                                return False
                        else:
                            return False
                    return True
        return False

    # def expressao_simples(self):

    def relacional(self):
        if ((self.match("<=")) or (self.match("<")) or (self.match(">"))
           or (self.match(">=")) or (self.match("==")) or (self.match("!="))):
            return True
        else:
            return False

    # def expressao_soma(self):
    
    def soma(self):
        if ((self.match("+")) or (self.match("-"))):
            return True
        else:
            return False

    # def termo(self):

    def mult(self):
        if ((self.match("*")) or (self.match("/"))):
            return True
        else:
            return False

    # def fator(self):
    #     if(self.match("("))
    #         self.expressao()


    # def ativacao(self):

    # def args(self):
        
    # def arg_lista(self):
    
    def num(self): # A TERMINAR
        if ((self.match("+")) or (self.match("-"))):
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
                print("QUERO IR EMBORA")
                return False

    def num_int(self):
        i = 1
        numero = self.tokenAtual
        numero = str(numero)
        self.tokenAtual = numero[0]
        if (self.digito()):
            print("ENTREI AUQD")
            aux = True
            while (i < len(numero)):
                self.tokenAtual = numero[i]
                if not(self.digito()):
                    print("FALSO CARLAHAO")
                    aux = False
                i += 1
            return aux
        else:
            print("QUERO IR EMBORA")
            return False

    def digito(self):
        if ((self.match("0")) or (self.match("1")) or (self.match("2")) or (self.match("3"))
           or (self.match("4")) or (self.match("5")) or (self.match("6")) or (self.match("7"))
           or (self.match("8")) or (self.match("9"))):
            print("MEU DEOS DO CEU")
            return True
        else:
            print("PUTA QUE APRU abaporu")
            return False
    
    def ident(self):
        i = 1
        palavra = self.tokenAtual
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
        
    def letra(self):
        if ((self.match("a")) or (self.match("b")) or (self.match("c")) or (self.match("d")) or (self.match("e"))
           or (self.match("f")) or (self.match("g")) or (self.match("h")) or (self.match("i")) or (self.match("j"))
           or (self.match("k")) or (self.match("l")) or (self.match("m")) or (self.match("n")) or (self.match("o"))
           or (self.match("p")) or (self.match("q")) or (self.match("r")) or (self.match("s")) or (self.match("t"))
           or (self.match("u")) or (self.match("v")) or (self.match("w")) or (self.match("x")) or (self.match("y"))
           or (self.match("z"))):
            return True
        else:
            return False

    def abre_chave(self):
        return self.match("{")

    def fecha_chave(self):
        return self.match("}")

    def abre_colchete(self):
        return self.match("[")
    
    def fecha_colchete(self):
        return self.match("]")
