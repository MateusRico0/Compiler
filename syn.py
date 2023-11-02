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
        if type(self.value) == type(''):
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

    def concat(self, str):
        self.value += str

    def found(self):
        if self.value: return True
        else: return False


def error(tokens):
    if not tokens.is_empty():
        raise ValueError(f"Erro: Token {tokens.current_value()} inesperado na linha {tokens.current_line()}")
    else:
        raise ValueError(f"Erro: Lista de Tokens vazia")


def check_non_terminal(no, tokens, first_list, child, ignorable=0):
    if not tokens.is_empty():
        if tokens.current_type() in first_list:
            no.add_child(child(tokens))
            return True
        elif None not in first_list and ignorable == 0:
            error(tokens)
    else:
        error(tokens)
    return False


def check_terminal(no, tokens, value, ignorable=0):
    if not tokens.is_empty():
        if tokens.current_type() == value:
            no.add_child(Node(tokens.next()))
            return True
        elif ignorable == 0:
            error(tokens)
    else:
        error(tokens)
    return False


FIRST_NUMERO = ['NUMBER']
def regra_NUMERO(tokens):
    no = Node('NUMERO')
    check_terminal(no, tokens, 'NUMBER')
    return no


FIRST_ID = ['IDENTIFIER']
def regra_ID(tokens):
    no = Node('ID')
    check_terminal(no, tokens, 'IDENTIFIER')
    return no


FIRST_NOME = ['DOT', 'LEFT_BRACKETS', 'LEFT_PARENTHESIS', None]
def regra_NOME(tokens):
    no = Node('NOME')
    if check_terminal(no, tokens, 'DOT', 1):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
    elif check_terminal(no, tokens, 'LEFT_BRACKETS', 1):
        check_non_terminal(no, tokens, FIRST_PARAMETRO, regra_PARAMETRO)
        check_terminal(no, tokens, 'RIGHT_BRACKETS')
    elif check_terminal(no, tokens, 'LEFT_PARENTHESIS'):
        check_non_terminal(no, tokens, FIRST_LISTA_PARAM, regra_LISTA_PARAM)
        check_terminal(no, tokens, 'RIGHT_PARENTHESIS')
    return no


FIRST_PARAMETRO = ['IDENTIFIER', 'NUMBER']
def regra_PARAMETRO(tokens):
    no = Node('PARAMETRO')
    if check_non_terminal(no, tokens, FIRST_ID, regra_ID, 1):
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
    elif check_non_terminal(no, tokens, FIRST_NUMERO, regra_NUMERO): pass
    return no


FIRST_OP_MAT = ['PLUS', 'MINUS', 'MUL', 'DIV']
def regra_OP_MAT(tokens):
    no = Node('OP_MAT')
    if check_terminal(no, tokens, 'PLUS', 1): pass
    elif check_terminal(no, tokens, 'MINUS', 1): pass
    elif check_terminal(no, tokens, 'MUL', 1): pass
    elif check_terminal(no, tokens, 'DIV'): pass
    return no


FIRST_EXP_MAT = ['IDENTIFIER', 'NUMBER']
def regra_EXP_MAT(tokens):
    no = Node('EXP_MAT')
    check_non_terminal(no, tokens, FIRST_PARAMETRO, regra_PARAMETRO)
    if check_non_terminal(no, tokens, FIRST_OP_MAT, regra_OP_MAT, 1):
        check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
    return no


FIRST_OP_LOGICO = ['GREATER', 'LESS', 'EQUAL', 'EXCLAMATION']
def regra_OP_LOGICO(tokens):
    no = Node('OP_LOGICO')
    if check_terminal(no, tokens, 'GREATER', 1): pass
    elif check_terminal(no, tokens, 'LESS', 1): pass
    elif check_terminal(no, tokens, 'EQUAL', 1): pass
    elif check_terminal(no, tokens, 'EXCLAMATION'): pass
    return no


