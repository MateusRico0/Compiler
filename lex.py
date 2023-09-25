import re
import os


def open_file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)
   with open(file_path, 'r') as file:
      content = file.read()
   return content


token_patterns = [
    (r'const', 'CONST'),
    (r';', 'SEMICOLON'),
    (r'=', 'EQUAL'),
    (r'type', 'TYPE'),
    (r'integer', 'INTEGER'),
    (r'real', 'REAL'),
    (r'array', 'ARRAY'),
    (r'\[', 'LEFT_BRACKETS'),
    (r'\]', 'RIGHT_BRACKETS'),
    (r'of', 'OF'),
    (r'record', 'RECORD'),
    (r':', 'COLON'),
    (r'var', 'VAR'),
    (r',', 'COMMA'),
    (r'function', 'FUNC'),
    (r'procedure', 'PROCEDURE'),
    (r'\(', 'LEFT_PARENTHESIS'),
    (r'\)', 'RIGHT_PARENTHESIS'),
    (r'begin', 'BEGIN'),
    (r'end', 'END'),
    (r':=', 'ASSIGN'),
    (r'while', 'WHILE'),
    (r'do', 'DO'),
    (r'if', 'IF'),
    (r'then', 'THEN'),
    (r'return', 'RETURN'),
    (r'write', 'WRITE'),
    (r'read', 'READ'),
    (r'else', 'ELSE'),
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
    (r'\s', None),
    (r'"[^"]*"', 'STRING')
]


def tokezizer(file):
    tokens = []
    line_number = 1
    while file:
        if(file[0] == '\n'):
            line_number += 1
        for pattern, token_type in token_patterns:
            match = re.match(pattern, file)
            if match:
                value = match.group(0)
                if token_type:
                    print('t',token_type)
                    if token_type == 'STRING':
                        print('values',value)
                        tokens.append((token_type, value[1:-1], line_number))
                    else:
                        tokens.append((token_type, value, line_number))
                file = file[len(value):]
                break
    return tokens


if __name__ == '__main__':
    file = open_file_in_same_directory("real_text.txt")
    tokens = tokezizer(file)
    all_tokens = []
    for token_type, value, line_number in tokens:
        token_string = f'Type: {token_type}, Value: {value}, Line: {line_number}'
        all_tokens.append(token_string)
        print(token_string)