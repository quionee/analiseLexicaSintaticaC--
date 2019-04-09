entrada = {'a':12,'b':16,'c':5,'d':15,'e':3,'f':1,'g':16,'h':14,'i':0,'j':16,'k':16,'l':10,'m':16,
    'n':8,'o':11,'p':16,'q':16,'r':7,'s':2,'t':9,'u':13,'v':6,'w':4,'x':16,'y':16,'z':16,'0':17,
    '1':17,'2':17,'3':17,'4':17,'5':17,'6':17,'7':17,'8':17,'9':17,'/':18,'+':19,'-':20,'*':21,
    '<':22,'>':23,'=':24,'{':25,'}':26,'[':27,']':28,'!':29,'@':30,'.':31}

estadosFinais = {4:'int',10:'float',17:'struct',22:'else',24:'if',30:'while',35:'char',40:'void',
47:'return',52:'comentario',54:'identificador',56:'+',58:'-',60:'*',63:'>',65:'<',66:'=',68:'>=',70:'<=',
73:'==',76:'!=',80:'abreChave',78:'fechaChave',82:'abreColchete',84:'fechaColchete',86:'constNumerica'
,89:'constNumerica'}   

#função que lê o arquivo com as transições do automato e preenche a matriz
#A ordem dos elementos são ESTADO ATUAL / caracter de leitura / ESTADO DE DESTINO.
def geraTabelaDirecionada():
   # nomeArq = raw_input("\nNome do arquivo: ")
    arquivo = open("automato")
    tabela = [0] * 90   # gerando as linhas
    for i in range(90):
        tabela[i] = [-1] * 32 #gerando as colunas
    linha = arquivo.readline()
    while linha:# formato da linha : estadoAtual entrada : estadoDestino
        valores = linha.split(' ')
        tabela[int(valores[0])][entrada[valores[1]]] = int(valores[2])#ENTRADA é dicionario com os indices das colunas dos caracteres
        linha = arquivo.readline()
    arquivo.close()
    
    return tabela

def imprimeTabela():
    for i in range(90):
        for j in range(32):
            print(tabela[i][j], end=' ')
        print()

# Verifica um lexema e retorna o tipo dele
def verifica(lexemas, tabela):
    estado = 0 #estado inicial
    #Percorre cada caracter do lexema
    for i in (lexemas + "@"): # + @ = ultima trasição para o estado final(@ representa espaço vazio)
        estado = tabela[estado][entrada[i]] # atualiza o estado atual
    if estado in estadosFinais: # verifica se o estado atual é um estado final
        return estadosFinais[estado]#retorna o tipo léxico
    else:
        return -1 #palavra inválida
