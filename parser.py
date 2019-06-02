# -*- coding: utf-8 -*-

class Parser:
    def __init__(self, tokens, tabelaDeSimbolos):
        self.tokens = tokens # Lista de todos os tokens lidos do arquivo
        self.tokenAtual = "" # Token sendo analisado no momento
        self.posicaoAtual = 0 # Posição do token atual na lista "tokens"
        self.errosAtuais = []
        self.tabelaDeSimbolos = tabelaDeSimbolos

    def match(self, tokenEsperado):
        if (self.tokenAtual == tokenEsperado):
            return True
        return False

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

    def erro(self):
        self.errosAtuais.append("Erro sintático na linha " + str(self.tokens[self.posicaoAtual - 1].linha)
                                + " e coluna " + str(self.tokens[self.posicaoAtual - 1].coluna) + " : "
                                + str(self.tokens[self.posicaoAtual - 1].valor))

    def removeErrosRepetidos(self):
        self.errosAtuais = list(set(self.errosAtuais)) # remove elementos repetidos

    def programa(self):
        self.proximoToken()
        if (self.declaracaoLista()):
            print("TUDO CERTO")
        else:
            self.removeErrosRepetidos()
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
        #print ("posicaoAtual: ", self.posicaoAtual)
        #print ("tokenAtual: ", self.tokenAtual)
        if (self.var_declaracao()):
            print("VAR_DECLARACAO")
            return True
        self.posicaoAtual = indice - 1
        self.proximoToken()
        #print ("posicaoAtual Fun: ", self.posicaoAtual)
        #print ("tokenAtual Fun: ", self.tokenAtual)
        if (self.fun_declaracao()):
            print("FUN_DECLARACAO()")
            return True
        else:
            return False

    def var_declaracao(self):
        indice = self.posicaoAtual

        if (self.match("struct")):
            return self.tipo_especificador()

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
                        self.proximoToken()
                        if (self.fecha_chave()):
                            return True;
                        else:
                            self.erro()
                            return False # TERMINAR ISSO AQ
        else:
            self.erro()
            return False

    def atributos_declaracao(self): # ARRUMAR ISSO AQ
        retorno = self.var_declaracao()
        self.proximoToken()
        while(retorno):
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
        return False

    def params(self):
        indice = self.posicaoAtual
        if (self.param_lista()):
            return True

        self.posicaoAtual = indice - 1
        self.proximoToken()
        if (self.match("void")):
            return True

        self.erro()
        return False

    def param_lista(self):
        if (self.param()):
            while (self.match(",")):
                self.proximoToken()
                if not(self.param()):
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
                self.proximoToken()
                if (self.comando_lista()):
                    self.proximoToken()
                    if (self.fecha_chave()):
                        print (self.tokenAtual)
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

    # <composto-decl> ::= <abre-chave> <local-declara¸c˜oes> <comando-lista> <fecha-chave>

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

    # <local-declara¸c˜oes> ::= {<var-declara¸c˜ao>}

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
            
    # <comando-lista> ::= { <comando> }
        
    def comando(self):
        aux = 0
        indice = self.posicaoAtual
        if (self.expressao_decl()):
            print("\nexpressao_decl: ", aux, "\n")
            aux += 1
            return True

        self.posicaoAtual = indice - 1
        self.proximoToken()
        if (self.composto_decl()):
            print("\ncomposto_decl: ", aux, "\n")
            aux += 1
            return True
        
        self.posicaoAtual = indice - 1
        self.proximoToken()
        if (self.selecao_decl()):
            print("\nselecao_decl: ", aux, "\n")
            aux += 1
            return True

        self.posicaoAtual = indice - 1
        self.proximoToken()
        if (self.iteracao_decl()):
            print("\niteracao_decl: ", aux, "\n")
            aux += 1
            return True

        self.posicaoAtual = indice - 1
        self.proximoToken()
        if (self.retorno_decl()):
            print("\nretorno_decl: ", aux, "\n")
            aux += 1
            return True

        self.erro()
        return False

    # <comando> ::= <express˜ao-decl> | <composto-decl> | <sele¸c˜ao-decl> | <itera¸c˜ao-decl> | <retorno-decl>
    
    def expressao_decl(self):
        indice = self.posicaoAtual
        if (self.expressao()):
            if (self.match(";")):
                return True
            else:
                self.erro()
                return False

        self.posicaoAtual = indice - 1
        self.proximoToken()

        if (self.match(";")):
            return True
        
        self.erro()
        return False

    # <express˜ao-decl> ::= <express˜ao> ; | ;

    def selecao_decl(self):
        if (self.match("if")):
            self.proximoToken()
            if (self.match("(")):
                self.proximoToken()
                if (self.expressao()):
                    self.proximoToken()
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
                                self.posicaoAtual = indice - 1
                                self.proximoToken()
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

    # <sele¸c˜ao-decl> ::= if ( <express˜ao> ) <comando> | if ( <express˜ao> ) <comando> else <comando>

    def iteracao_decl(self):
        if (self.match("while")):
            self.proximoToken()
            if (self.match("(")):
                self.proximoToken()
                if (self.expressao()):
                    self.proximoToken()
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
                        
    # <itera¸c˜ao-decl> ::= while ( <express˜ao> ) <comando>

    def retorno_decl(self): # Ver drireito isso aqui
        if (self.match("return")):
            self.proximoToken()
            if (self.match(";")):
                return True
            elif (self.expressao()):
                self.proximoToken()
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

    # <retorno-decl> ::= return ; | return <express˜ao> ;
    # CONTINUAR A PARTIR DAQUI
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
        
        self.posicaoAtual = indice - 1
        self.proximoToken()
        if (self.expressao_simples()):
            return True
        else:
            self.erro()
            return False

    # <express˜ao> ::= <var> = <express˜ao> | <express˜ao-simples>
    
    def var(self):
        if (self.ident()):
            indice = self.posicaoAtual
            self.proximoToken()
            if (self.abre_colchete()):
                self.proximoToken()
                if (self.expressao()):
                    self.proximoToken()
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
                        self.posicaoAtual = indice - 1
                        self.proximoToken()
                        return True
            else:
                self.posicaoAtual = indice - 1
                self.proximoToken()
                return True
        else:
            return False

    def expressao_simples(self):
        if (self.expressao_soma()):
            # self.proximoToken()
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

    # <express˜ao-simples> ::= <express˜ao-soma> <relacional> <express˜ao-soma> | <express˜ao-soma>

    def relacional(self):
        if ((self.match("<=")) or (self.match("<")) or (self.match(">"))
           or (self.match(">=")) or (self.match("==")) or (self.match("!="))):
            return True
        else:
            return False

    def expressao_soma(self):
        if (self.termo()):
            indice = self.posicaoAtual
            self.proximoToken()
            if (self.soma()):
                while (self.soma()):
                    self.proximoToken()
                    if not(self.termo()):
                        self.erro()
                        return False
                    self.proximoToken()
                return True
            else:
                self.posicaoAtual = indice - 1
                self.proximoToken()
                return True
        else:
            self.erro()
            return False
                    


    # <express˜ao-soma> ::= <termo> {<soma> <termo>}
    
    def soma(self):
        if ((self.match("+")) or (self.match("-"))):
            return True
        else:
            return False

    def termo(self):
        if (self.fator()):
            self.proximoToken()
            if (self.mult()):
                while (self.mult()):
                    self.proximoToken()
                    if not(self.fator()):
                        self.erro()
                        return False
                    self.proximoToken()
            else:
                return True
        else:
            self.erro()
            return False

    # <fator> {<mult> <fator>}

    def mult(self):
        if ((self.match("*")) or (self.match("/"))):
            return True
        else:
            return False

    def fator(self):
        if (self.match("(")):
            self.proximoToken()
            if (self.expressao()):
                self.proximoToken()
                if (self.match(")")):
                    return True
                else:
                    self.erro()
                    return False
            else:
                self.erro()
                return False
        elif (self.var()):
            return True
            
        elif (self.ativacao()):
            return True
        
        elif (self.num()):
            return True

        elif (self.num_int()):
            return True
        else:
            self.erro()
            return False

    # <fator> ::= ( <express˜ao> ) | <var> | <ativa¸c˜ao> | <num> | <num-int>

    def ativacao(self):
        if (self.ident()):
            self.proximoToken()
            if (self.match("(")):
                self.proximoToken()
                if (self.args()):
                    self.proximoToken()
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

    # <ativa¸c˜ao> ::= <ident> ( <args> )

    def args(self):
        self.arq_lista()
        return True

    # <args> ::= [<arg-lista>]
        
    def arg_lista(self):
        if (self.expressao()):
            self.proximoToken()
            while (self.match(",")):
                self.proximoToken()
                if not(self.expressao()):
                    self.erro()
                    return False
                self.proximoToken()
        else:
            self.erro()
            return False


    # <arg-lista> ::= <express˜ao> {, <express˜ao>}
    
    def num(self): # A TERMINAR
        if ((self.match("+")) or (self.match("-")) or (self.digito())):
            i = 1
            if not(self.digito()):
                self.proximoToken()
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

    # [+ | -] <d´ıgito> {<d´ıgito>} [. <d´ıgito> {<d´ıgito>}] [E [+ | -] <d´ıgito> {<d´ıgito>}]

    def num_int(self):
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
            # self.erro()
            return False
        return True

    def fecha_chave(self):
        if not(self.match("}")):
            # self.erro()
            return False
        return True

    def abre_colchete(self):
        if not(self.match("[")):
            # self.erro()
            return False
        return True
    
    def fecha_colchete(self):
        if not(self.match("]")):
            # self.erro()
            return False
        return True
