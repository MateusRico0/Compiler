import re
import os


FOLLOW_NUMERO = ['COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
FOLLOW_ID = ['EQUIVALENCE', 'SEMICOLON', 'END', 'RIGHT_PARENTHESIS', 'VAR', 'BEGIN', 'COLON', 'COMMA', 'LEFT_PARENTHESIS', 'DOT', 'LEFT_BRACKETS', 'ASSIGN', None, 'FUNC', 'PROCEDURE', 'ELSE', 'PLUS', 'MINUS', 'MUL', 'DIV', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
FOLLOW_NOME = ['ASSIGN', 'COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
FOLLOW_PARAMETRO = ['COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
FOLLOW_OP_MAT = ['IDENTIFIER', 'NUMBER']
FOLLOW_EXP_MAT = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN']
FOLLOW_OP_LOGICO = ['IDENTIFIER', 'NUMBER']
FOLLOW_EXP_LOGICA = ['DO', 'THEN', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
FOLLOW_LISTA_PARAM = ['RIGHT_PARENTHESIS']
FOLLOW_ELSE = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
FOLLOW_ATRIB = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
FOLLOW_COMANDO = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
FOLLOW_LISTA_COM = ['END']
FOLLOW_BLOCO = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
FOLLOW_PARAM_ROT = ['COLON', 'VAR', 'BEGIN', 'COLON']
FOLLOW_NOME_ROTINA = ['VAR', 'BEGIN', 'COLON']
FOLLOW_DEF_ROT = ['BEGIN', 'COLON']
FOLLOW_LISTA_ID = ['COLON']
FOLLOW_VARIAVEL = ['SEMICOLON']
FOLLOW_LIST_VAR = ['FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
FOLLOW_DEF_VAR = ['FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
FOLLOW_LISTA_CAMPOS = ['END', 'SEMICOLON', 'RIGHT_PARENTHESIS']
FOLLOW_CAMPOS = ['END', 'SEMICOLON', 'RIGHT_PARENTHESIS']
FOLLOW_TIPO_DADO = ['SEMICOLON', 'END', 'RIGHT_PARENTHESIS', 'VAR', 'BEGIN', 'COLON']
FOLLOW_TIPO = ['SEMICOLON']
FOLLOW_LIST_TIPOS = ['VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
FOLLOW_DEF_TIPOS = ['VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
FOLLOW_CONST_VALOR = ['SEMICOLON']
FOLLOW_CONSTANTE = ['SEMICOLON']
FOLLOW_LIST_CONST = ['TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
FOLLOW_DEF_CONST = ['TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
FOLLOW_DECLARACOES = ['BEGIN', 'COLON']
FOLLOW_PROGRAMA = [None]

FIRST_PROGRAMA = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', None]
FIRST_DECLARACOES = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', None]
FIRST_DEF_CONST = ['CONST', None]
FIRST_LIST_CONST = ['IDENTIFIER', None]
FIRST_CONSTANTE = ['IDENTIFIER']
FIRST_CONST_VALOR = ['STRING', 'IDENTIFIER', 'NUMBER']
FIRST_DEF_TIPOS = ['TYPE', None]
FIRST_LIST_TIPOS = ['IDENTIFIER', None]
FIRST_TIPO = ['IDENTIFIER']
FIRST_TIPO_DADO = ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER']
FIRST_CAMPOS = ['IDENTIFIER']
FIRST_LISTA_CAMPOS = ['SEMICOLON', None]
FIRST_DEF_VAR = ['VAR', None]
FIRST_LIST_VAR = ['IDENTIFIER', None]
FIRST_VARIAVEL = ['IDENTIFIER']
FIRST_LISTA_ID = ['COMMA', None]
FIRST_DEF_ROT = ['FUNC', 'PROCEDURE', None]
FIRST_NOME_ROTINA = ['FUNC', 'PROCEDURE']
FIRST_PARAM_ROT = ['LEFT_PARENTHESIS', None]
FIRST_BLOCO = ['BEGIN', 'COLON']
FIRST_LISTA_COM = ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ', None]
FIRST_COMANDO = ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ']
FIRST_ATRIB = ['ASSIGN', None]
FIRST_ELSE = ['ELSE', None]
FIRST_LISTA_PARAM = ['IDENTIFIER', 'NUMBER', None]
FIRST_EXP_LOGICA = ['IDENTIFIER', 'NUMBER']
FIRST_OP_LOGICO = ['GREATER', 'LESS', 'EQUAL', 'EXCLAMATION']
FIRST_EXP_MAT = ['IDENTIFIER', 'NUMBER']
FIRST_OP_MAT = ['PLUS', 'MINUS', 'MUL', 'DIV']
FIRST_PARAMETRO = ['IDENTIFIER', 'NUMBER']
FIRST_NOME = ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', None]
FIRST_ID = ['IDENTIFIER']
FIRST_NUMERO = ['NUMBER']



rules = {
    'PROGRAMA' :( FIRST_PROGRAMA, FOLLOW_PROGRAMA ),
    'DECLARACOES' :( FIRST_DECLARACOES , FOLLOW_DECLARACOES ),
    'DEF_CONST' :( FIRST_DEF_CONST , FOLLOW_DEF_CONST ),
    'LIST_CONST' :( FIRST_LIST_CONST  , FOLLOW_LIST_CONST  ),
    'CONSTANTE'  :( FIRST_CONSTANTE  , FOLLOW_CONSTANTE  ),
    'CONST_VALOR'   :( FIRST_CONST_VALOR  , FOLLOW_CONST_VALOR  ),
    'DEF_TIPOS'   :( FIRST_DEF_TIPOS  , FOLLOW_DEF_TIPOS  ),
    'LIST_TIPOS'  :( FIRST_LIST_TIPOS  , FOLLOW_LIST_TIPOS  ),
    'TIPO'  :( FIRST_TIPO  , FOLLOW_TIPO  ),
    'TIPO_DADO' :( FIRST_TIPO_DADO , FOLLOW_TIPO_DADO ),
    'CAMPOS'  :( FIRST_CAMPOS  , FOLLOW_CAMPOS  ),
    'LISTA_CAMPOS' :( FIRST_LISTA_CAMPOS  , FOLLOW_LISTA_CAMPOS  ),
    'DEF_VAR'   :( FIRST_DEF_VAR  , FOLLOW_DEF_VAR  ),
    'LIST_VAR'  :( FIRST_LIST_VAR  , FOLLOW_LIST_VAR  ),
    'VARIAVEL'   :( FIRST_VARIAVEL  , FOLLOW_VARIAVEL  ),
    'LISTA_ID' :( FIRST_LISTA_ID , FOLLOW_LISTA_ID ),
    'DEF_ROT' :( FIRST_DEF_ROT  , FOLLOW_DEF_ROT  ),
    'NOME_ROTINA'  :( FIRST_NOME_ROTINA  , FOLLOW_NOME_ROTINA  ),
    'PARAM_ROT'  :( FIRST_PARAM_ROT  , FOLLOW_PARAM_ROT  ),
    'BLOCO'  :( FIRST_BLOCO  , FOLLOW_BLOCO  ),
    'LISTA_COM' :( FIRST_LISTA_COM  , FOLLOW_LISTA_COM  ),
    'COMANDO'   :( FIRST_COMANDO  , FOLLOW_COMANDO  ),
    'ATRIB'  :( FIRST_ATRIB , FOLLOW_ATRIB ),
    'ELSE':( FIRST_ELSE, FOLLOW_ELSE),
    'LISTA_PARAM'   :( FIRST_LISTA_PARAM  , FOLLOW_LISTA_PARAM  ),
    'EXP_LOGICA'   :( FIRST_EXP_LOGICA  , FOLLOW_EXP_LOGICA  ),
    'OP_LOGICO'   :( FIRST_OP_LOGICO  , FOLLOW_OP_LOGICO  ),
    'EXP_MAT'  :( FIRST_EXP_MAT  , FOLLOW_EXP_MAT  ),
    'OP_MAT'  :( FIRST_OP_MAT , FOLLOW_OP_MAT ),
    'PARAMETRO' :( FIRST_PARAMETRO  , FOLLOW_PARAMETRO  ),
    'NOME'  :( FIRST_NOME , FOLLOW_NOME ),
    'ID'  :( FIRST_ID , FOLLOW_ID ),
    'NUMERO' :( FIRST_NUMERO  , FOLLOW_NUMERO)
}

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def get_value(self):
        return self.value

    def __str__(self, level=0):
        result = "    " * level + repr(self.value) + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result


def erro(tokens,value=0):
    if tokens:
        if value != 0:
            print(f"Erro: Token {tokens[0][1]} inesperado na linha {tokens[0][2]}. Era esperado {value}")
        else:
            print(f"Erro: Token {tokens[0][1]} inesperado na linha {tokens[0][2]}.")

    else:
        raise ValueError(f"Erro: token necessário não encontrado na linha ")

def recover(no,tokens,follow):
    while(len(tokens) != 0):
        if(tokens[0][0] in follow):
            return 
        else:
            tokens.pop(0)[1]

def check_non_terminal(no, tokens, list_dict, filho, ignoravel=0):
    global linha
    if tokens:
        if tokens[0][0] in list_dict[0]:
            linha = tokens[0][2]
            no.children.append(filho(tokens))
            return True
        elif None not in list_dict[0] and ignoravel == 0:
            erro(tokens)
            raise SyntaxError 
    else:
        erro(tokens,2)
    return False


def check_terminal(no, tokens, value, ignoravel=0):
    if tokens:
        if tokens[0][0] == value:
            no.children.append(Node(tokens.pop(0)[1]))
            return True
        elif ignoravel == 0:
            erro(tokens,value)
            raise SyntaxError
    else:
        erro(tokens,value)
    return False


def regra_NUMERO(tokens):
    no = Node('NUMERO')
    try:
        check_terminal(no, tokens, 'NUMBER')
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_NUMERO)
        return no


def regra_ID(tokens):
    no = Node('ID')
    try:
        check_terminal(no, tokens, 'IDENTIFIER')
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_ID)
        return no


def regra_NOME(tokens):
    no = Node('NOME')
    try:
        if check_terminal(no, tokens, 'DOT', 1):
            check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
            check_non_terminal(no, tokens, rules.get('NOME'), regra_NOME)
            return no
        elif check_terminal(no, tokens, 'LEFT_BRACKETS', 1):
            check_non_terminal(no, tokens, rules.get('PARAMETRO'), regra_PARAMETRO)
            check_terminal(no, tokens, 'RIGHT_BRACKETS')
            return no
        elif check_terminal(no, tokens, 'LEFT_PARENTHESIS'):
            check_non_terminal(no, tokens, rules.get('LISTA_PARAM'), regra_LISTA_PARAM)
            check_terminal(no, tokens, 'RIGHT_PARENTHESIS')
            return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_NOME)
        return no


def regra_PARAMETRO(tokens):
    no = Node('PARAMETRO')
    try:
        if check_non_terminal(no, tokens, rules.get('ID'), regra_ID, 1):
            check_non_terminal(no, tokens, rules.get('NOME'), regra_NOME)
            return no
        elif check_non_terminal(no, tokens, rules.get('NUMERO'), regra_NUMERO):
            return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_PARAMETRO)
        return no


def regra_OP_MAT(tokens):
    no = Node('OP_MAT')
    try:
        if check_terminal(no, tokens, 'PLUS', 1):
            return no
        elif check_terminal(no, tokens, 'MINUS', 1):
            return no
        elif check_terminal(no, tokens, 'MUL', 1):
            return no
        elif check_terminal(no, tokens, 'DIV'):
            return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_OP_MAT)
        return no


def regra_EXP_MAT(tokens):
    no = Node('EXP_MAT')
    try:
        check_non_terminal(no, tokens, rules.get('PARAMETRO'), regra_PARAMETRO)
        if check_non_terminal(no, tokens, rules.get('OP_MAT'), regra_OP_MAT, 1):
            check_non_terminal(no, tokens, rules.get('EXP_MAT'), regra_EXP_MAT)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_EXP_MAT)
        return no

def regra_OP_LOGICO(tokens):
    no = Node('OP_LOGICO')
    try:
        if check_terminal(no, tokens, 'GREATER', 1):
            return no
        elif check_terminal(no, tokens, 'LESS', 1):
            return no
        elif check_terminal(no, tokens, 'EQUAL', 1):
            return no
        elif check_terminal(no, tokens, 'EXCLAMATION'):
            return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_OP_LOGICO)
        return no



def regra_EXP_LOGICA(tokens):
    no = Node('EXP_LOGICA')
    try:
        check_non_terminal(no, tokens, rules.get('EXP_MAT'), regra_EXP_MAT)
        if check_non_terminal(no, tokens, rules.get('OP_LOGICO'), regra_OP_LOGICO, 1):
            check_non_terminal(no, tokens, rules.get('EXP_LOGICA'), regra_EXP_LOGICA)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_EXP_LOGICA)
        return no


def regra_LISTA_PARAM(tokens):
    no = Node('LISTA_PARAM')
    try:
        check_non_terminal(no, tokens, rules.get('PARAMETRO'), regra_PARAMETRO)
        if check_terminal(no, tokens, 'COMMA', 1):
            check_non_terminal(no, tokens, rules.get('LISTA_PARAM'), regra_LISTA_PARAM)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_LISTA_PARAM)
        return no


def regra_ELSE(tokens):
    no = Node('ELSE')
    try:
        check_terminal(no, tokens, 'ELSE')
        check_non_terminal(no, tokens, rules.get('BLOCO'), regra_BLOCO)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_ELSE)
        return no


def regra_COMANDO(tokens):
    no = Node('COMANDO')
    try:
        if check_non_terminal(no, tokens, rules.get('ID'), regra_ID, 1):
            check_non_terminal(no, tokens, rules.get('NOME'), regra_NOME)
            if check_terminal(no, tokens, 'ASSIGN', 1):
                check_non_terminal(no, tokens, rules.get('EXP_MAT'), regra_EXP_MAT)
            return no
        elif check_terminal(no, tokens, 'WHILE', 1):
            check_non_terminal(no, tokens, rules.get('EXP_LOGICA'), regra_EXP_LOGICA)
            check_terminal(no, tokens, 'DO')
            check_non_terminal(no, tokens, rules.get('BLOCO'), regra_BLOCO)
            return no
        elif check_terminal(no, tokens, 'IF', 1):
            check_non_terminal(no, tokens, rules.get('EXP_LOGICA'), regra_EXP_LOGICA)
            check_terminal(no, tokens, 'THEN')
            check_non_terminal(no, tokens, rules.get('BLOCO'), regra_BLOCO)
            check_non_terminal(no, tokens, rules.get('ELSE'), regra_ELSE)
            return no
        elif check_terminal(no, tokens, 'RETURN', 1):
            check_non_terminal(no, tokens, rules.get('EXP_LOGICA'), regra_EXP_LOGICA)
            return no
        elif check_terminal(no, tokens, 'WRITE', 1):
            check_non_terminal(no, tokens, rules.get('EXP_MAT'), regra_EXP_MAT)
            return no
        elif check_terminal(no, tokens, 'READ'):
            check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
            check_non_terminal(no, tokens, rules.get('NOME'), regra_NOME)
            return no
    except SyntaxError:
        print(FOLLOW_COMANDO)
        recover(no,tokens,FOLLOW_COMANDO)
        return no


def regra_LISTA_COM(tokens):
    no = Node('LISTA_COM')
    try:
        check_non_terminal(no, tokens, rules.get('COMANDO'), regra_COMANDO)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('LISTA_COM'), regra_LISTA_COM)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_LISTA_COM)
        return no


