# -*- coding: utf-8 -*-

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
    def getTipo(self):
        return self.tipo
    
    def getValor(self):
        return self.valor
    
    def imprime(self):
        print("<", self.tipo, ",", self.valor, ">")
