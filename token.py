# -*- coding: utf-8 -*-

class Token:
    def __init__(self, tipo, valor, linha, coluna):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna
    
    def getTipo(self):
        return self.tipo
    
    def getValor(self):
        return self.valor
    
    def getLinha(self):
        return self.linha
    
    def getColuna(self):
        return self.coluna

    def imprime(self):
        print("<", self.tipo, ",", self.valor, ",", self.linha, ",", self.coluna, ">")
