#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// All the names related to the tokens
enum TYPE {
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


struct Token createToken(enum TYPE type, const char *value) {
    struct Token token;
    token.type = type;
    strcpy(token.value, value);
    return token;
}


int main(){
    char *input = "alo";

    printf("%ld\n",input);
    printf("%c\n",*input);
    printf("%ld\n",input+1);
    printf("%c\n",*(input+1));
    printf("%ld\n",input+2);
    printf("%c\n",*(input+2));

}