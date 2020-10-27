grammar agenda;

// Esta é uma linguagem para descrever contatos (nome, email, telefone, endereço) 


// Agenda é composta por contatos
agenda 		    : contatos EOF ;


// Para compor a agenda, é necessário que tenha pelo menos um contato
contatos        : contato+ ;


// Contato é composto de um nome mais um meio de comunicação, pelo menos
contato         :   LINE_BREAK? nome LINE_BREAK 
                    ( grupo LINE_BREAK )?
					( email LINE_BREAK 
                    | telefone LINE_BREAK 
                    | endereco LINE_BREAK )+
                  ;


// É possível agrupar contatos usando um identificador
grupo           : nome_grupo ( WS nome_grupo )* ;


// Email é composto por um nome de usuário e um domínio
// Nome de usuário é um nome com algumas restrições
email 			: nome_de_usuario '@' dominio ;


// Nome de usuário não pode começar com _ ou . , mas ambos são permitidos nos próximos caracteres
nome_de_usuario : l1=L_MINUSCULA+ ('_' | '.' | NUMERO | L_MINUSCULA)* ( L_MINUSCULA | NUMERO );

// Domínios podem ser simples (ex: ufscar.br) ou compostos (ex: estudante.ufscar.br)
// Por motivos de simplicidade só são permitidos domínios brasileiros
dominio			: (L_MINUSCULA)+  ('.' (L_MINUSCULA)+)? '.' ('com'|'br'|'com.br') ;

// Composto por DDD e número
telefone 		: ddd=DDD WS? NUMERO ( WS? '-'? WS? NUMERO)* ; 

// Definição do DDD, que é o código da cidade
DDD             : '(' [0-9][0-9] ')' ;

// Endereço tem de ser composto minimamente de rua, numero e bairro
// outros itens como cidade, cep e país são opcionais
endereco        : rua WS? ',' WS? NUMERO WS? ',' WS? bairro (WS? ',' WS? cidade WS? '-' WS? uf )? (WS? ',' WS? cep )? (WS? ',' WS? pais)? ;

descritor_rua   : ('Rua' | 'Avenida' | 'Logradouro' | 'R.' | 'Av.' | 'Logr.') WS?  ;

rua  			: descritor_rua n1=NOME (WS (n2+=NOME | L_MINUSCULA+))* ;

bairro          : NOME (WS (NOME | L_MINUSCULA+))* ;

cidade 			: NOME (WS (NOME | L_MINUSCULA+))* ;

// Sigla que descreve a unidade federativa
uf				: UNID_FED ;

cep				: NUMERO | (NUMERO WS? '-' WS? NUMERO) ;

pais 			: NOME (WS (NOME | L_MINUSCULA+))* ;

// Uma pessoa tem, no mínimo, um nome
nome   			: NOME (WS NOME)* ;

// Nomes devem iniciar com letra maiúscula e podem ser compostos de uma ou mais letras
// É permitido nomes que contenham hífen (ex: Jean-Paul, Guiné-Bissau)
NOME			: [A-Z][a-z]* ('-' [A-Z][a-z]*)? ; 

nome_grupo		: (nome_g=NOME | letra=L_MINUSCULA+);

NUMERO			: [0-9]+ ;

L_MINUSCULA     : [a-z] ; 

L_MAIUSCULA     : [A-Z] ;

UNID_FED        : [A-Z][A-Z] ; 

SIMBOLO_INVALIDO : '!' | '#' | '$' | '%' | '*' | '=' | '+' | '?' | '<' | '>' | '|' | ':' | '/' | '{' | '}' | '[' | ']' ;

LINE_BREAK		: '\n' ;

WS				: ' ' ;
