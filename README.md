# Agenda de contatos em HTML

Este projeto consiste em um gerador de agenda de contatos. A partir de um arquivo texto contendo uma lista de nomes, endereços, emails e/ou telefones, é produzido um arquivo em formato HTML que mostra essas informações de maneira organizada e visualmente atrativa.

Aqui serão dadas as instruções de uso e compilação, considerando comandos executados em terminais bash do sistema operacional Linux. Adaptações podem ser necessárias para que os passos indicados funcionem adequadamente em outros sistemas operacionais.

## Sobre

Este é um trabalho produzido para a disciplina de Construção de Compiladores, ministrada pelo Prof. Dr. Daniel Lucrédio na Universidade Federal de São Carlos (UFSCar).

Autoria: Fernanda Ferreira e Vitor Sugaya.

## Arquivos e diretórios

* `./arquivos_antlr4/`: diretório que contém arquivos do ANTLR4 com correções de codificação ASCII/UTF-8;

* `./casos_de_teste_lexicos_e_sintaticos/`: exemplos de arquivos de entrada que apresentam erros léxicos e/ou sintáticos (o arquivo de saída produzido contém uma mensagem de erro);

* `./casos_de_teste_semanticos/`: exemplos de arquivos de entrada que apresentam erros semânticos (o arquivo de saída produzido contém uma ou mais mensagens de erro);

* `./casos_de_teste_gerador/`: exemplos de arquivos de entrada que não possuem erros e, portanto, possibilitam a geração adequada do arquivo de saída como um HTML;

* `agenda.g4`: gramática da linguagem, construída a partir do ANTLR4;

* `agenda.py`: código principal, responsável por fazer a leitura do arquivo de entrada, verificar a conformidade léxica e sintática e coordenar a análise semântica e geração de código;

* `agenda_gerador.py`: código responsável pela geração do HTML, caso o arquivo de entrada não contenha erros;

* `agenda_semantico.py`: código responsável por realizar a análise semântica;

* `agenda_utils.py`: utilitários que auxiliam a análise semântica e geração de código.

## Como usar?

### Instalações necessárias

