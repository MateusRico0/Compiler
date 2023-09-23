#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// All the names related to the tokens
enum Type {
    CONST,
    TYPE,
    INTEGER,
    REAL,
    ARRAY,
    RECORD,
    VAR,
    END,
    FUNC,
    PROCEDURE,
    BEGIN,
    WHILE,
    DO,
    IF,
    ELSE,
    THEN,
    RETURN,
    WRITE,
    READ,
    GREATER,
    LESS,
    PLUS,
    MINUS,
    MUL,
    EXCLAMATION,
    DIV,
    DOT,
    EQUAL,
    ASSIGN,
    LEFT_BRACKETS,
    RIGHT_BRACKETS,
    OF,
    COLON,
    SEMICOLON,
    LEFT_PARENTHESIS,
    RIGHT_PARENTHESIS,
    COMMA
};

// info about the tokens
struct Token {
    enum TYPE type;
    char value[20];
    int line;
};
