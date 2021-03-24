from FA import *

if __name__ == "__main__":
    str = input('输入data.in路径：')
    nfa = NFA.generateFAFromFile(str) 
    nfa.printFA()

    print('\n Generating DFA From NFA...\n')
    dfa = DFA.genDFAFromNFA(nfa)
    dfa.printFA()