def regra_BLOCO(tokens):
    no = Node('BLOCO')
    try:
        if check_terminal(no, tokens, 'BEGIN', 1):
            check_non_terminal(no, tokens, rules.get('COMANDO'), regra_COMANDO)
            check_terminal(no, tokens, 'SEMICOLON')
            check_non_terminal(no, tokens, rules.get('LISTA_COM'), regra_LISTA_COM)
            check_terminal(no, tokens, 'END')
            return no
        elif check_terminal(no, tokens, 'COLON'):
            check_non_terminal(no, tokens, rules.get('COMANDO'), regra_COMANDO)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_BLOCO)
        return no

def regra_PARAM_ROT(tokens):
    no = Node('PARAM_ROT')
    try:
        check_terminal(no, tokens, 'LEFT_PARENTHESIS')
        check_non_terminal(no, tokens, rules.get('CAMPOS'), regra_CAMPOS)
        check_terminal(no, tokens, 'RIGHT_PARENTHESIS')
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_PARAM_ROT)
        return no


def regra_NOME_ROTINA(tokens):
    no = Node('NOME_ROTINA')
    try:
        if check_terminal(no, tokens, 'FUNC', 1):
            check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
            check_non_terminal(no, tokens, rules.get('PARAM_ROT'), regra_PARAM_ROT)
            check_terminal(no, tokens, 'COLON')
            check_non_terminal(no, tokens, rules.get('TIPO_DADO'), regra_TIPO_DADO)
            return no
        elif check_terminal(no, tokens, 'PROCEDURE'):
            check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
            check_non_terminal(no, tokens, rules.get('PARAM_ROT'), regra_PARAM_ROT)
            return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_NOME_ROTINA)
        return no


