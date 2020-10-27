# !/usr/bin/env python
## coding: utf-8

## Generated from agenda.g4 by ANTLR 4.8

from antlr4 import *
from agendaVisitor import agendaVisitor
if __name__ is not None and "." in __name__:
    from .agendaParser import agendaParser
else:
    from agendaParser import agendaParser

class agendaGerador(agendaVisitor):

	## Inicialização de listas e dicionários
    def __init__(self, utils):
        self.utils = utils
        self.grupos = {}
        self.contatos_s_grupo = {}


    def visitAgenda(self, ctx: agendaParser.AgendaContext):
        self.utils.adicionarCodigo("<html>\n")
        self.utils.adicionarCodigo("<body>\n")
        self.utils.adicionarCodigo("<center>\n") ## deixa texto centralizado
        self.visitContatos(ctx.contatos())

        ## Se existem grupos, vamos imprimí-los primeiro
        if len(self.grupos) != 0:
            ## Ordenar
            nomes_grupos = list(self.grupos.keys())
            nomes_grupos.sort()

            ## Para cada grupo
            for nome_grupo in nomes_grupos:
                ## Criar separador para agrupar contatos por letra
                separador = 'a'

                ## Ordena nomes
                sorted_group = dict(
                    sorted(self.grupos[nome_grupo].items(), key=lambda item: item[0]))

                ## Nome do grupo
                self.utils.adicionarCodigo(
                    f"<p style=\"font-family:'verdana'\">Grupo: {nome_grupo}<br></p>\n")

                self.utils.adicionarCodigo(
                    f"<p style=\"font-family:Courier New\">")

                ## Para cada pessoa
                for nome, (email, telefone, endereco) in sorted_group.items():
                    ## Verificar se separador precisa ser mostrado
                    inicial = nome[0].upper()
                    if inicial != separador:
                        self.utils.adicionarCodigo(
                            f"<b>{inicial}</b><br>\n")
                        separador = inicial

                    ## Imprime informações do contato
                    self.utils.adicionarCodigo(f"{nome}<br>\n")
                    if email != []:
                        self.iterThrough("e-mail", email)
                    if telefone != []:
                        self.iterThrough("telefone", telefone)
                    if endereco != []:
                        self.iterThrough("endereço", endereco)

                    self.utils.adicionarCodigo("<br><br>\n")

                self.utils.adicionarCodigo(f"</p>\n")

        self.utils.adicionarCodigo("<br><br><br><br>\n")

        ## Impressão de contatos que ñ possuem grupo
        if len(self.grupos) > 0 and len(self.contatos_s_grupo) > 0:
            self.utils.adicionarCodigo(
                "<p style=\"Serif\">------- Outros Contatos -------</p>")
        ## Ordena nomes
        self.contatos_s_grupo = dict(
            sorted(self.contatos_s_grupo.items(), key=lambda item: item[0]))

        self.utils.adicionarCodigo(
            f"<p style=\"font-family:Courier New\">")

        ## Separador de agrupamento
        separador = 'a'
        for nome, (email, telefone, endereco) in self.contatos_s_grupo.items():
            inicial = nome[0].upper()
            ## Caso letra inicial seja diferente da anterior
            if inicial != separador:
                self.utils.adicionarCodigo(
                    f"<b>{inicial}</b><br><br>\n")
                separador = inicial

            self.utils.adicionarCodigo(f"{nome}<br>\n")
            if email != []:
                self.iterThrough("email", email)

            if telefone != []:
                self.iterThrough("telefone", telefone)

            if endereco != []:
                self.iterThrough("endereco", endereco)

            self.utils.adicionarCodigo("<br><br>\n")

        self.utils.adicionarCodigo(f"</p>\n")

        self.utils.adicionarCodigo("</center>\n")
        self.utils.adicionarCodigo("</body>\n")
        self.utils.adicionarCodigo("</html>\n")


    def visitContato(self, ctx: agendaParser.ContatoContext):
        nome = self.visitNome(ctx.nome())
        grupo = None
        email = []
        telefone = []
        endereco = []

        if ctx.grupo() is not None:
            grupo = self.visitGrupo(ctx.grupo())

        for c_email in ctx.email():
            email.append(self.visitEmail(c_email))

        for c_telefone in ctx.telefone():
            telefone.append(self.padronizaTelefone(
                self.visitTelefone(c_telefone)))

        for c_endereco in ctx.endereco():
            endereco.append(self.visitEndereco(c_endereco))

        ## Email, telefone e endereco são listas, pois contato pode ter mais de um
        ## Se está em grupo, colocamos na lista de acordo com respectivo grupo,
        ## caso contrário colocamos em contatos sem grupo
        if grupo is None:
            self.contatos_s_grupo[nome] = (email, telefone, endereco)
        else:
            self.grupos[grupo][nome] = (email, telefone, endereco)


    def visitGrupo(self, ctx: agendaParser.GrupoContext):
        nome_grupo = ctx.getText()
        ## Se o grupo ñ havia sido referenciado antes,
        ## cria um novo grupo com aquele nome como identificador
        if nome_grupo not in self.grupos:
            self.grupos[nome_grupo] = {}

        return nome_grupo


    def visitEmail(self, ctx: agendaParser.EmailContext):
        if ctx.nome_de_usuario() is not None:
            nome_de_usuario = self.visitNome_de_usuario(ctx.nome_de_usuario())
        if ctx.dominio() is not None:
            dominio = self.visitDominio(ctx.dominio())

        return nome_de_usuario + '@' + dominio

    def visitNome_de_usuario(self, ctx: agendaParser.Nome_de_usuarioContext):
        return ctx.getText()

    def visitDominio(self, ctx: agendaParser.DominioContext):
        return ctx.getText()

    def visitTelefone(self, ctx: agendaParser.TelefoneContext):
        return ctx.getText()

    def visitEndereco(self, ctx: agendaParser.EnderecoContext):
        end = ""
        end += self.visitRua(ctx.rua()) + ', '
        end += ctx.NUMERO().getText() + ', '
        end += self.visitBairro(ctx.bairro())

        if ctx.cidade() is not None:
            end += ', ' + self.visitCidade(ctx.cidade())
            end += ' - '
            end += self.visitUf(ctx.uf())

        if ctx.cep() is not None:
            end += ', ' + self.visitCep(ctx.cep())

        if ctx.pais() is not None:
            end += ', ' + self.visitPais(ctx.pais())

        return end

    def visitCidade(self, ctx: agendaParser.CidadeContext):
        return ctx.getText()

    def visitBairro(self, ctx: agendaParser.BairroContext):
        return ctx.getText()

    def visitRua(self, ctx: agendaParser.RuaContext):
        return ctx.getText()

    def visitUf(self, ctx: agendaParser.UfContext):
        return ctx.getText()

    def visitPais(self, ctx: agendaParser.PaisContext):
        return ctx.getText()

    def visitCep(self, ctx: agendaParser.CepContext):
        return self.padronizaCEP(ctx.getText())

    def visitNome(self, ctx: agendaParser.NomeContext):
        return ctx.getText()

    ## Procedimento que itera pela lista de emails, telefones e endereco de cada contato
    ## 'tag' é o texto que será mostrado
    ## 'iterable' é a lista que vamos percorrer
    def iterThrough(self, tag, iterable):
        ## Imprime tag + primeiro elemento
        self.utils.adicionarCodigo(f"{tag}: {iterable[0]}")

        ## Se há mais elementos, imprimimos, separando por uma barra
        if len(iterable) > 1:
            i = 1
            while i < len(iterable):
                self.utils.adicionarCodigo(f" / {iterable[i]}")
                i += 1
        self.utils.adicionarCodigo("<br>\n")

    ## Função para padronizar como CEPs são mostrados
    def padronizaCEP(self, cep):
        ## Se possui espaços ou não possui hífen
        if ' ' in cep or '-' not in cep:
            raw_cep = ""
            for c in cep:
                ## Só adiciona os números
                if c >= '0' and c <= '9':
                    raw_cep += c

            ## Separa devidamente
            cep = raw_cep[0] + raw_cep[1:5] + '-' + raw_cep[5:]

        return cep

    ## Função para padronizar como telefones serão mostrados
    def padronizaTelefone(self, telefone):
        ## Devemos alterar caso falte o hífen no meio do telefone
        ## ou caso haja espaços no número
        if '-' not in telefone or ' ' in telefone:
            ## Deparamos em ddd e número
            ddd = telefone.split(')')[0][1:]
            telefone_s_ddd = telefone.split(')')[1]

            ddd_final = "("
            telefone_final = ""

            ## De caractere em DDD ñ for espaço, acrescentamos à porção final
            for N in ddd:
                if N != ' ':
                    ddd_final += N

            ddd_final += ')'

            ## Se caracter em número ñ for espaço
            ## ou hífen, acrescentamos, removemos o hífen
            ## pois sempre o colocaremos no final
            for N in telefone_s_ddd:
                if N != ' ' and N != '-':
                    telefone_final += N

            telefone_final = telefone_final[:4] + '-' + telefone_final[4:]
            telefone = ddd_final + telefone_final

        return telefone


del agendaParser