FIRST_EXP_LOGICA = ['IDENTIFIER', 'NUMBER']
def regra_EXP_LOGICA(tokens):
    no = Node('EXP_LOGICA')
    check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
    if check_non_terminal(no, tokens, FIRST_OP_LOGICO, regra_OP_LOGICO, 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
    return no


FIRST_LISTA_PARAM = ['IDENTIFIER', 'NUMBER', None]
def regra_LISTA_PARAM(tokens):
    no = Node('LISTA_PARAM')
    check_non_terminal(no, tokens, FIRST_PARAMETRO, regra_PARAMETRO)
    if check_terminal(no, tokens, 'COMMA', 1):
        check_non_terminal(no, tokens, FIRST_LISTA_PARAM, regra_LISTA_PARAM)
    return no


FIRST_ELSE = ['ELSE', None]
def regra_ELSE(tokens):
    no = Node('ELSE')
    check_terminal(no, tokens, 'ELSE')
    check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
    return no


FIRST_ATRIB = ['ASSIGN', None]
def regra_ATRIB(tokens):
    no = Node('ATRIB')
    if check_terminal(no, tokens, 'ASSIGN'):
        check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
    return no


FIRST_COMANDO = ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ']
def regra_COMANDO(tokens):
    no = Node('COMANDO')
    if check_non_terminal(no, tokens, FIRST_ID, regra_ID, 1):
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
        check_non_terminal(no, tokens, FIRST_ATRIB, regra_ATRIB)
    elif check_terminal(no, tokens, 'WHILE', 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
        check_terminal(no, tokens, 'DO')
        check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
    elif check_terminal(no, tokens, 'IF', 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
        check_terminal(no, tokens, 'THEN')
        check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
        check_non_terminal(no, tokens, FIRST_ELSE, regra_ELSE)
    elif check_terminal(no, tokens, 'RETURN', 1):
        check_non_terminal(no, tokens, FIRST_EXP_LOGICA, regra_EXP_LOGICA)
    elif check_terminal(no, tokens, 'WRITE', 1):
        check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT)
    elif check_terminal(no, tokens, 'READ'):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_NOME, regra_NOME)
    return no


FIRST_LISTA_COM = ['IDENTIFIER', 'WHILE', 'IF', 'RETURN', 'WRITE', 'READ', None]
def regra_LISTA_COM(tokens):
    no = Node('LISTA_COM')
    check_non_terminal(no, tokens, FIRST_COMANDO, regra_COMANDO)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LISTA_COM, regra_LISTA_COM)
    return no


FIRST_BLOCO = ['BEGIN', 'COLON']
def regra_BLOCO(tokens):
    no = Node('BLOCO')
    if check_terminal(no, tokens, 'BEGIN', 1):
        check_non_terminal(no, tokens, FIRST_COMANDO, regra_COMANDO)
        check_terminal(no, tokens, 'SEMICOLON')
        check_non_terminal(no, tokens, FIRST_LISTA_COM, regra_LISTA_COM)
        check_terminal(no, tokens, 'END')
    elif check_terminal(no, tokens, 'COLON'):
        check_non_terminal(no, tokens, FIRST_COMANDO, regra_COMANDO)
    return no


FIRST_PARAM_ROT = ['LEFT_PARENTHESIS', None]
def regra_PARAM_ROT(tokens):
    no = Node('PARAM_ROT')
    check_terminal(no, tokens, 'LEFT_PARENTHESIS')
    check_non_terminal(no, tokens, FIRST_CAMPOS, regra_CAMPOS)
    check_terminal(no, tokens, 'RIGHT_PARENTHESIS')
    return no


FIRST_NOME_ROTINA = ['FUNC', 'PROCEDURE']
def regra_NOME_ROTINA(tokens):
    no = Node('NOME_ROTINA')
    if check_terminal(no, tokens, 'FUNC', 1):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_PARAM_ROT, regra_PARAM_ROT)
        check_terminal(no, tokens, 'COLON')
        check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    elif check_terminal(no, tokens, 'PROCEDURE'):
        check_non_terminal(no, tokens, FIRST_ID, regra_ID)
        check_non_terminal(no, tokens, FIRST_PARAM_ROT, regra_PARAM_ROT)
    return no


FIRST_DEF_ROT = ['FUNC', 'PROCEDURE', None]
def regra_DEF_ROT(tokens):
    no = Node('DEF_ROT')
    check_non_terminal(no, tokens, FIRST_NOME_ROTINA, regra_NOME_ROTINA)
    check_non_terminal(no, tokens, FIRST_DEF_VAR, regra_DEF_VAR)
    check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
    check_non_terminal(no, tokens, FIRST_DEF_ROT, regra_DEF_ROT)
    return no


FIRST_LISTA_ID = ['COMMA', None]
def regra_LISTA_ID(tokens):
    no = Node('LISTA_ID')
    check_terminal(no, tokens, 'COMMA')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_non_terminal(no, tokens, FIRST_LISTA_ID, regra_LISTA_ID)
    return no


FIRST_VARIAVEL = ['IDENTIFIER']
def regra_VARIAVEL(tokens):
    no = Node('VARIAVEL')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_non_terminal(no, tokens, FIRST_LISTA_ID, regra_LISTA_ID)
    check_terminal(no, tokens, 'COLON')
    check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    return no


FIRST_LIST_VAR = ['IDENTIFIER', None]
def regra_LIST_VAR(tokens):
    no = Node('LIST_VAR')
    check_non_terminal(no, tokens, FIRST_VARIAVEL, regra_VARIAVEL)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_VAR, regra_LIST_VAR)
    return no


FIRST_DEF_VAR = ['VAR', None]
def regra_DEF_VAR(tokens):
    no = Node('DEF_VAR')
    check_terminal(no, tokens, 'VAR')
    check_non_terminal(no, tokens, FIRST_VARIAVEL, regra_VARIAVEL)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_VAR, regra_LIST_VAR)
    return no


FIRST_LISTA_CAMPOS = ['SEMICOLON', None]
def regra_LISTA_CAMPOS(tokens):
    no = Node('LISTA_CAMPOS')
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_CAMPOS, regra_CAMPOS)
    check_non_terminal(no, tokens, FIRST_LISTA_CAMPOS, regra_LISTA_CAMPOS)
    return no