def regra_DEF_ROT(tokens):
    no = Node('DEF_ROT')
    try:
        check_non_terminal(no, tokens, rules.get('NOME_ROTINA'), regra_NOME_ROTINA)
        check_non_terminal(no, tokens, rules.get('DEF_VAR'), regra_DEF_VAR)
        check_non_terminal(no, tokens, rules.get('BLOCO'), regra_BLOCO)
        check_non_terminal(no, tokens, rules.get('DEF_ROT'), regra_DEF_ROT)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_DEF_ROT)
        return no


def regra_LISTA_ID(tokens):
    no = Node('LISTA_ID')
    try:
        check_terminal(no, tokens, 'COMMA')
        check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
        check_non_terminal(no, tokens, rules.get('LISTA_ID'), regra_LISTA_ID)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_LISTA_ID)
        return no


def regra_VARIAVEL(tokens):
    no = Node('VARIAVEL')
    try:
        check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
        check_non_terminal(no, tokens, rules.get('LISTA_ID'), regra_LISTA_ID)
        check_terminal(no, tokens, 'COLON')
        check_non_terminal(no, tokens, rules.get('TIPO_DADO'), regra_TIPO_DADO)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_VARIAVEL)
        return no


def regra_LIST_VAR(tokens):
    no = Node('LIST_VAR')
    try:
        check_non_terminal(no, tokens, rules.get('VARIAVEL'), regra_VARIAVEL)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('LIST_VAR'), regra_LIST_VAR)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_LIST_VAR)
        return no


