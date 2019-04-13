# -*- coding: utf-8 -*-

class TabelaDeSimbolos:
    def __init__(self):
        self.tabelaDeSimbolos = []
        self.qtdLinhas = 0
    
    def adiciona(self, lexema):
        if (not(self.consulta(lexema))):
            self.qtdLinhas += 1
            linha = [0] * 2
            linha[0] = self.qtdLinhas
            linha[1] = lexema
            self.tabelaDeSimbolos.append(linha)
            return self.qtdLinhas

    def consulta(self, lexema):
        for i in range(len(self.tabelaDeSimbolos)):
            if (self.tabelaDeSimbolos[i][1] == lexema):
                return True
        return False
    
    def imprime(self):
        print("ENTRADA  LEXEMA")
        for i in range(self.qtdLinhas):
            print(self.tabelaDeSimbolos[i][0], self.tabelaDeSimbolos[i][1])