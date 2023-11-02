import re
import os


def tokenizer(file):
    token_patterns = [
        (r'\s', None),
        (r'^#.*', None),
        (r'==', 'EQUIVALENCE'),
        (r':=', 'ASSIGN'),
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
        (r'"[^"]*"', 'STRING')
    ]
    tokens = []
    line_number = 1
    while file:
        if file[0] == '\n':
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