FIRST_CAMPOS = ['IDENTIFIER']
def regra_CAMPOS(tokens):
    no = Node('CAMPOS')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_terminal(no, tokens, 'COLON')
    check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    check_non_terminal(no, tokens, FIRST_LISTA_CAMPOS, regra_LISTA_CAMPOS)
    return no


FIRST_TIPO_DADO = ['INTEGER', 'REAL', 'ARRAY', 'RECORD', 'IDENTIFIER']
def regra_TIPO_DADO(tokens):
    no = Node('TIPO_DADO')
    if check_terminal(no, tokens, 'INTEGER', 1): pass
    elif check_terminal(no, tokens, 'REAL', 1): pass
    elif check_terminal(no, tokens, 'ARRAY', 1):
        check_terminal(no, tokens, 'LEFT_BRACKETS')
        check_non_terminal(no, tokens, FIRST_NUMERO, regra_NUMERO)
        check_terminal(no, tokens, 'RIGHT_BRACKETS')
        check_terminal(no, tokens, 'OF')
        check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    elif check_terminal(no, tokens, 'RECORD', 1):
        check_non_terminal(no, tokens, FIRST_CAMPOS, regra_CAMPOS)
        check_terminal(no, tokens, 'END')
    elif check_non_terminal(no, tokens, FIRST_ID, regra_ID): pass
    return no


FIRST_TIPO = ['IDENTIFIER']
def regra_TIPO(tokens):
    no = Node('TIPO')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_terminal(no, tokens, 'EQUIVALENCE')
    check_non_terminal(no, tokens, FIRST_TIPO_DADO, regra_TIPO_DADO)
    return no


FIRST_LIST_TIPOS = ['IDENTIFIER', None]
def regra_LIST_TIPOS(tokens):
    no = Node('LIST_TIPOS')
    check_non_terminal(no, tokens, FIRST_TIPO, regra_TIPO)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_TIPOS, regra_LIST_TIPOS)
    return no


FIRST_DEF_TIPOS = ['TYPE', None]
def regra_DEF_TIPOS(tokens):
    no = Node('DEF_TIPOS')
    check_terminal(no, tokens, 'TYPE')
    check_non_terminal(no, tokens, FIRST_TIPO, regra_TIPO)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_TIPOS, regra_LIST_TIPOS)
    return no


FIRST_CONST_VALOR = ['STRING', 'IDENTIFIER', 'NUMBER']
def regra_CONST_VALOR(tokens):
    no = Node('CONST_VALOR')
    if check_terminal(no, tokens, 'STRING', 1): pass
    elif check_non_terminal(no, tokens, FIRST_EXP_MAT, regra_EXP_MAT): pass
    return no


FIRST_CONSTANTE = ['IDENTIFIER']
def regra_CONSTANTE(tokens):
    no = Node('CONSTANTE')
    check_non_terminal(no, tokens, FIRST_ID, regra_ID)
    check_terminal(no, tokens, 'EQUIVALENCE')
    check_non_terminal(no, tokens, FIRST_CONST_VALOR, regra_CONST_VALOR)
    return no


FIRST_LIST_CONST = ['IDENTIFIER', None]
def regra_LIST_CONST(tokens):
    no = Node('LIST_CONST')
    check_non_terminal(no, tokens, FIRST_CONSTANTE, regra_CONSTANTE)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_CONST, regra_LIST_CONST)
    return no


FIRST_DEF_CONST = ['CONST', None]
def regra_DEF_CONST(tokens):
    no = Node('CONST')
    check_terminal(no, tokens, 'CONST')
    check_non_terminal(no, tokens, FIRST_CONSTANTE, regra_CONSTANTE)
    check_terminal(no, tokens, 'SEMICOLON')
    check_non_terminal(no, tokens, FIRST_LIST_CONST, regra_LIST_CONST)
    return no


FIRST_DECLARACOES = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', None]
def regra_DECLARACOES(tokens):
    no = Node('DECLARACOES')
    check_non_terminal(no, tokens, FIRST_DEF_CONST, regra_DEF_CONST)
    check_non_terminal(no, tokens, FIRST_DEF_TIPOS, regra_DEF_TIPOS)
    check_non_terminal(no, tokens, FIRST_DEF_VAR, regra_DEF_VAR)
    check_non_terminal(no, tokens, FIRST_DEF_ROT, regra_DEF_ROT)
    return no


FIRST_PROGRAMA = ['CONST', 'TYPE', 'VAR', 'FUNC', 'PROCEDURE', 'BEGIN', 'COLON']
def regra_PROGRAMA(tokens):
    no = Node('PROGRAMA')
    check_non_terminal(no, tokens, FIRST_DECLARACOES, regra_DECLARACOES)
    check_non_terminal(no, tokens, FIRST_BLOCO, regra_BLOCO)
    return no


def syntactic_analyzer(token_list):
    try:
        tokens = Tokens(token_list)
        tree = regra_PROGRAMA(tokens)
        return tree
    except ValueError as e:
        print(e)