def regra_DEF_VAR(tokens):
    no = Node('DEF_VAR')
    try:
        check_terminal(no, tokens, 'VAR')
        check_non_terminal(no, tokens, rules.get('VARIAVEL'), regra_VARIAVEL)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('LIST_VAR'), regra_LIST_VAR)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_DEF_VAR)
        return no


def regra_LISTA_CAMPOS(tokens):
    no = Node('LISTA_CAMPOS')
    try:
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('CAMPOS'), regra_CAMPOS)
        check_non_terminal(no, tokens, rules.get('LISTA_CAMPOS'), regra_LISTA_CAMPOS)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_LISTA_CAMPOS)
        return no




def regra_CAMPOS(tokens):
    no = Node('CAMPOS')
    try:
        check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
        check_terminal(no, tokens, 'COLON')
        check_non_terminal(no, tokens, rules.get('TIPO_DADO'), regra_TIPO_DADO)
        check_non_terminal(no, tokens, rules.get('LISTA_CAMPOS'), regra_LISTA_CAMPOS)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_CAMPOS)
        return no


def regra_TIPO_DADO(tokens):
    no = Node('TIPO_DADO')
    try:
        if check_terminal(no, tokens, 'INTEGER', 1):
            return no
        elif check_terminal(no, tokens, 'REAL', 1):
            return no
        elif check_terminal(no, tokens, 'ARRAY', 1):
            check_terminal(no, tokens, 'LEFT_BRACKETS')
            check_non_terminal(no, tokens, rules.get('NUMERO'), regra_NUMERO)
            check_terminal(no, tokens, 'RIGHT_BRACKETS')
            check_terminal(no, tokens, 'OF')
            check_non_terminal(no, tokens, rules.get('TIPO_DADO'), regra_TIPO_DADO)
            return no
        elif check_terminal(no, tokens, 'RECORD', 1):
            check_non_terminal(no, tokens, rules.get('CAMPOS'), regra_CAMPOS)
            check_terminal(no, tokens, 'END')
            return no
        elif check_non_terminal(no, tokens, rules.get('ID'), regra_ID):
            return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_TIPO_DADO)
        return no


