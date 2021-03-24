from FA import *

if __name__ == "__main__":
    nfa = NFA.generateFAFromFile("./data.in") 
    nfa.printFA()

    print('\n Generating DFA From NFA...\n')
    dfa = DFA.genDFAFromNFA(nfa)
    dfa.printFA()
