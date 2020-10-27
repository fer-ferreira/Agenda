# !/usr/bin/env python
## coding: utf-8

import sys
from antlr4 import *
from antlr4.error.ErrorListener import *
from antlr4.tree.Trees import Trees
from agendaLexer import agendaLexer
from agendaParser import agendaParser
from agendaListener import agendaListener
from agendaVisitor import agendaVisitor
from agenda_gerador import agendaGerador
from agenda_semantico import agendaSemantico
from agenda_utils import agenda_utils

## Símbolos não permitidos
invalid_symbols = ['!', '#', '$', '%', '*', '=', '+', '?', '<',
                   '>', '|', ':', '/', '{', '}', '[', ']']

## Procedimento usado para escrever o erro no arquivo
def escreveSaida(linha, coluna, erro, tipo):

    if(tipo == 'extraneous/mismatched' or tipo == 'eof'):
        arquivo.write(f"Linha {linha}: erro proximo a '{erro}'\n")

    else:
        arquivo.write(f"Linha {linha}: simbolo '{erro}' nao identificado\n")


class agendaErrorListener(ErrorListener):

	## Sobrescrevendo a função padrão "syntaxError" do antlr4
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):

        err = offendingSymbol.text

        if ('extraneous input' in msg or 'mismatched' in msg) and err not in invalid_symbols:
            escreveSaida(line, column, err, 'extraneous/mismatched')

        elif len(msg.split("'")) > 1 and err not in invalid_symbols:
            if '<EOF>' in err:
                err = 'EOF'
            escreveSaida(line, column, err, 'eof')

        else:
            escreveSaida(line, column, err, 'simbolo')

        arquivo.write('Fim da compilacao\n')
        exit()


def main(argv):

	## Obtenção dos parâmetros da linha de comando
    input = FileStream(argv[1])
    output_file = argv[2]

    global arquivo
    arquivo = open(output_file, 'w')

    lexer = agendaLexer(input)
    lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    parser = agendaParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(agendaErrorListener())
    tree = parser.agenda()

    printer = agendaListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    # Análise semântica
    utils = agenda_utils(output_file, tree)
    s = agendaSemantico(utils)
    s.visitAgenda(tree)

    # A geração de código é feita somente se não houver nenhum erro semântico
    if len(utils.errosSemanticos) == 0:
        c = agendaGerador(utils)
        c.visitAgenda(tree)

    # Fechamento do arquivo / gravação do buffer
    arquivo.close()


if __name__ == '__main__':

    # Função principal (início do programa)
    main(sys.argv)
