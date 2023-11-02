import re
import os

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


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self, level=0):
        result = "  " * level + repr(self.value) + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result


def erro(tokens):
    if tokens:
        raise ValueError(f"Erro: Token {tokens[0][1]}, do tipo {tokens[0][0]} inesperado na linha {tokens[0][2]}")
    else:
        raise ValueError(f"Erro: token necessário não encontrado na linha {linha}")


def check_non_terminal(no, tokens, first_list, filho, ignoravel=0):
    global linha
    if tokens:
        if tokens[0][0] in first_list:
            linha = tokens[0][2]
            no.children.append(filho(tokens))
            return True
        elif None not in first_list and ignoravel == 0:
            erro(tokens)
    else:
        erro(tokens)
    return False


def check_terminal(no, tokens, value, ignoravel=0):
    if tokens:
        if tokens[0][0] == value:
            no.children.append(Node(tokens.pop(0)[1]))
            return True
        elif ignoravel == 0:
            erro(tokens)
    else:
        erro(tokens)
    return False


def regra_NUMERO(tokens):
    no = Node('NUMERO')
    check_terminal(no, tokens, 'NUMBER')
    return no


def regra_ID(tokens):
    no = Node('ID')
    check_terminal(no, tokens, 'IDENTIFIER')
    return no


def regra_NOME(tokens):
    no = Node('NOME')
    if check_terminal(no, tokens, 'DOT', 1):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
        return no
    elif check_terminal(no, tokens, 'LEFT_BRACKETS', 1):
        check_non_terminal(no, tokens, FIRST_PARAMETRO, regra_PARAMETRO)
        check_terminal(no, tokens, 'RIGHT_BRACKETS')
        return no
    elif check_terminal(no, tokens, 'LEFT_PARENTHESIS'):
        check_non_terminal(no, tokens, FIRST_LISTA_PARAM, regra_LISTA_PARAM)
        check_terminal(no, tokens, 'RIGHT_PARENTHESIS')
        return no


def regra_PARAMETRO(tokens):
    no = Node('PARAMETRO')
    if check_non_terminal(no, tokens, FIRST_ID, regra_ID, 1):
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
        return no
    elif check_non_terminal(no, tokens, FIRST_NUMERO, regra_NUMERO):
        return no


def regra_OP_MAT(tokens):
    no = Node('OP_MAT')
    if check_terminal(no, tokens, 'PLUS', 1):
        return no
    elif check_terminal(no, tokens, 'MINUS', 1):
        return no
    elif check_terminal(no, tokens, 'MUL', 1):
        return no
    elif check_terminal(no, tokens, 'DIV'):
        return no


def regra_EXP_MAT(tokens):
    no = Node('EXP_MAT')
    check_non_terminal(no, tokens, FIRST_PARAMETRO, regra_PARAMETRO)
    if check_non_terminal(no, tokens, FIRST_OP_MAT, regra_OP_MAT, 1):
        check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
    return no


def regra_OP_LOGICO(tokens):
    no = Node('OP_LOGICO')
    if check_terminal(no, tokens, 'GREATER', 1):
        return no
    elif check_terminal(no, tokens, 'LESS', 1):
        return no
    elif check_terminal(no, tokens, 'EQUAL', 1):
        return no
    elif check_terminal(no, tokens, 'EXCLAMATION'):
        return no