* Python 3 (versão 3.7 ou superior), que pode ser obtido [aqui](https://www.python.org/downloads/);

* Gerenciador de pacotes Python, que pode ser instalado a partir de um bash executando:

```
$ python -m pip install pip
```
ou 

```
$ python3 -m pip install pip
```

* Java (versão 11 ou superior), que pode ser obtido [aqui](http://jdk.java.net/);

* ANTLR4, que pode ser obtido a partir da execução de um dos seguintes comandos em um bash:

```
$ python -m pip install antlr4-python3-runtime
```
ou

```
$ python3 -m pip install antlr4-python3-runtime
```

* ANTLR jar, que pode ser obtido pela execução dos seguintes comandos fornecidos [na página do ANTLR](https://www.antlr.org/):

```
$ cd /usr/local/lib
$ wget https://www.antlr.org/download/antlr-4.8-complete.jar
$ export CLASSPATH=".:/usr/local/lib/antlr-4.8-complete.jar:$CLASSPATH"
$ alias antlr4='java -jar /usr/local/lib/antlr-4.8-complete.jar'
```

### Compilação

Opcionalmente, para facilitar a compilação, pode-se criar o seguinte `alias`:

```
$ alias antlr4=”java -jar /usr/local/lib/antlr-4.8-complete.jar -visitor -Dlanguage=Python3”
```

Faça download dos arquivos deste projeto, deixando-os em um mesmo diretório. Inicie um bash nesse diretório e execute:

```
$ antlr4 agenda.g4
```

ou, caso o `alias` não tenha sido criado:

```
$ java -jar /usr/local/lib/antlr-4.8-complete.jar -visitor -Dlanguage=Python3 agenda.g4
```

Esse passo gera os arquivos necessários para funcionamento do programa. NÃO APAGUE-OS!

## Criação de um arquivo de entrada

Após a compilação pode-se executar o programa, mas para isso é necessário ter um arquivo de entrada (arquivo de texto contendo o(s) contato(s) da agenda).

Para que a execução não resulte em erros, algumas regras devem ser seguidas:

* o arquivo de entrada deve conter pelo menos um contato;

* um contato deve ter um nome e pelo menos uma informação adicional (email, telefone ou endereço);

* a primeira informação a ser dada sobre um contato é sempre o nome;

* nomes de contatos, ruas, bairros, cidades e países devem sempre iniciar com letra maiúscula;

* acentos não são permitidos;

* cada contato pode ter múltiplos emails, telefones e endereços, que podem ser dados em qualquer ordem;

* a separação das informações deve ser dada por quebra de linha ("enter");

* deve-se sempre ter uma linha vazia entre dois contatos e ao final do arquivo;

* emails devem seguir o padrão `user@dominio` (no momento só é permitido que o final seja `.com`, `.br` ou `.com.br`), sendo que `user` deve ser composto por letras minúsculas e pode, opcionalmente, conter números, `_` e/ou `.`;

* telefones devem seguir o padrão `(DDD) numero`, em que `DDD` corresponde a dois dígitos numéricos e `numero` corresponde a uma sequência de dígitos númericos (pode-se separá-los em duas partes usando hífen ou espaço - ex: 0000-0000 ou 0000 0000);

* os campos de um endereço (rua, número, bairro, cidade, cep e país) devem ser separados por vírgula;

* endereços devem começar com `Rua`, `Avenida`, `Logradouro`, `R.`, `Av.` ou `Logr.`;

* os campos obrigatórios de um endereço são: nome da rua, número e bairro;

* opcionalmente um endereço pode conter cidade e unidade federativa, sendo que a unidade federativa deve ser dada em duas letras maiúsculas e deve ser separada de cidade por um hífen (ex: São Paulo - SP);

* também é opcional informar cep (sequência de dígitos numéricos, que podem ou não ser separados em duas partes por hífen - ex: 00000-000) e país;

* não é permitido o uso dos símbolos: `!`, `#`, `$`, `%`, `*`, `=`, `+`, `?`, `<`, `>`, `|`, `:`, `/`, `{`, `}`, `[` e `]`;

* é permitido criar um grupo de contatos e, para isso, é preciso declarar o nome do grupo logo abaixo do nome do contato;

* todas as regras anteriores valem para contatos em um grupo;

* um grupo deve conter mais de um contato.


Essas regras são definidas na gramática (`agenda.g4`). Arquivos de exemplo que estão em conformidade com essas regras podem ser encontrados no diretório `./casos_de_teste_gerador/`.

### Execução

Até o momento da escrita deste documento (26/10/2020), se fazem necessárias algumas alterações em [arquivos da biblioteca](https://github.com/antlr/antlr4/pull/1630/commits/99ed4b6de662d7b9f647bf5c95cb34dbcabe8bd6) para uma execução correta. Essas alterações se referem a problemas de codificação (ASCII e UTF-8) no momento da manipulação de arquivos. Para maiores informações acesse [este link](https://github.com/antlr/antlr4/pull/1630). 

Os arquivos a serem alterados são `FileStream.py` e `StdinStream.py`. Em um sistema Linux, considerando Python 3.8, os arquivos originais se encontram em

```
/home/<seu_user>/.local/lib/python3.8/site-packages/antlr4/FileStream.py
```
e

```
/home/<seu_user>/.local/lib/python3.8/site-packages/antlr4/StdinStream.py
```

Localize-os (se achar necessário, faça um backup, renomeando-os para `FileStream_bkp.py` e `StdinStream_bkp.py`). Em seguida, copie para esse diretório os arquivos `FileStream.py` e `StdinStream.py` disponibilizados neste projeto no diretório `arquivos_antlr4`.

Feito isso, pode-se finalmente executar o programa! De posse de um arquivo de entrada (crie um seguindo as regras dadas em `Criação de um arquivo de entrada` ou selecione um exemplo em `./casos_de_teste_gerador/`), escolha um nome para o arquivo de saída e execute:

```
python agenda.py <arquivo_de_entrada> <arquivo_de_saida>
```

ou

```
python3 agenda.py <arquivo_de_entrada> <arquivo_de_saida>
```

Se não houverem erros no arquivo de entrada, uma agenda em html será produzida. Para visualizá-la, basta abrir o html em um navegador (Google Chrome, Mozilla Firefox etc).

Aproveite!