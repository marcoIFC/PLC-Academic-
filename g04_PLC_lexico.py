from re import *
import ply.lex as lex

'''
Init        : Cmds

Cmds        : Cmd Cmds
            | €

Cmd         : Cmd_If
            | Cmd_If_Else
            | Cmd_While
            | Cmd_For
            | Cmd_Write
            | Cmd_Read
            | Atrib
            | VARS

Atrib       : Atrib_var
            | Atrib_arr

Atrib_var   : ID '=' Exp

Atrib_arr   : ID '[' Exp ']' '=' Exp

VARS        : Decl VARS
            | €

Decl        : VAR IdList ';'
            | ARR ID '[' NUM ']' ';'

IdList      : ID
            | ID ',' IdList

Cmd_If      : IF '(' Cond ')' THEN '{' Cmds '}' 

Cmd_If_Else : IF '(' Cond ')' THEN '{' Cmds '}' ELSE '{' Cmds '}' 

Cmd_While   : WHILE '(' Cond ')' DO '{' Cmds '}' 

Cmd_For     : FOR '(' ID '=' Exp ';' Cond ';' ID '=' Exp ')' DO '{' Cmds '}'

Cmd_Write   : WRITE '(' Exp ')' ';'

Cmd_Read    : READ '(' ID ')' ';'

Exp         : Exp '+' Exp
            | Exp '-' Exp
            | Exp '*' Exp
            | Exp '/' Exp
            | Exp '%' Exp
            | Factor

Factor      : NUM
            | ID
            | ID '[' Exp ']'
            | '(' Exp ')'

Cond        : NOT Cond
            | Cond AND Cond
            | Cond OR Cond
            | Exp '>' Exp
            | Exp '<' Exp
            | Exp '>' '=' Exp
            | Exp '<' '=' Exp
            | Exp '=' '=' Exp
            | Exp '!' '=' Exp

----            
VAR: 
p0 = 'pushi' p2        
'''

literals = ('{', '}', ',', '[', ']', '(', ')','=',';','+','-','*','>','<','!')

tokens = [
    'ID',
    'NUM'
]

p_reservadas = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'write': 'WRITE',
    'read': 'READ',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'var': 'VAR',
    'arr': 'ARR',
    'input': 'INPUT',
    'print': 'PRINT'
}

tokens += list(p_reservadas.values())  #Atualiza os tokens com palavras reservadas


def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = p_reservadas.get(t.value, 'ID') # Checka as palavras reservadas
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

t_ignore = ' \n\t'

def t_error(t):
    print(f"Caractére inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# NOTA: Não sei se é preciso criar outra função só para o \n