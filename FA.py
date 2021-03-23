#!/usr/bin/env python3

from __future__ import annotations
from typing import List, Dict


class NFA:
    def __init__(self):
        # All the states are represented by numbers from 0 ~ (n-1)
        self.states: List[int] = []
        self.states_num: int = 0
        self.input: List[str] = []
        self.functions: List[Dict[str, List[int]]] = []
        self.start_state = 0
        self.final_states: List[int] = []

    @classmethod
    def generateFAFromFile(cls, filename: str) -> NFA:
        nfa = cls()
        with open(filename, 'r', encoding='utf-8') as f:
            nfa.states_num = int(next(f).strip())
            nfa.states = list(range(0, nfa.states_num))
            nfa.input = [x for x in next(f).strip().split(' ')]
            nfa.functions = cls.getFunctionsFromFile(next(f).strip())
            nfa.start_state = int(next(f).strip())
            nfa.final_states = eval(next(f).strip())
        return nfa
        
    @classmethod
    def getFunctionsFromFile(cls, filename: str) -> List:
        func = []
        with open(filename, 'r', encoding='utf-8') as f:
            func = eval(f.read()) 
        return func

    def printFA(self):
        print(f'states_num: {self.states_num}')
        print(f'input: {self.input}')
        print(f'functions:')
        self.printFunctions()
        print(f'start_state: {self.start_state}')
        print(f'final_states: {self.final_states}')

    def printFunctions(self):
        print('From\tInput\tTo')
        for x in range(self.states_num):
            for key, val in self.functions[x].items():
                print(f'{x}\t{key}\t{val}')

class DFA(NFA):
    def __init__(self):
        super(NFA, self).__init__()
        self.functions: List[Dict[str, int]] = []

