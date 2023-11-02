class Tokens:
    def __init__(self, token_list):
        self.tokens = token_list

    def current(self):
        return self.tokens[0]

    def current_type(self):
        return self.tokens[0][0]

    def current_value(self):
        return self.tokens[0][1]

    def current_line(self):
        return self.tokens[0][2]

    def next(self):
        return self.tokens.pop(0)

    def is_empty(self):
        if self.tokens: return False
        else: return True


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self, level=0):
        if isinstance(self.value, str):
            result = "    " * level + "Node:" + repr(self.value) + "\n"
            for child in self.children:
                result += child.__str__(level + 1)
        else:
            result = "    " * level + "Leaf:" + repr(self.value[1]) + "\n"
        return result

    def add_child(self, child):
        self.children.append(child)


class Error_Message:
    def __init__(self):
        self.value = ""

    def concat(self, string):
        self.value += string

    def found(self):
        if self.value: return True
        else: return False


def error(tokens, message, follow_list):
    if not tokens.is_empty():
        message.concat(f"Erro: Token {tokens.current_value()} inesperado na linha {tokens.current_line()}\n")
        while (not tokens.is_empty()) and (tokens.current_value() not in follow_list):
            tokens.next()
    else:
        message.concat(f"Erro: Lista de Tokens vazia")
        raise ValueError(message.value)


def check_non_terminal(no, tokens, message, first_list, child, follow_list, ignorable=0):
    if not tokens.is_empty():
        if tokens.current_type() in first_list:
            no.add_child(child(tokens, message))
            return True
        elif None not in first_list and ignorable == 0:
            error(tokens, message, follow_list)
    else:
        error(tokens, message, follow_list)
    return False


def check_terminal(no, tokens, message, value, follow_list, ignorable=0):
    if not tokens.is_empty():
        if tokens.current_type() == value:
            no.add_child(Node(tokens.next()))
            return True
        elif ignorable == 0:
            error(tokens, message, follow_list)
    else:
        error(tokens, message, follow_list)
    return False