def regra_TIPO(tokens):
    no = Node('TIPO')
    try:
        check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
        check_terminal(no, tokens, 'EQUIVALENCE')
        check_non_terminal(no, tokens, rules.get('TIPO_DADO'), regra_TIPO_DADO)
        return no
    except SyntaxError:
            recover(no,tokens,FOLLOW_TIPO)
            return no


def regra_LIST_TIPOS(tokens):
    no = Node('LIST_TIPOS')
    try:
        check_non_terminal(no, tokens, rules.get('TIPO'), regra_TIPO)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('LIST_TIPOS'), regra_LIST_TIPOS)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_LIST_TIPOS)
        return no


def regra_DEF_TIPOS(tokens):
    no = Node('DEF_TIPOS')
    try:
        check_terminal(no, tokens, 'TYPE')
        check_non_terminal(no, tokens, rules.get('TIPO'), regra_TIPO)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('LIST_TIPOS'), regra_LIST_TIPOS)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_DEF_TIPOS)
        return no


def regra_CONST_VALOR(tokens):
    no = Node('CONST_VALOR')
    try:
        if check_terminal(no, tokens, 'STRING', 1):
            return no
        elif check_non_terminal(no, tokens, rules.get('EXP_MAT'), regra_EXP_MAT):
            return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_CONST_VALOR)
        return no


def regra_CONSTANTE(tokens):
    no = Node('CONSTANTE')
    try:
        check_non_terminal(no, tokens, rules.get('ID'), regra_ID)
        check_terminal(no, tokens, 'EQUIVALENCE')
        check_non_terminal(no, tokens, rules.get('CONST_VALOR'), regra_CONST_VALOR)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_CONSTANTE)
        return no


def regra_LIST_CONST(tokens):
    no = Node('LIST_CONST')
    try:
        check_non_terminal(no, tokens, rules.get('CONSTANTE'), regra_CONSTANTE)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('LIST_CONST'), regra_LIST_CONST)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_LIST_CONST)
        return no


def regra_DEF_CONST(tokens):
    no = Node('CONST')
    try:
        check_terminal(no, tokens, 'CONST')
        check_non_terminal(no, tokens, rules.get('CONSTANTE'), regra_CONSTANTE)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, rules.get('LIST_CONST'), regra_LIST_CONST)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_DEF_CONST)
        return no


def regra_DECLARACOES(tokens):
    no = Node('DECLARACOES')
    try:
        check_non_terminal(no, tokens, rules.get('DEF_CONST'), regra_DEF_CONST)
        check_non_terminal(no, tokens, rules.get('DEF_TIPOS'), regra_DEF_TIPOS)
        check_non_terminal(no, tokens, rules.get('DEF_VAR'), regra_DEF_VAR)
        check_non_terminal(no, tokens, rules.get('DEF_ROT'), regra_DEF_ROT)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_DECLARACOES)
        return no


