# -*- coding: utf-8 -*-

from prettytable import PrettyTable

class TabelaDeSimbolos:
    def __init__(self):
        self.tabelaDeSimbolos = []
        self.qtdLinhas = 0
    
    def adiciona(self, lexema, tipo):
        consulta = self.consulta(lexema)
        if (not(consulta)):
            self.qtdLinhas += 1
            linha = [0] * 3
            linha[0] = self.qtdLinhas
            linha[1] = lexema
            linha[2] = tipo
            self.tabelaDeSimbolos.append(linha)
            return self.qtdLinhas
        else:
            return consulta

    def consulta(self, lexema):
        for i in range(len(self.tabelaDeSimbolos)):
            if (self.tabelaDeSimbolos[i][1] == lexema):
                return self.tabelaDeSimbolos[i][0]
        return False
    
    def imprime(self):
        print("\n\n     ----- Tabela de Símbolos -----\n")
        tabela = PrettyTable(["Entrada", "Lexema", "Tipo"])
        tabela.align["Entrada"] = "1"
        tabela.align["Lexema"] = "1"
        tabela.align["Tipo"] = "1"

        for i in range(self.qtdLinhas):
            tabela.add_row([self.tabelaDeSimbolos[i][0], self.tabelaDeSimbolos[i][1], self.tabelaDeSimbolos[i][2]])
        
        print(tabela)