def regra_EXP_LOGICA(tokens):
    no = Node('EXP_LOGICA')
    check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
    if check_non_terminal(no, tokens, FIRST_OP_LOGICO, regra_OP_LOGICO, 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
    return no


def regra_LISTA_PARAM(tokens):
    no = Node('LISTA_PARAM')
    check_non_terminal(no, tokens, FIRST_PARAMETRO, regra_PARAMETRO)
    if check_terminal(no, tokens, 'COMMA', 1):
        check_non_terminal(no, tokens, FIRST_LISTA_PARAM, regra_LISTA_PARAM)
    return no


def regra_ELSE(tokens):
    no = Node('ELSE')
    check_terminal(no, tokens, 'ELSE')
    check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
    return no


def regra_COMANDO(tokens):
    no = Node('COMANDO')
    if check_non_terminal(no, tokens, FIRST_ID, regra_ID, 1):
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
        if check_terminal(no, tokens, 'ASSIGN', 1):
            check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
        return no
    elif check_terminal(no, tokens, 'WHILE', 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
        check_terminal(no, tokens, 'DO')
        check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
        return no
    elif check_terminal(no, tokens, 'IF', 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
        check_terminal(no, tokens, 'THEN')
        check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
        check_non_terminal(no, tokens, FIRST_ELSE, regra_ELSE)
        return no
    elif check_terminal(no, tokens, 'RETURN', 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
        return no
    elif check_terminal(no, tokens, 'WRITE', 1):
        check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
        return no
    elif check_terminal(no, tokens, 'READ'):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
        return no


def regra_LISTA_COM(tokens):
    no = Node('LISTA_COM')
    check_non_terminal(no, tokens, FIRST_COMANDO, regra_COMANDO)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LISTA_COM, regra_LISTA_COM)
    return no


def regra_BLOCO(tokens):
    no = Node('BLOCO')
    if check_terminal(no, tokens, 'BEGIN', 1):
        check_non_terminal(no, tokens, FIRST_COMANDO, regra_COMANDO)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, FIRST_LISTA_COM, regra_LISTA_COM)
        check_terminal(no, tokens, 'END')
        return no
    elif check_terminal(no, tokens, 'COLON'):
        check_non_terminal(no, tokens, FIRST_COMANDO, regra_COMANDO)
        return no

def regra_PARAM_ROT(tokens):
    no = Node('PARAM_ROT')
    check_terminal(no, tokens, 'LEFT_PARENTHESIS')
    check_non_terminal(no, tokens, FIRST_CAMPOS, regra_CAMPOS)
    check_terminal(no, tokens, 'RIGHT_PARENTHESIS')
    return no


def regra_NOME_ROTINA(tokens):
    no = Node('NOME_ROTINA')
    if check_terminal(no, tokens, 'FUNC', 1):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_PARAM_ROT, regra_PARAM_ROT)
        check_terminal(no, tokens, 'COLON')
        check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
        return no
    elif check_terminal(no, tokens, 'PROCEDURE'):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_PARAM_ROT, regra_PARAM_ROT)
        return no


def regra_DEF_ROT(tokens):
    no = Node('DEF_ROT')
    check_non_terminal(no, tokens, FIRST_NOME_ROTINA, regra_NOME_ROTINA)
    check_non_terminal(no, tokens, FIRST_DEF_VAR, regra_DEF_VAR)
    check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
    check_non_terminal(no, tokens, FIRST_DEF_ROT, regra_DEF_ROT)
    return no


def regra_LISTA_ID(tokens):
    no = Node('LISTA_ID')
    check_terminal(no, tokens, 'COMMA')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_non_terminal(no, tokens, FIRST_LISTA_ID, regra_LISTA_ID)
    return no


def regra_VARIAVEL(tokens):
    no = Node('VARIAVEL')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_non_terminal(no, tokens, FIRST_LISTA_ID, regra_LISTA_ID)
    check_terminal(no, tokens, 'COLON')
    check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    return no


def regra_LIST_VAR(tokens):
    no = Node('LIST_VAR')
    check_non_terminal(no, tokens, FIRST_VARIAVEL, regra_VARIAVEL)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_VAR, regra_LIST_VAR)
    return no


def regra_DEF_VAR(tokens):
    no = Node('DEF_VAR')
    check_terminal(no, tokens, 'VAR')
    check_non_terminal(no, tokens, FIRST_VARIAVEL, regra_VARIAVEL)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_VAR, regra_LIST_VAR)
    return no


def regra_LISTA_CAMPOS(tokens):
    no = Node('LISTA_CAMPOS')
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_CAMPOS, regra_CAMPOS)
    check_non_terminal(no, tokens, FIRST_LISTA_CAMPOS, regra_LISTA_CAMPOS)
    return no