def regra_PROGRAMA(tokens):
    no = Node('PROGRAMA')
    try:
        check_non_terminal(no, tokens, rules.get('DECLARACOES'), regra_DECLARACOES)
        check_non_terminal(no, tokens, rules.get('BLOCO'), regra_BLOCO)
        return no
    except SyntaxError:
        recover(no,tokens,FOLLOW_PROGRAMA)
        return no

def create_syntactic_tree(tokens):
    if tokens[0][0] in FIRST_PROGRAMA:
        tree = regra_PROGRAMA(tokens)
        return tree
    else:
        erro(tokens)


table = []
def add_element(name, classs, tyyppe, scope,qtd,order):
    element = {
        'name': name,
        'class': classs,
        'type': tyyppe,
        'scope': scope,
        'qtd': qtd,
        'order': order
    }
    table.append(element)

def print_elements():
    print('\n')
    for element in table:
        print(f"Name: {element['name']},class: {element['class']}, Type: {element['type']}, Scope: {element['scope']}, qtd: {element['qtd']}")

def syntactic_analyzer(tokens):
    try:
        tree = regra_PROGRAMA(tokens) #create_syntactic_tree(tokens)
        semantic(tree)
        bloco_declaration(tree.children[1],'global')
        print_elements()
        #print(tree)
        return tree
    except print as e:
        print(e)


def semantic(node):
    if node is None:
        return

    if node.get_value() == 'DEF_ROT': # dealing with functon
        function_entry(node)
    if node.get_value() == 'CONST': # const at the begining
        const_treat(node)
    if node.get_value() == 'DEF_TIPOS': # type at the begining
        tipos_treat(node)
    if node.get_value() == 'DECLARACOES': # analisando def_var, esse declaracoes garante que seja o primeiro
        find_variables(node.children[2],'global')
        

    for child in node.children:
        semantic(child)
    
def bloco_declaration(node,scope):
    if node is None:
        return
    
    if node.get_value() == 'ID':
        declared(node,scope)
    if node.get_value() == 'PARAMETRO':
        if len(node.children) == 2:
            for item in table:
                if item['name'] == node.children[0].children[0].value and  (item['scope'] == scope or item['scope'] == 'global'):
                    if(item['class'] == 'function'):
                        verify_func(node,scope)

                        if item['qtd'] != count_id(node.children[1],0):
                            print('ERRO: mais variaveis do que aceitavel para a funçao',item['name'])
                    else:
                        qtd_max = 0
                        if node.children[1].children[0].value == '[':
                            for item_a in table:
                                if item_a['name'] == node.children[0].children[0].value and (item['scope'] == scope or item['scope'] == 'global'):
                                    tipo_vetor = item['type']
                            for item_b in table:
                                if item_b['name'] == tipo_vetor:
                                    qtd_max = item_b['qtd']
                        if node.children[1].children[1].children[0].value == 'NUMERO':
                            if not (int(node.children[1].children[1].children[0].children[0].value) >= 1 and int(node.children[1].children[1].children[0].children[0].value) <= qtd_max):
                                print(f'ERRO: array {node.children[0].children[0].value} está com indice errado no {scope}')
                            

    list_nome_record = []
    
    recordd = 0
    if node.get_value() == 'COMANDO':
        for x in node.children:
            if x.value == 'ID':
                name_of_record = x.children[0].value
                recordd = recordd + 1
            if x.value == 'NOME':
                if x.children[0].value == '.':
                    recordd = recordd + 1
                    name_of_sub_type = x.children[1].children[0].value
        if recordd == 2:
            for item in table:
                if item['name'] == name_of_record and (item['scope'] == scope or item['scope'] == 'global'):
                    the_type_of_recrod = item['type']
                    #print('here')
            check = 0
            for item in table:
              #  print(the_type_of_recrod)
              #  print(scope)
                if item['scope'] == the_type_of_recrod:
                    #print(item['name'],name_of_sub_type)

                  #  print()
                    if item['name'] == name_of_sub_type:
                        check = 1
            if check == 0:
                print(f'ERRO: sub-grupo {name_of_sub_type} do record {the_type_of_recrod} invádio')
       

    for child in node.children:
        if child.get_value() != 'NOME':
            bloco_declaration(child,scope)

def deal_record(node,scope):
    if node is None:
        return

###### adicionar aqui a orde, de ID, NOME
    if node.get_value == 'ID':
        if node.children[0].value == 'ID' and node.children[1].value == 'NOME':
            print('here')

    for child in node.children:
        deal_record(child,scope)



    declared(node,scope)

def count_id(node,n):
    if node is None:
        return n

    if node.get_value() == 'ID':
        return n + 1

    for child in node.children:
        n = count_id(child,n)

    return n
    

