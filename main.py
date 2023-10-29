import lex
import syn

if __name__ == '__main__':
    lexical_output = lex.lexical_analyzer("test.txt")
    syntactic_output = syn.syntactic_analyzer(lexical_output)
    print(syntactic_output)