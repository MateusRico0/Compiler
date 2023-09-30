import re
import os


def open_file_in_same_directory(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def save_file_in_same_directory(tokens):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'output.txt')
    f = open(file_path, 'w')
    for token in tokens:
        f.write(token)
    f.close()


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


def tokezizer(file):
    tokens = []
    line_number = 1
    while file:
        if (file[0] == '\n'):
            line_number += 1
        for pattern, token_type in token_patterns:
            match = re.match(pattern, file)
            # print('match',match)
            # print('PATTERN',pattern)
            # print('TOKEN',token_type)
            if match:
                # print("1\n")
                value = match.group(0)
                if token_type:
                    tokens.append((token_type, value, line_number))
                    # print('vall: ', value)
                file = file[len(value):]
                break
        else:
            raise ValueError(f"Erro: Token {file[0]} não identificado na linha {line_number}")

    return tokens


if __name__ == '__main__':
    file = open_file_in_same_directory("real_text.txt")
    try:
        tokens = tokezizer(file)
        all_tokens = []
        for token_type, value, line_number in tokens:
            token_string = f'Value: {value}, Type: {token_type}, Line: {line_number}\n'
            all_tokens.append(token_string)
            # print(token_string)
        save_file_in_same_directory(all_tokens)
    except ValueError as e:
        print(e)