def verify_func(node,scope):
    nome = node.children[0].children[0].value
    list_of_type_func = []
    for item in table:
        if item['class'] == 'parametro' and item['scope'] == nome:
            list_of_type_func = list_of_type_func + [item['type']]
    verify_params(node.children[1],list_of_type_func,scope)



def verify_params(node,list_of_type_func,scope):
    if node is None:
        return
    tipo = None
    if node.get_value() == 'PARAMETRO':
        for item in table:
            if item['name'] == node.children[0].children[0].value and item['scope'] == scope:
                tipo = item['type']
        if tipo not in list_of_type_func:
            print(f'ERRO: parametro {node.children[0].children[0].value} passado a funcao com tipo errado')

    for child in node.children:
        verify_params(child,list_of_type_func,scope)



def tipos_treat(node):
    if node is None:
        return
    check = 0
    if node.get_value() == 'TIPO':
        name_tipo = node.children[0].children[0].value
        for item in table:
            if item['name'] == name_tipo and item['scope'] == 'global':
                check = 1
        if check == 0:
            if node.children[2].children[0].value == 'array':
                process_array(name_tipo,node.children[2])
            elif node.children[2].children[0].value == 'record':
                add_element(name_tipo,'parametro','record','global',1,'-')
                process_record(name_tipo,node.children[2]) # adicionar a tabela todas as 
            else:
                add_element(name_tipo,'parametro',node.children[2].children[0].value,'global',1,'-')
        else:
            print(f'ERRO: variavel {name_tipo} já foi declarada')


       


    for child in node.children:
        tipos_treat(child)

def process_array(nome,node):
    qtd = node.children[2].children[0].value
    typpe = node.children[5].children[0].value
    add_element(nome,'parametro',typpe,'global',qtd,'-')

def process_record(scope,node):
    if node.children[1].get_value() == 'CAMPOS':
        get_params(node.children[1],scope)
    
def const_treat(node):
    if node is None:
        return
    
    check = 0
    if node.get_value() == 'CONSTANTE':
        name_consta = node.children[0].children[0].value
        for item in table:
            if item['name'] == name_consta and item['scope'] == 'global':
                check = 1
        if check == 0:
            val = find_type_const(node,name_consta)
        else:
            print(f'ERRO: constante {name_consta} já foi declarada')



    for child in node.children:
        const_treat(child)

def find_type_const(node,name_consta):
    if node is None:
        return

    if node.get_value() == 'CONST_VALOR':
        if node.children[0].value == 'EXP_MAT':
            add_element(name_consta,'parametro','integer','global',1,'-')
        else:
            add_element(name_consta,'parametro','string','global',1,'-')



    for child in node.children:
        find_type_const(child,name_consta)

def function_entry(node):
    for no in node.children:
        if no.value == 'NOME_ROTINA':
            counter = 0
            our_func_type = 'void' # se nao achar tipo, é considerado void
            check = 0
            for n in no.children:
                if n.get_value() == 'ID': # get function nname
                    func_name = n.children[0].value

                if n.get_value() == 'PARAM_ROT': # counting parameters of function
                    for items in n.children:
                        if items.value == 'CAMPOS':
                            counter = func_counter(items,func_name)
                            get_params(items,func_name)

                if n.get_value() == 'TIPO_DADO':
                    our_func_type = find_type(n) # pega o valor
            for item in table:
                if item['name'] == func_name and item['scope'] == 'global':
                    check = 1
                    print(f'ERRO: função {func_name} já foi declarada')
            if check == 0:
                add_element(func_name,'function',our_func_type,'global',counter,'-')
        elif no.value == 'DEF_VAR':
            find_variables(no,func_name) # adding the IDS of variables inside functon
        elif no.value == 'BLOCO':
            check_ids(no,func_name) # verificar se os ids existem e se os atributos estao certos
            bloco_declaration(no,func_name) #  TEST BLOCO INSIDE FUNCTIONS
        




def check_ids(node,scope):
    if node is None:
        return
    
    if node.get_value() == 'COMANDO':
        our_id_type = None
        if node.children[0].value == 'ID':
            print(node)
            our_id_type = declared(node.children[0],scope) # verifica se tá declarado, e se tiver retorna o tipo que ele tem
            if len(node.children) > 1 and len(node.children[1].children) > 1:
                if (node.children[1].children[0].value == '[') and (our_id_type != 'array'):
                    print(f'ERRO: Variavel {node.children[0].children[0].value} não é um array')
        if our_id_type != None:
            fiding_exp_mat_atrib(node,scope,our_id_type) # checa se os atributos recebidos estao de acordo com a variavel
    for child in node.children:
        check_ids(child,scope)

