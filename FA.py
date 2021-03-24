#!/usr/bin/env python3

from __future__ import annotations
from typing import List, Dict, Set, FrozenSet

class State:
    def __init__(self, name):
        self.name: str = str(name)
        self.function: Dict[str, List[State]] = {}
    def __str__(self):
        return self.name
    def printFunctionString(self, isStart=0, isFinal=0):
        string = ''
        string += '->' if isStart else '  '
        string += '*' if isFinal else ' '
        string += self.name.ljust(20)
        for x in sorted(self.function):
            string += f'\t{State.stateListToStr(self.function[x]).ljust(20)}' 
        print(string)

    @classmethod
    def stateListToStr(cls, states: List[State]):
        return str([str(x) for x in states])
        

class NFA:
    def __init__(self):
        # All the states are represented by numbers string from 0 ~ (n-1)
        self.states: List[State] = []
        self.states_num: int = 0
        self.input: List[str] = []
        self.start_state: State = State(0)
        self.final_states: List[State] = []
    @classmethod
    def generateFAFromFile(cls, filename: str) -> NFA:
        nfa = cls()
        with open(filename, 'r', encoding='utf-8') as f:
            nfa.states_num = int(next(f).strip())
            nfa.states = [State(str(x)) for x in range(nfa.states_num)]
            nfa.input = [x for x in next(f).strip().split(' ')]
            funcfile = next(f).strip()
            nfa.getFunctionsFromFile(funcfile)
            nfa.start_state = nfa.states[int(next(f).strip())]
            nfa.final_states = [nfa.states[x] for x in eval(next(f).strip())]
        return nfa

    def getFunctionsFromFile(self, filename: str) -> None:
        with open(filename, 'r', encoding='utf-8') as f:
            func_list = eval(f.read()) 
            for x in range(0, self.states_num):
                for y in func_list[x]:
                    func_list[x][y] = [self.states[z] for z in func_list[x][y]]
                self.states[x].function = func_list[x]

    def printFA(self):
        print(f'states_num: {self.states_num}')
        print(f'input: {self.input}')
        print(f'start_state: {self.start_state}')
        print(f'final_states: {[str(x) for x in self.final_states]}')
        print(f'functions:')
        self._printFunctions()

    def _printFunctions(self):
        string = 'State'.ljust(20)
        for x in sorted(self.input): 
            string += f'\t{x.ljust(20)}'
        print(string)
        for x in self.states:
            x.printFunctionString(x == self.start_state, x in self.final_states)

class DFA(NFA):
    def __init__(self):
        super(DFA, self).__init__()

    @classmethod
    def genDFAFromNFA(cls, nfa: NFA) -> DFA:
        dfa = cls()
        dfa.input = nfa.input
        # A queue of new NFA combinations(List[State])
        state_queue: List[Set[State]] = [{nfa.start_state}]
        init_state = State(State.stateListToStr([nfa.start_state]))
        dfa.start_state = init_state
        dfa_states: Dict[FrozenSet[State], State] = {frozenset([ nfa.start_state ]): init_state}

        while state_queue:
            states = frozenset(state_queue.pop())
            dfa.states.append(dfa_states[states])
            dfa.states_num+=1
            if set(nfa.final_states) | states == states:
                dfa.final_states.append(dfa_states[states])

            for input in nfa.input:
                dest_states = set()
                for state in states:
                    dest_states |= set(state.function[input])
                dest_states = frozenset(dest_states)
                if dest_states not in dfa_states:
                    state_queue.append(set(dest_states))
                    new_state = State(State.stateListToStr(list(dest_states)))
                    dfa_states[dest_states] = new_state
                dfa_states[states].function[input] = [ dfa_states[dest_states] ]

        return dfa