FIRST_NUMERO = ['NUMBER']
FOLLOW_NUMERO = ['COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
def regra_NUMERO(tokens, message):
    no = Node('NUMERO')
    check_terminal(no, tokens, message, 'NUMBER', FOLLOW_NUMERO)
    return no


FIRST_ID = ['IDENTIFIER']
FOLLOW_ID = ['EQUIVALENCE', 'SEMICOLON', 'END', 'RIGHT_PARENTHESIS', 'VAR', 'BEGIN', 'COLON', 'COMMA', 'LEFT_PARENTHESIS', 'DOT', 'LEFT_BRACKETS', 'ASSIGN', None, 'FUNC', 'PROCEDURE', 'ELSE', 'PLUS', 'MINUS', 'MUL', 'DIV', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
def regra_ID(tokens, message):
    no = Node('ID')
    check_terminal(no, tokens, message, 'IDENTIFIER', FOLLOW_ID)
    return no


FIRST_NOME = ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', None]
FOLLOW_NOME = ['ASSIGN', 'COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
def regra_NOME(tokens, message):
    no = Node('NOME')
    if check_terminal(no, tokens, message, 'DOT', ['IDENTIFIER'], 1):
        check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', 'ASSIGN', 'COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS'])
        check_non_terminal(no, tokens, message, FIRST_NOME, regra_NOME, FOLLOW_NOME)
    elif check_terminal(no, tokens, message, 'LEFT_BRACKETS', ['IDENTIFIER', 'NUMBER'], 1):
        check_non_terminal(no, tokens, message, FIRST_PARAMETRO, regra_PARAMETRO, ['RIGHT_BRACKETS'])
        check_terminal(no, tokens, message, 'RIGHT_BRACKETS', FOLLOW_NOME)
    elif check_terminal(no, tokens, message, 'LEFT_PARENTHESIS', ['IDENTIFIER', 'NUMBER', 'RIGHT_PARENTHESIS']):
        check_non_terminal(no, tokens, message, FIRST_LISTA_PARAM, regra_LISTA_PARAM, ['RIGHT_PARENTHESIS'])
        check_terminal(no, tokens, message, 'RIGHT_PARENTHESIS', FOLLOW_NOME)
    return no


FIRST_PARAMETRO = ['IDENTIFIER', 'NUMBER']
FOLLOW_PARAMETRO = ['COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS']
def regra_PARAMETRO(tokens, message):
    no = Node('PARAMETRO')
    if check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', 'COMMA', 'RIGHT_PARENTHESIS', 'PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', 'RIGHT_BRACKETS'],1):
        check_non_terminal(no, tokens, message, FIRST_NOME, regra_NOME, FOLLOW_PARAMETRO)
    elif check_non_terminal(no, tokens, message, FIRST_NUMERO, regra_NUMERO, FOLLOW_PARAMETRO): pass
    return no


FIRST_OP_MAT = ['PLUS', 'MINUS', 'MUL', 'DIV']
FOLLOW_OP_MAT = ['IDENTIFIER', 'NUMBER']
def regra_OP_MAT(tokens, message):
    no = Node('OP_MAT')
    if check_terminal(no, tokens, message, 'PLUS', FOLLOW_OP_MAT, 1): pass
    elif check_terminal(no, tokens, message, 'MINUS', FOLLOW_OP_MAT,  1): pass
    elif check_terminal(no, tokens, message, 'MUL', FOLLOW_OP_MAT,  1): pass
    elif check_terminal(no, tokens, message, 'DIV', FOLLOW_OP_MAT): pass
    return no


FIRST_EXP_MAT = ['IDENTIFIER', 'NUMBER']
FOLLOW_EXP_MAT = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN']
def regra_EXP_MAT(tokens, message):
    no = Node('EXP_MAT')
    check_non_terminal(no, tokens, message, FIRST_PARAMETRO, regra_PARAMETRO, ['PLUS', 'MINUS', 'MUL', 'DIV', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE', 'GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN'])
    if check_non_terminal(no, tokens, message, FIRST_OP_MAT, regra_OP_MAT, ['IDENTIFIER', 'NUMBER'], 1):
        check_non_terminal(no, tokens, message, FIRST_EXP_MAT, regra_EXP_MAT, FOLLOW_EXP_MAT)
    return no


FIRST_OP_LOGICO = ['GREATER', 'LESS', 'EQUAL', 'EXCLAMATION']
FOLLOW_OP_LOGICO = ['IDENTIFIER', 'NUMBER']
def regra_OP_LOGICO(tokens, message):
    no = Node('OP_LOGICO')
    if check_terminal(no, tokens, message, 'GREATER', FOLLOW_OP_LOGICO, 1): pass
    elif check_terminal(no, tokens, message, 'LESS', FOLLOW_OP_LOGICO, 1): pass
    elif check_terminal(no, tokens, message, 'EQUAL', FOLLOW_OP_LOGICO, 1): pass
    elif check_terminal(no, tokens, message, 'EXCLAMATION', FOLLOW_OP_LOGICO): pass
    return no


FIRST_EXP_LOGICA = ['IDENTIFIER', 'NUMBER']
FOLLOW_EXP_LOGICA = ['DO', 'THEN', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
def regra_EXP_LOGICA(tokens, message):
    no = Node('EXP_LOGICA')
    check_non_terminal(no, tokens, message, FIRST_EXP_MAT, regra_EXP_MAT, ['GREATER', 'LESS', 'EQUAL', 'EXCLAMATION', 'DO', 'THEN', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE'])
    if check_non_terminal(no, tokens, message, FIRST_OP_LOGICO, regra_OP_LOGICO, ['IDENTIFIER', 'NUMBER'], 1):
        check_non_terminal(no, tokens, message, FIRST_EXP_LOGICA, regra_EXP_LOGICA, FOLLOW_EXP_LOGICA)
    return no


FIRST_LISTA_PARAM = ['IDENTIFIER', 'NUMBER', None]
FOLLOW_LISTA_PARAM = ['RIGHT_PARENTHESIS']
def regra_LISTA_PARAM(tokens, message):
    no = Node('LISTA_PARAM')
    check_non_terminal(no, tokens, message, FIRST_PARAMETRO, regra_PARAMETRO, ['COMMA', 'RIGHT_PARENTHESIS'])
    if check_terminal(no, tokens, message, 'COMMA', ['IDENTIFIER', 'NUMBER', 'RIGHT_PARENTHESIS'], 1):
        check_non_terminal(no, tokens, message, FIRST_LISTA_PARAM, regra_LISTA_PARAM, FOLLOW_LISTA_PARAM)
    return no


FIRST_ELSE = ['ELSE', None]
FOLLOW_ELSE = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
def regra_ELSE(tokens, message):
    no = Node('ELSE')
    check_terminal(no, tokens, message, 'ELSE', ['BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_BLOCO, regra_BLOCO, FOLLOW_ELSE)
    return no


FIRST_ATRIB = ['ASSIGN', None]
FOLLOW_ATRIB = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
def regra_ATRIB(tokens, message):
    no = Node('ATRIB')
    if check_terminal(no, tokens, message, 'ASSIGN', ['IDENTIFIER', 'NUMBER']):
        check_non_terminal(no, tokens, message, FIRST_EXP_MAT, regra_EXP_MAT, FOLLOW_ATRIB)
    return no


FIRST_COMANDO = ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ']
FOLLOW_COMANDO = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
def regra_COMANDO(tokens, message):
    no = Node('COMANDO')
    if check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', 'ASSIGN', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE'], 1):
        check_non_terminal(no, tokens, message, FIRST_NOME, regra_NOME, ['ASSIGN', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE'])
        check_non_terminal(no, tokens, message, FIRST_ATRIB, regra_ATRIB, FOLLOW_COMANDO)
    elif check_terminal(no, tokens, message, 'WHILE', ['IDENTIFIER', 'NUMBER'], 1):
        check_non_terminal(no, tokens, message, FIRST_EXP_LOGICA, regra_EXP_LOGICA, ['DO'])
        check_terminal(no, tokens, message, 'DO', ['BEGIN', 'COLON'])
        check_non_terminal(no, tokens, message, FIRST_BLOCO, regra_BLOCO, FOLLOW_COMANDO)
    elif check_terminal(no, tokens, message, 'IF', ['IDENTIFIER', 'NUMBER'], 1):
        check_non_terminal(no, tokens, message, FIRST_EXP_LOGICA, regra_EXP_LOGICA, ['THEN'])
        check_terminal(no, tokens, message, 'THEN', ['BEGIN', 'COLON'])
        check_non_terminal(no, tokens, message, FIRST_BLOCO, regra_BLOCO, ['ELSE', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE'])
        check_non_terminal(no, tokens, message, FIRST_ELSE, regra_ELSE, FOLLOW_COMANDO)
    elif check_terminal(no, tokens, message, 'RETURN', ['IDENTIFIER', 'NUMBER'], 1):
        check_non_terminal(no, tokens, message, FIRST_EXP_LOGICA, regra_EXP_LOGICA, FOLLOW_COMANDO)
    elif check_terminal(no, tokens, message, 'WRITE', ['IDENTIFIER', 'NUMBER'], 1):
        check_non_terminal(no, tokens, message, FIRST_EXP_MAT, regra_EXP_MAT, FOLLOW_COMANDO)
    elif check_terminal(no, tokens, message, 'READ', ['IDENTIFIER']):
        check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE'])
        check_non_terminal(no, tokens, message, FIRST_NOME, regra_NOME, FOLLOW_COMANDO)
    return no


FIRST_LISTA_COM = ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ', None]
FOLLOW_LISTA_COM = ['END']
def regra_LISTA_COM(tokens, message):
    no = Node('LISTA_COM')
    check_non_terminal(no, tokens, message, FIRST_COMANDO, regra_COMANDO, ['SEMICOLON'])
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ', 'END'])
    check_non_terminal(no, tokens, message, FIRST_LISTA_COM, regra_LISTA_COM, FOLLOW_LISTA_COM)
    return no


FIRST_BLOCO = ['BEGIN', 'COLON']
FOLLOW_BLOCO = [None, 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON', 'SEMICOLON', 'ELSE']
def regra_BLOCO(tokens, message):
    no = Node('BLOCO')
    if check_terminal(no, tokens, message, 'BEGIN', ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ'], 1):
        check_non_terminal(no, tokens, message, FIRST_COMANDO, regra_COMANDO, ['SEMICOLON'])
        check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ', 'END'])
        check_non_terminal(no, tokens, message, FIRST_LISTA_COM, regra_LISTA_COM, ['END'])
        check_terminal(no, tokens, message, 'END', FOLLOW_BLOCO)
    elif check_terminal(no, tokens, message, 'COLON', ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ']):
        check_non_terminal(no, tokens, message, FIRST_COMANDO, regra_COMANDO, FOLLOW_BLOCO)
    return no


FIRST_PARAM_ROT = ['LEFT_PARENTHESIS', None]
FOLLOW_PARAM_ROT = ['COLON', 'VAR', 'BEGIN', 'COLON']
def regra_PARAM_ROT(tokens, message):
    no = Node('PARAM_ROT')
    check_terminal(no, tokens, message, 'LEFT_PARENTHESIS', ['IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_CAMPOS, regra_CAMPOS, ['RIGHT_PARENTHESIS'])
    check_terminal(no, tokens, message, 'RIGHT_PARENTHESIS', FOLLOW_PARAM_ROT)
    return no


FIRST_NOME_ROTINA = ['FUNC', 'PROCEDURE']
FOLLOW_NOME_ROTINA = ['VAR', 'BEGIN', 'COLON']
def regra_NOME_ROTINA(tokens, message):
    no = Node('NOME_ROTINA')
    if check_terminal(no, tokens, message, 'FUNC', ['IDENTIFIER'], 1):
        check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['LEFT_PARENTHESIS', 'COLON'])
        check_non_terminal(no, tokens, message, FIRST_PARAM_ROT, regra_PARAM_ROT, ['COLON'])
        check_terminal(no, tokens, message, 'COLON', ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER'])
        check_non_terminal(no, tokens, message, FIRST_TIPO_DADO, regra_TIPO_DADO, FOLLOW_NOME_ROTINA)
    elif check_terminal(no, tokens, message, 'PROCEDURE', ['IDENTIFIER']):
        check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['LEFT_PARENTHESIS', 'VAR', 'BEGIN', 'COLON'])
        check_non_terminal(no, tokens, message, FIRST_PARAM_ROT, regra_PARAM_ROT, FOLLOW_NOME_ROTINA)
    return no


FIRST_DEF_ROT = ['FUNC', 'PROCEDURE', None]
FOLLOW_DEF_ROT = ['BEGIN', 'COLON']
def regra_DEF_ROT(tokens, message):
    no = Node('DEF_ROT')
    check_non_terminal(no, tokens, message, FIRST_NOME_ROTINA, regra_NOME_ROTINA, ['VAR', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_DEF_VAR, regra_DEF_VAR, ['BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_BLOCO, regra_BLOCO, ['FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_DEF_ROT, regra_DEF_ROT, FOLLOW_DEF_ROT)
    return no


FIRST_LISTA_ID = ['COMMA', None]
FOLLOW_LISTA_ID = ['COLON']
def regra_LISTA_ID(tokens, message):
    no = Node('LISTA_ID')
    check_terminal(no, tokens, message, 'COMMA', ['IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['COMMA', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LISTA_ID, regra_LISTA_ID, FOLLOW_LISTA_ID)
    return no


FIRST_VARIAVEL = ['IDENTIFIER']
FOLLOW_VARIAVEL = ['SEMICOLON']
def regra_VARIAVEL(tokens, message):
    no = Node('VARIAVEL')
    check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['COMMA', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LISTA_ID, regra_LISTA_ID, ['COLON'])
    check_terminal(no, tokens, message, 'COLON', ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_TIPO_DADO, regra_TIPO_DADO, FOLLOW_VARIAVEL)
    return no


FIRST_LIST_VAR = ['IDENTIFIER', None]
FOLLOW_LIST_VAR = ['FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
def regra_LIST_VAR(tokens, message):
    no = Node('LIST_VAR')
    check_non_terminal(no, tokens, message, FIRST_VARIAVEL, regra_VARIAVEL, ['SEMICOLON'])
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LIST_VAR, regra_LIST_VAR, FOLLOW_LIST_VAR)
    return no


FIRST_DEF_VAR = ['VAR', None]
FOLLOW_DEF_VAR = ['FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
def regra_DEF_VAR(tokens, message):
    no = Node('DEF_VAR')
    check_terminal(no, tokens, message, 'VAR', ['IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_VARIAVEL, regra_VARIAVEL, ['SEMICOLON'])
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LIST_VAR, regra_LIST_VAR, FOLLOW_DEF_VAR)
    return no


FIRST_LISTA_CAMPOS = ['SEMICOLON', None]
FOLLOW_LISTA_CAMPOS = ['END', 'SEMICOLON', 'RIGHT_PARENTHESIS']
def regra_LISTA_CAMPOS(tokens, message):
    no = Node('LISTA_CAMPOS')
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_CAMPOS, regra_CAMPOS, ['END', 'SEMICOLON', 'RIGHT_PARENTHESIS'])
    check_non_terminal(no, tokens, message, FIRST_LISTA_CAMPOS, regra_LISTA_CAMPOS, FOLLOW_LISTA_CAMPOS)
    return no


FIRST_CAMPOS = ['IDENTIFIER']
FOLLOW_CAMPOS = ['END', 'SEMICOLON', 'RIGHT_PARENTHESIS']
def regra_CAMPOS(tokens, message):
    no = Node('CAMPOS')
    check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['COLON'])
    check_terminal(no, tokens, message, 'COLON', ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_TIPO_DADO, regra_TIPO_DADO, ['END', 'SEMICOLON', 'RIGHT_PARENTHESIS'])
    check_non_terminal(no, tokens, message, FIRST_LISTA_CAMPOS, regra_LISTA_CAMPOS, FOLLOW_CAMPOS)
    return no


FIRST_TIPO_DADO = ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER']
FOLLOW_TIPO_DADO = ['SEMICOLON', 'END', 'RIGHT_PARENTHESIS', 'VAR', 'BEGIN', 'COLON']
def regra_TIPO_DADO(tokens, message):
    no = Node('TIPO_DADO')
    if check_terminal(no, tokens, message, 'INTEGER', FOLLOW_TIPO_DADO, 1): pass
    elif check_terminal(no, tokens, message, 'REAL', FOLLOW_TIPO_DADO, 1): pass
    elif check_terminal(no, tokens, message, 'ARRAY', ['LEFT_BRACKETS'], 1):
        check_terminal(no, tokens, message, 'LEFT_BRACKETS', ['NUMBER'])
        check_non_terminal(no, tokens, message, FIRST_NUMERO, regra_NUMERO, ['RIGHT_BRACKETS'])
        check_terminal(no, tokens, message, 'RIGHT_BRACKETS', ['OF'])
        check_terminal(no, tokens, message, 'OF', ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER'])
        check_non_terminal(no, tokens, message, FIRST_TIPO_DADO, regra_TIPO_DADO, FOLLOW_TIPO_DADO)
    elif check_terminal(no, tokens, message, 'RECORD', ['IDENTIFIER'],  1):
        check_non_terminal(no, tokens, message, FIRST_CAMPOS, regra_CAMPOS, ['END'])
        check_terminal(no, tokens, message, 'END', FOLLOW_TIPO_DADO)
    elif check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, FOLLOW_TIPO_DADO): pass
    return no


FIRST_TIPO = ['IDENTIFIER']
FOLLOW_TIPO = ['SEMICOLON']
def regra_TIPO(tokens, message):
    no = Node('TIPO')
    check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['EQUIVALENCE'])
    check_terminal(no, tokens, message, 'EQUIVALENCE', ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_TIPO_DADO, regra_TIPO_DADO, FOLLOW_TIPO)
    return no


FIRST_LIST_TIPOS = ['IDENTIFIER', None]
FOLLOW_LIST_TIPOS = ['VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
def regra_LIST_TIPOS(tokens, message):
    no = Node('LIST_TIPOS')
    check_non_terminal(no, tokens, message, FIRST_TIPO, regra_TIPO, ['SEMICOLON'])
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LIST_TIPOS, regra_LIST_TIPOS, FOLLOW_LIST_TIPOS)
    return no


FIRST_DEF_TIPOS = ['TYPE', None]
FOLLOW_DEF_TIPOS = ['VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
def regra_DEF_TIPOS(tokens, message):
    no = Node('DEF_TIPOS')
    check_terminal(no, tokens, message, 'TYPE',['IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_TIPO, regra_TIPO, ['SEMICOLON'])
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LIST_TIPOS, regra_LIST_TIPOS, FOLLOW_DEF_TIPOS)
    return no


FIRST_CONST_VALOR = ['STRING', 'IDENTIFIER', 'NUMBER']
FOLLOW_CONST_VALOR = ['SEMICOLON']
def regra_CONST_VALOR(tokens, message):
    no = Node('CONST_VALOR')
    if check_terminal(no, tokens, message, 'STRING', FOLLOW_CONST_VALOR, 1): pass
    elif check_non_terminal(no, tokens, message, FIRST_EXP_MAT, regra_EXP_MAT, FOLLOW_CONST_VALOR): pass
    return no


FIRST_CONSTANTE = ['IDENTIFIER']
FOLLOW_CONSTANTE = ['SEMICOLON']
def regra_CONSTANTE(tokens, message):
    no = Node('CONSTANTE')
    check_non_terminal(no, tokens, message, FIRST_ID, regra_ID, ['EQUIVALENCE'])
    check_terminal(no, tokens, message, 'EQUIVALENCE', ['STRING', 'IDENTIFIER', 'NUMBER'])
    check_non_terminal(no, tokens, message, FIRST_CONST_VALOR, regra_CONST_VALOR, FOLLOW_CONSTANTE)
    return no


FIRST_LIST_CONST = ['IDENTIFIER', None]
FOLLOW_LIST_CONST = ['TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
def regra_LIST_CONST(tokens, message):
    no = Node('LIST_CONST')
    check_non_terminal(no, tokens, message, FIRST_CONSTANTE, regra_CONSTANTE, ['SEMICOLON'])
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LIST_CONST, regra_LIST_CONST, FOLLOW_LIST_CONST)
    return no


FIRST_DEF_CONST = ['CONST', None]
FOLLOW_DEF_CONST = ['TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
def regra_DEF_CONST(tokens, message):
    no = Node('CONST')
    check_terminal(no, tokens, message, 'CONST', ['IDENTIFIER'])
    check_non_terminal(no, tokens, message, FIRST_CONSTANTE, regra_CONSTANTE, ['SEMICOLON'])
    check_terminal(no, tokens, message, 'SEMICOLON', ['IDENTIFIER', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_LIST_CONST, regra_LIST_CONST, FOLLOW_DEF_CONST)
    return no


FIRST_DECLARACOES = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', None]
FOLLOW_DECLARACOES = ['BEGIN', 'COLON']
def regra_DECLARACOES(tokens, message):
    no = Node('DECLARACOES')
    check_non_terminal(no, tokens, message, FIRST_DEF_CONST, regra_DEF_CONST, ['TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_DEF_TIPOS, regra_DEF_TIPOS, ['VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_DEF_VAR, regra_DEF_VAR, ['FUNC', 'PROCEDURE', 'BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_DEF_ROT, regra_DEF_ROT, FOLLOW_DECLARACOES)
    return no


FIRST_PROGRAMA = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
FOLLOW_PROGRAMA = [None]
def regra_PROGRAMA(tokens):
    no = Node('PROGRAMA')
    message = Error_Message()
    check_non_terminal(no, tokens, message, FIRST_DECLARACOES, regra_DECLARACOES, ['BEGIN', 'COLON'])
    check_non_terminal(no, tokens, message, FIRST_BLOCO, regra_BLOCO, FOLLOW_PROGRAMA)
    if message.found(): raise ValueError(message.value)
    return no


def syntactic_analyzer(token_list):
    try:
        tokens = Tokens(token_list)
        tree = regra_PROGRAMA(tokens)
        return tree
    except ValueError as e:
        print(e)
