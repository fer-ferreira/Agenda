# !/usr/bin/env python
## coding: utf-8

from agendaVisitor import agendaVisitor
from agendaParser import agendaParser

class agendaSemantico(agendaVisitor):

	## Inicializações de listas e dicionários a serem utilizados
    def __init__(self, utils):
        self.utils = utils
        self.contatos = []
        self.grupos = {}
        self.grupos_ctx = {}


    ## Os 'visit' abaixo sobrescrevem aqueles gerados como padrão pelo antlr4
    ## Isso é feito para que, ao dar match em cada regra da gramática, o programa tenha o comportamento desejado

    ## Visita a primeira regra da gramática
    def visitAgenda(self, ctx: agendaParser.AgendaContext):
        self.visitContatos(ctx.contatos())
        self.checkGroups()

    ## 'visitContatos' verifica duplicatas internas (repetições de email e telefone em um mesmo contato)
    ## e duplicatas externas (ocorrência do mesmo telefone ou email em dois contatos diferentes)
    ## Para isso são utilizadas listas e um dicionário
    def visitContatos(self, ctx: agendaParser.ContatosContext):
        counter = 0

        if ctx.contato() is not None:
            for i, c in enumerate(ctx.contato()):
                flag_externa = 0

                ## Caso seja o primeiro contato
                if counter == 0:

                	## Inicialização do dicionário
                    dados = {'nome': None, 'email': None,
                             'telefone': None, 'endereco': None}

                    ## Obtenção das informações do contato
                    nome, email, telefone, endereco = self.visitContato(c)

                    ## Verificação de duplicata interna
                    flag_interna = 0

                    tmp_email = []
                    for j, e in enumerate(email):
                        if e not in tmp_email:
                            tmp_email.append(e)
                        else:
                            flag_interna = 1
                            self.utils.adicionarErroSemantico(
                                ctx.contato()[i].email()[j].nome_de_usuario().l1, f"email '{e}' duplicado")
                            

                    tmp_telefone = []
                    for j, t in enumerate(telefone):
                        if t not in tmp_telefone:
                            tmp_telefone.append(t)
                        else:
                            flag_interna = 1
                            self.utils.adicionarErroSemantico(ctx.contato()[i].telefone()[
                                                              j].ddd, f"telefone '{t}' duplicado")
                            
                    ## A verificação da duplicata externa não é aplicável aqui, pois trata-se do primeiro contato

                    ## Se nenhum erro foi encontrado, as informações são adicionadas ao dicionário
                    if flag_interna == 0:
                        dados = {'nome': nome, 'email': email,
                                 'telefone': telefone, 'endereco': endereco}
                        self.contatos.append(dados)
                    counter += 1

                else:
                    nome, email, telefone, endereco = self.visitContato(c)

                    ## Verificação de duplicata interna
                    flag_interna = 0

                    tmp_email = []
                    for j, e in enumerate(email):
                        if e not in tmp_email:
                            tmp_email.append(e)
                        else:
                            flag_interna = 1
                            self.utils.adicionarErroSemantico(
                                ctx.contato()[i].email()[j].nome_de_usuario().l1, f"email '{e}' duplicado")
                            

                    tmp_telefone = []
                    for j, t in enumerate(telefone):
                        if t not in tmp_telefone:
                            tmp_telefone.append(t)
                        else:
                            flag_interna = 1
                            self.utils.adicionarErroSemantico(ctx.contato()[i].telefone()[j].ddd, f"telefone '{t}' duplicado")

                    ## Verificação de duplicata externa
                    for j, e in enumerate(email):
                        for dic in self.contatos:
                            for item in dic['email']:
                                if e == item:
                                    self.utils.adicionarErroSemantico(
                                        ctx.contato()[i].email()[j].nome_de_usuario().l1, f"email '{e}' duplicado")
                                    flag = 1

                    for j, t in enumerate(telefone):
                        for dic in self.contatos:
                            for item in dic['telefone']:
                                if t == item:
                                    self.utils.adicionarErroSemantico(ctx.contato()[i].telefone()[j].ddd, f"telefone '{t}' duplicado")
                                    flag = 1
                    
                    ## Se nenhum erro for encontrado os dados são adicionados ao dicionário
                    if flag_externa == 0 and flag_interna == 0:
                        dados = {'nome': nome, 'email': email,
                                 'telefone': telefone, 'endereco': endereco}
                        self.contatos.append(dados)

                counter += 1

    ## Esse 'visit' retorna informações de um mesmo contato e é utilizado em 'visitContatos'
    ## Como é permitida a declaração de vários emails, telefones e endereços, são utilizadas listas
    def visitContato(self, ctx: agendaParser.ContatoContext):
        grupo = None
        nome = self.visitNome(ctx.nome())
        email = []
        telefone = []
        endereco = []

        if ctx.grupo() is not None:
            nome_grupo, grupo_ctx = self.visitGrupo(ctx.grupo())
            self.grupos_ctx[nome_grupo] = grupo_ctx

            if nome_grupo not in self.grupos:
                self.grupos[nome_grupo] = []
                self.grupos[nome_grupo].append(nome)
            else:
                self.grupos[nome_grupo].append(nome)

        if ctx.email() is not None:
            for e in ctx.email():
                email.append(self.visitEmail(e))

        if ctx.telefone() is not None:
            for t in ctx.telefone():
                telefone.append(self.visitTelefone(t))

        if ctx.endereco() is not None:
            for e in ctx.endereco():
                endereco.append(self.visitEndereco(e))

        return nome, email, telefone, endereco

    ## Os 'visit' abaixo retornam as strings correspondentes a cada informação reconhecida
    ## por suas respectivas regras (email, telefone, endereço), para serem utilizadas em 'visitContato'

    ## Caso essas regras sejam compostas por outras, a string a ser retornada é montada a partir
    ## da visita a essas; caso contrário, é retornado apenas o texto reconhecido (ctx.getText())

    def visitNome(self, ctx: agendaParser.NomeContext):
        return ctx.getText()

    def visitEmail(self, ctx: agendaParser.EmailContext):
        user = self.visitNome_de_usuario(ctx.nome_de_usuario())
        dom = self.visitDominio(ctx.dominio())

        return (user + '@' + dom)

    def visitNome_de_usuario(self, ctx: agendaParser.Nome_de_usuarioContext):
        return ctx.getText()

    def visitDominio(self, ctx: agendaParser.DominioContext):
        return ctx.getText()

    def visitTelefone(self, ctx: agendaParser.TelefoneContext):
        return ctx.getText()

    def visitEndereco(self, ctx: agendaParser.EnderecoContext):
        endereco = self.visitRua(ctx.rua())
        endereco += ', ' + ctx.NUMERO().getText() + ', '
        endereco += self.visitBairro(ctx.bairro())

        if ctx.cidade() is not None:
            endereco += ', ' + self.visitCidade(ctx.cidade())
            endereco += '-' + self.visitUf(ctx.uf())

        if ctx.cep() is not None:
            endereco += ', ' + self.visitCep(ctx.cep())

        if ctx.pais() is not None:
            endereco += ', ' + self.visitPais(ctx.pais())
            
        return endereco

    def visitDescritor_rua(self, ctx: agendaParser.Descritor_ruaContext):
        return ctx.getText()

    def visitRua(self, ctx: agendaParser.RuaContext):
        nome_rua = self.visitDescritor_rua(ctx.descritor_rua())
        nome_rua += ' ' + ctx.n1.text

        if ctx.n2 is not None:
            for n in ctx.n2:
                nome_rua += ' ' + n.text

        return nome_rua

    def visitBairro(self, ctx: agendaParser.BairroContext):
        return ctx.getText()

    def visitCidade(self, ctx: agendaParser.CidadeContext):
        return ctx.getText()

    def visitUf(self, ctx: agendaParser.UfContext):
        return ctx.getText()

    def visitCep(self, ctx: agendaParser.CepContext):
        return ctx.getText()

    def visitPais(self, ctx: agendaParser.PaisContext):
        return ctx.getText()

    def visitGrupo(self, ctx: agendaParser.GrupoContext):
        if ctx.nome_grupo(0).NOME() is not None:
            return (ctx.getText(), ctx.nome_grupo(0).nome_g)
        return (ctx.getText(), ctx.nome_grupo(0).letra)

    ## Verificação de tamanho do grupo
    ## Não é permitido que um grupo tenha apenas 1 contato
    def checkGroups(self):
        for grupo in self.grupos.keys():
            if len(self.grupos[grupo]) == 1:
                self.utils.adicionarErroSemantico(
                    self.grupos_ctx[grupo], f"grupo '{grupo}' com apenas 1 membro")
