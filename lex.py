import re
import os

token_patterns = [
    (r'\s', None),
    (r'^#.*', None),
    (r'==', 'EQUIVALENCE'),
    (r'\bconst\b', 'CONST'),
    (r';', 'SEMICOLON'),
    (r'=', 'EQUAL'),
    (r'\btype\b', 'TYPE'),
    (r'\binteger\b', 'INTEGER'),
    (r'\breal\b', 'REAL'),
    (r'\barray\b', 'ARRAY'),
    (r'\[', 'LEFT_BRACKETS'),
    (r'\]', 'RIGHT_BRACKETS'),
    (r'\bof\b', 'OF'),
    (r'\brecord\b', 'RECORD'),
    (r':', 'COLON'),
    (r'\bvar\b', 'VAR'),
    (r',', 'COMMA'),
    (r'\bfunction\b', 'FUNC'),
    (r'\bprocedure\b', 'PROCEDURE'),
    (r'\(', 'LEFT_PARENTHESIS'),
    (r'\)', 'RIGHT_PARENTHESIS'),
    (r'\bbegin\b', 'BEGIN'),
    (r'\bend\b', 'END'),
    (r':=', 'ASSIGN'),
    (r'\bwhile\b', 'WHILE'),
    (r'\bdo\b', 'DO'),
    (r'\bif\b', 'IF'),
    (r'\bthen\b', 'THEN'),
    (r'\breturn\b', 'RETURN'),
    (r'\bwrite\b', 'WRITE'),
    (r'\bread\b', 'READ'),
    (r'\belse\b', 'ELSE'),
    (r'>', 'GREATER'),
    (r'<', 'LESS'),
    (r'!', 'EXCLAMATION'),
    (r'\+', 'PLUS'),
    (r'-', 'MINUS'),
    (r'\*', 'MUL'),
    (r'/', 'DIV'),
    (r'\.', 'DOT'),
    (r'(\d+\.\d*|\.\d+|\d+)', 'NUMBER'),
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
    (r'"[^"]*"', 'STRING'),
]

FIRST_PROGRAMA = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', None]
FIRST_DECLARACOES = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', None]
FIRST_DEF_CONST = ['CONST', None]
FIRST_LIST_CONST = ['IDENTIFIER', None]
FIRST_CONSTANTE = ['IDENTIFIER']
FIRST_CONST_VALOR = ['STRING', 'IDENTIFIER', 'NUMBER']
FIRST_DEF_TIPOS = ['TYPE', None]
FIRST_LIST_TIPOS = ['IDENTIFIER', None]
FIRST_TIPO = ['IDENTIFIER']
FIRST_TIPO_DADO = ['INTEGER', 'REAL', 'ARRAY', 'RECORD']
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
FIRST_LISTA_PARAM = ['IDENTIFIER', 'NUMBER']
FIRST_EXP_LOGICA = ['IDENTIFIER', 'NUMBER']
FIRST_OP_LOGICO = ['GREATER', 'LESS', 'EQUAL', 'EXCLAMATION']
FIRST_EXP_MAT = ['IDENTIFIER', 'NUMBER']
FIRST_OP_MAT = ['PLUS', 'MINUS', 'MUL', 'DIV']
FIRST_PARAMETRO = ['IDENTIFIER', 'NUMBER']
FIRST_NOME = ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', None]
FIRST_ID = ['IDENTIFIER']
FIRST_NUMERO = ['NUMBER']


# ======================================================================================================================#
def tokenizer(file):
    tokens = []
    line_number = 1
    while file:
        if (file[0] == '\n'):
            line_number += 1
        for pattern, token_type in token_patterns:
            match = re.match(pattern, file)
            if match:
                value = match.group(0)
                if token_type:
                    tokens.append((token_type, value, line_number))
                file = file[len(value):]
                break
        else:
            raise ValueError(f"Erro: Token {file[0]} não identificado na linha {line_number}")
    return tokens