def fiding_exp_mat_atrib(node,scope,id_type): # serve para achar a sub-arvore com os atributops
    if node is None:
        return

    if node.get_value() == 'EXP_MAT':
        finding_ids(node,scope,id_type) # verifica os ids passados se tem mesmo valor


    for child in node.children:
        fiding_exp_mat_atrib(child,scope,id_type)


def finding_ids(node,scope,our_type):
    if node is None:
        return 

    if node.get_value() == 'PARAMETRO':
        check = 0 # valida se entrou em uma das possibilidades
        for item in table:
            if node.children[0].children[0].value == item['name'] and item['class'] == 'function':
                if ((item['scope'] == scope) or (item['scope'] == 'global')) and item['type'] == our_type:
                    check = 1
            #    for it in table:
             #       if it['name'] == node.children[0].children[0].value:
            if node.children[0].value == 'NUMERO':
                if ((item['scope'] == scope) or (item['scope'] == 'global')) and item['type'] == our_type:# precisa melhor pois teoricamente deveria ter acesso a variavel
                    check = 1
                

            

                   
            else:
                our_guy = node.children[0].children[0].value
                if len(node.children) > 1: # avaliando arrays e records
                    if node.children[1].value == 'NOME':
                        if node.children[1].children[0].value == '[': # se atrib verifica a tipo do vetor
                            for it in table:
                                if it['name'] == node.children[0].children[0].value and ((item['scope'] == scope) or (item['scope'] == 'global')):
                                    el_record_type = it['type']
                            for it in table:
                                if it['name'] == el_record_type and ((item['scope'] == scope) or (item['scope'] == 'global')):
                                    el_array_type = it['type']
                            if ((item['scope'] == scope) or (item['scope'] == 'global')) and el_array_type == our_type:
                               check = 1
                        elif node.children[1].children[0].value == '.': # se o atrib for com record, precisa ver o valor da varaivel dentro de record
                            for it in table:
                                if it['name'] == node.children[1].children[1].children[0].value and ((item['scope'] == scope) or (item['scope'] == 'global')):
                                    el_record_type = it['type']
                            if ((item['scope'] == scope) or (item['scope'] == 'global')) and el_record_type == our_type:
                                check = 1
                    
                else: 
                    if item['name'] == node.children[0].children[0].value and ((item['scope'] == scope) or (item['scope'] == 'global')) and item['type'] == our_type:
                        check = 1
        if check == 0:
            print('ERRO: ',node.children[0].children[0].value, 'não tem o memso tipo, no scopo',scope)
                    
                    
    for child in node.children:
        if child.get_value() != 'NOME': # garante que não entre na variavel de uma função
            finding_ids(child,scope,our_type)


def declared(node,scope):
    for item in table:
        if item['name'] == node.children[0].value and (item['scope'] == scope or item['scope'] == 'global'):
            return item['type']
    print('ERRO: variavel ',node.children[0].value, 'não declarada no escopo',scope)
    return 0


def find_variables(node,scope):
    if node is None:
        return

    if node.get_value() == 'VARIAVEL': # significa que tem variaveis
        list_of_ids = []
        list_of_ids = all_ids(node,list_of_ids) # pega a lista dos ids de determinada variavel
        our_type = find_type(node) # pega o type
        for item in list_of_ids:
            check = 0
            for items in table:
                if items['name'] == item and items['scope'] == scope and items['type'] == our_type:
                    print('ERRO: variavel',item,'já foi declarada no scopo',scope)
                    check = 1
            if check == 0:    
                add_element(item,'parametro',our_type,scope,1,'-')


    for child in node.children:
        find_variables(child,scope)


def find_type(node):
    if node is None:
        return

    if node.get_value() == 'TIPO_DADO':
        if node.children[0].value == 'ID':
            return node.children[0].children[0].value
        else:
            return node.children[0].value


    for child in node.children:
        val = find_type(child)
        if val != None:
            return val


def all_ids(node,l):
    if node is None:
        return l

    if node.get_value() == 'ID':
        return l + [node.children[0].value]
    if node.get_value() == 'TIPO_DADO':
        return l

    for child in node.children:
        l = all_ids(child,l)

    return l

def get_params(node,name):

    for n in node.children:
        if n.value == 'ID':
            param_name = n.children[0].value

        if n.value == 'TIPO_DADO':
            if n.children[0].value == 'ID':# tem types que tem id
                param_type = n.children[0].children[0].value
            else:
                param_type = n.children[0].value
            add_element(param_name,'Parametro',param_type,name,1,'-')
        
        if n.value == 'LISTA_CAMPOS':
            get_params(n.children[1],name)


def func_counter(node,name): # count paraments
    count = 0

    if node.value == 'ID':
        count += 1


    for child in node.children:
        if child.value != 'TIPO_DADO': # when it's tipo_dado means the type of the id so it's not the id that we want
            count += func_counter(child,name)


    return count
