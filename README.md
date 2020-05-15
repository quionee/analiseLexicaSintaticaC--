### Análise léxica e análise sintática para a linguagem C--

A descrição do que é pedido em cada etapa e as especificações da linguagem C-- estão na pasta *descricao*.

#### Etapa 1 - Análise léxica
Um analisador léxico para a linguagem C-- foi implementado. O programa também trata erros léxicos e ignora / remove comentários e espaços em branco.

#### Etapa 2 – Análise sintática
Um analisador sintático para a linguagem C-- foi implementado. O analisador tem a tarefa de varrer todo o código-fonte fornecido como entrada	e relatar os possíveis erros de sintaxe. E como saída temos os possíveis erros sintáticos e a árvore de análise sintática.

#### Etapa 3 - Geração de código de três endereços
Foi implementado nessa etapa o código de três endereços para expressões aritméticas básicas da linguagem C--. Como saída tem-se uma matriz com o formato de quádrupla: resultado, operando1, operador, operando2.

*Observação:* a chamada para a etapa 3 está comentada no código, pois roda apenas para o arquivo de teste *arq_teste.txt*, para realizar a chamada, basta descomentar a linha *250* do arquivo *main.py*.

#### Entrada e Execução

O programa recebe como entrada um arquivo texto contendo um exemplo de código na linguagem C--. Os arquivos disponíveis para teste estão na pasta *arquivos_teste*, e são eles:

	* arquivo_sem_erros_lexicos.txt
	* arquivo_com_erros_lexicos.txt
	* arquivo_sem_erros_sintaticos.txt
	* arquivo_com_erros_sintaticos.txt
	* arq_teste.txt

Foi utilizado o python 3 para a implementação.

Para executar, basta rodar o comando `python3 main.py` no terminal e entrar com o nome do arquivo de teste.

#### Resultados

Os resultados são impressos no terminal ao final da execução, e são eles:

	* erros léxicos (se existirem)
	* lista de lexemas
	* lista de tokens
	* tabela de símbolos
	* erros sintáticos (se existirem)
	* tabela de símbolos

Copyright (c) 2019 Felipe Ferreira Carvalho Silva, Lorena Kerollen Botelho Tavares, Rodrigo Pinto Herculano, William Davi Coelho