def regra_CAMPOS(tokens):
    no = Node('CAMPOS')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_terminal(no, tokens, 'COLON')
    check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    check_non_terminal(no, tokens, FIRST_LISTA_CAMPOS, regra_LISTA_CAMPOS)
    return no


def regra_TIPO_DADO(tokens):
    no = Node('TIPO_DADO')
    if check_terminal(no, tokens, 'INTEGER', 1):
        return no
    elif check_terminal(no, tokens, 'REAL', 1):
        return no
    elif check_terminal(no, tokens, 'ARRAY', 1):
        check_terminal(no, tokens, 'LEFT_BRACKETS')
        check_non_terminal(no, tokens, FIRST_NUMERO, regra_NUMERO)
        check_terminal(no, tokens, 'RIGHT_BRACKETS')
        check_terminal(no, tokens, 'OF')
        check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
        return no
    elif check_terminal(no, tokens, 'RECORD', 1):
        check_non_terminal(no, tokens, FIRST_CAMPOS, regra_CAMPOS)
        check_terminal(no, tokens, 'END')
        return no
    elif check_non_terminal(no, tokens, FIRST_ID, regra_ID):
        return no


def regra_TIPO(tokens):
    no = Node('TIPO')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_terminal(no, tokens, 'EQUIVALENCE')
    check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    return no


def regra_LIST_TIPOS(tokens):
    no = Node('LIST_TIPOS')
    check_non_terminal(no, tokens, FIRST_TIPO, regra_TIPO)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_TIPOS, regra_LIST_TIPOS)
    return no


def regra_DEF_TIPOS(tokens):
    no = Node('DEF_TIPOS')
    check_terminal(no, tokens, 'TYPE')
    check_non_terminal(no, tokens, FIRST_TIPO, regra_TIPO)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_TIPOS, regra_LIST_TIPOS)
    return no


def regra_CONST_VALOR(tokens):
    no = Node('CONST_VALOR')
    if check_terminal(no, tokens, 'STRING', 1):
        return no
    elif check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT):
        return no


def regra_CONSTANTE(tokens):
    no = Node('CONSTANTE')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_terminal(no, tokens, 'EQUIVALENCE')
    check_non_terminal(no, tokens, FIRST_CONST_VALOR, regra_CONST_VALOR)
    return no


def regra_LIST_CONST(tokens):
    no = Node('LIST_CONST')
    check_non_terminal(no, tokens, FIRST_CONSTANTE, regra_CONSTANTE)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_CONST, regra_LIST_CONST)
    return no


def regra_DEF_CONST(tokens):
    no = Node('CONST')
    check_terminal(no, tokens, 'CONST')
    check_non_terminal(no, tokens, FIRST_CONSTANTE, regra_CONSTANTE)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_CONST, regra_LIST_CONST)
    return no


def regra_DECLARACOES(tokens):
    no = Node('DECLARACOES')
    check_non_terminal(no, tokens, FIRST_DEF_CONST, regra_DEF_CONST)
    check_non_terminal(no, tokens, FIRST_DEF_TIPOS, regra_DEF_TIPOS)
    check_non_terminal(no, tokens, FIRST_DEF_VAR, regra_DEF_VAR)
    check_non_terminal(no, tokens, FIRST_DEF_ROT, regra_DEF_ROT)
    return no


def regra_PROGRAMA(tokens):
    no = Node('PROGRAMA')
    check_non_terminal(no, tokens, FIRST_DECLARACOES, regra_DECLARACOES)
    check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
    return no


def create_syntactic_tree(tokens):
    if tokens[0][0] in FIRST_PROGRAMA:
        tree = regra_PROGRAMA(tokens)
        return tree
    else:
        erro(tokens)


def syntactic_analyzer(tokens):
    try:
        tree = regra_PROGRAMA(tokens) #create_syntactic_tree(tokens)
        return tree
    except ValueError as e:
        print(e)