def open_file_in_same_directory(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def lexical_analyzer(file_name):
    file = open_file_in_same_directory(file_name)
    try:
        tokens = tokenizer(file)
        return tokens
    except ValueError as e:
        print(e)


# ======================================================================================================================#
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


def regra_NUMERO(tokens):
    no = Node("NUMERO")
    return no


def regra_ID(tokens):
    no = Node("ID")
    return no


def regra_NOME(tokens):
    no = Node("NOME")
    return no


def regra_PARAMETRO(tokens):
    no = Node("PARAMETRO")
    return no


def regra_OP_MAT(tokens):
    no = Node("OP_MAT")
    return no


def regra_EXP_MAT(tokens):
    no = Node("EXP_MAT")
    return no


def regra_OP_LOGICO(tokens):
    no = Node("OP_LOGICO")
    return no


def regra_EXP_LOGICA(tokens):
    no = Node("EXP_LOGICA")
    return no


def regra_LISTA_PARAM(tokens):
    no = Node("LISTA_PARAM")
    return no


def regra_ELSE(tokens):
    no = Node("ELSE")
    return no


def regra_COMANDO(tokens):
    no = Node("COMANDO")
    return no


def regra_LISTA_COM(tokens):
    no = Node("LISTA_COM")
    return no


def regra_BLOCO(tokens):
    no = Node("BLOCO")
    return no


def regra_PARAM_ROTINA(tokens):
    no = Node("PARAM_ROTINA")
    return no


def regra_NOME_ROTINA(tokens):
    no = Node("NOME_ROTINA")
    return no


def regra_DEF_ROT(tokens):
    no = Node("DEF_ROT")
    return no


def regra_LISTA_ID(tokens):
    no = Node("LISTA_ID")
    return no


def regra_VARIAVEL(tokens):
    no = Node("VARIAVEL")
    return no


def regra_LIST_VAR(tokens):
    no = Node("LIST_VAR")
    return no


def regra_DEF_VAR(tokens):
    no = Node("DEF_VAR")
    return no


def regra_LISTA_CAMPOS(tokens):
    no = Node("LISTA_CAMPOS")
    return no


def regra_CAMPOS(tokens):
    no = Node("CAMPOS")
    return no


def regra_TIPO_DADO(tokens):
    no = Node("TIPO_DADO")
    return no


def regra_TIPO(tokens):
    no = Node("TIPO")
    return no


def regra_LIST_TIPOS(tokens):
    no = Node("LIST_TIPOS")
    return no


def regra_DEF_TIPOS(tokens):
    no = Node("DEF_TIPOS")
    return no


def regra_CONST_VALOR(tokens):
    no = Node("CONST_VALOR")
    return no


def regra_CONSTANTE(tokens):
    no = Node("CONSTANTE")
    return no


def regra_LIST_CONST(tokens):
    no = Node("LIST_CONST")
    return no


def regra_DEF_CONST(tokens):
    no = Node("CONST")
    return no


def regra_DECLARACOES(tokens):
    no = Node("DECLARACOES")
    return no


def regra_PROGRAMA(tokens):
    no = Node("PROGRAMA")
    if tokens[0][0] in FIRST_DECLARACOES:
        no.children.append( regra_DECLARACOES(tokens) )
    if tokens[0][0] in FIRST_BLOCO:
        no.children.append( regra_BLOCO(tokens) )
    return no


def create_syntactic_tree(tokens):
    if tokens[0][0] in FIRST_PROGRAMA:
        tree = regra_PROGRAMA(tokens)
        return tree


def syntactic_analyzer(tokens):
    try:
        tree = create_syntactic_tree(tokens)
        return tree
    except ValueError as e:
        print(e)


# ======================================================================================================================#
if __name__ == '__main__':
    lexical_output = lexical_analyzer("input.txt")
    syntactic_output = syntactic_analyzer(lexical_output)
