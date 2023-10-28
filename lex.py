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


#======================================================================================================================#
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


#======================================================================================================================#
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


def regra_DECLARACOES(tokens):
    no = Node("DECLARACOES")
    if tokens[0][0] in FIRST_DEF_CONST:
        no.children.append(regra_DEF_CONST(tokens))
    if tokens[0][0] in FIRST_DEF_TIPOS:
        no.children.append(regra_DEF_TIPOS(tokens))
    if tokens[0][0] in FIRST_DEF_VAR:
        no.children.append(regra_DEF_VAR(tokens))
    if tokens[0][0] in FIRST_DEF_ROT:
        no.children.append(regra_DEF_ROT(tokens))
    return no


def regra_PROGRAMA(tokens):
    no = Node("PROGRAMA")
    if tokens[0][0] in FIRST_DECLARACOES:
        no.children.append(regra_DECLARACOES(tokens))
    if tokens[0][0] in FIRST_BLOCO:
        no.children.append(regra_BLOCO(tokens))
    return no


def create_syntactic_tree(tokens):
    if tokens[0][0] in FIRST_PROGRAMA:
        tree = regra_PROGRAMA(tokens)
        return tree
    else:
        raise ValueError(f"Erro: Token {tokens[0][1]} inesperado na linha {tokens[0][2]}")


def syntactic_analyzer(tokens):
    try:
        tree = create_syntactic_tree(tokens)
        return tree
    except ValueError as e:
        print(e)



#======================================================================================================================#
if __name__ == '__main__':
    lexical_output = lexical_analyzer("input.txt")
    syntactic_output = syntactic_analyzer(lexical_output)
