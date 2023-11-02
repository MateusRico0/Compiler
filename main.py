import lex
import syn


if __name__ == '__main__':
    lexical_output = lex.lexical_analyzer("input.txt")
    syntactic_output = syn.syntactic_analyzer(lexical_output)
    if syntactic_output: print(syntactic_output)