from g04_PLC_lexico import tokens
import ply.yacc as yacc
#Para poder ler argumentos da command line
import sys

def p_init(p):
    "Init : Cmds"
    p[0] = p[1]
    
def p_cmds(p):
    "Cmds : Cmd Cmds"
    p[0] = p[1] + p[2]

def p_cmds2(p):
    "Cmds : "
    p[0] = ""
    
def p_cmd1(p):
    "Cmd : Cmd_If"
    p[0] = p[1]
    
def p_cmd2(p):
    "Cmd : Cmd_If_Else"
    p[0] = p[1]

def p_cmd3(p):
    "Cmd : Cmd_While"
    p[0] = p[1]

def p_cmd4(p):
    "Cmd : Cmd_For"
    p[0] = p[1]

def p_cmd5(p):
    "Cmd : Cmd_Write"
    p[0] = p[1]

def p_cmd_write(p):
    "Cmd_Write : PRINT '(' Exp ')'"
    p[0] = p[3] + "WRITEI\n"

def p_cmd_read(p):
    "Cmd_Read : INPUT '(' ID ')'"
    if p[3] in parser.vars:
        p[0] = f"READ\nATOI\nSTOREG {parser.vars[p[3]][0]}"

def p_cmd_read1(p):
    "Cmd_Read : INPUT '(' ID '[' Exp ']' ')'"
    if p[3] in parser.arrs:
        p[0] = f"PUSHG {parser.arrs[p[3]][0]}\n" + p[5] + f"READ\nATOI\nSTOREN\n"

def p_cmd6(p):
    "Cmd : Cmd_Read"
    p[0] = p[1]

def p_cmd7(p):
    "Cmd : Atrib ';'"
    p[0] = p[1]

def p_atrib(p):
    "Atrib : Atrib_var"
    p[0] = p[1]

def p_atrib1(p):
    "Atrib : Atrib_arr"
    p[0] = p[1]

def p_atrib_var(p):
    "Atrib_var : ID '=' Exp"
    if p[1] in parser.vars:
        p[0] = p[3] + f"STOREG {parser.vars[p[1]][0]}\n"

def p_atrib_arr(p):
    "Atrib_arr : ID '[' Exp ']' '=' Exp"
    if p[1] in parser.arrs:
        p[0] = f"PUSHG {parser.arrs[p[1]][0]}\n" + p[3] + p[6] + "STOREN\n"
    else:
        parser.sucesso = False
        print('Erro! Array' + p[1] + "nao existe!")

def p_cmd9(p):
    "Cmd : VARS"
    p[0] = p[1]

def p_vars(p):
    "VARS : Decl VARS"
    p[0] = p[1] + p[2]

def p_vars1(p):
    "VARS : "
    p[0] = ""

def p_decl(p):
    "Decl : VAR IdList ';'"
    for v in p[2]:
        parser.vars[v] = (parser.gp,0)
        parser.gp+=1
    p[0] = ""
        
def p_decl1(p):
    "Decl : ARR ID '[' NUM ']' ';'"
    var = p[2]
    size = int(p[4])
    parser.arr[var] = (parser.gp,size)
    parser.gp+=1
    p[0] = ""

def p_idlist(p):
    "IdList : ID"
    p[0] = [p[1]]

def p_idlist1(p):
    "IdList : ID ',' IdList"
    p[0] = [p[1]] + p[3]

def p_cmd_if(p):
    "Cmd_If : IF '(' Cond ')' THEN '{' Cmds '}'"
    p[0] = p[3] + f"JZ ponto{parser.pts}\n" + p[7] + f"ponto{parser.pts}:\n"
    parser.pts+=1

def p_cmd_if_then(p):
    "Cmd_If_Else : IF '(' Cond ')' THEN '{' Cmds '}' ELSE '{' Cmds '}'"
    p[0] = p[3] + f"JZ ponto{parser.pts}\n" + p[7] + f"PUSHA ponto{parser.pts+1}\nCALL\nponto{parser.pts}:\n" + p[11] + f"ponto{parser.pts+1}:\n"
    parser.pts+=2

def p_cmd_while(p):
    "Cmd_While : WHILE '(' Cond ')' DO '{' Cmds '}'"
    p[0] = f"ponto{parser.pts}:\n" + p[3] + f"JZ ponto{parser.pts+1}\n" + p[7] + f"PUSHA ponto{parser.pts}\nCALL\nponto{parser.pts+1}:\n"
    parser.pts+=2

def p_cmd_for(p):
    "Cmd_For : FOR '(' Atrib ';' Cond ';' Atrib ')' DO '{' Cmds '}'"
    p[0] = p[3] + f"ponto{parser.pts}:\n" + p[5] + f"JZ ponto{parser.pts+1}\n" + p[11] + p[7] + f"PUSHA ponto{parser.pts}\nCALL\nponto{parser.pts+1}:\n"
    parser.pts+=2

def p_exp_add(p):
    "Exp : Exp '+' Exp"
    p[0] = p[1] + p[3] + "ADD\n"

def p_exp_sub(p):
    "Exp : Exp '-' Exp"
    p[0] = p[1] + p[3] + "SUB\n"

def p_exp_mul(p):
    "Exp : Exp '*' Exp"
    p[0] = p[1] + p[3] + "MUL\n"

def p_exp_div(p):
    "Exp : Exp '/' Exp"
    p[0] = p[1] + p[3] + "DIV\n"

def p_exp_mod(p):
    "Exp : Exp '%' Exp"
    p[0] = p[1] + p[3] + "MOD\n"

def p_exp_factor(p):
    "Exp : Factor"
    p[0] = p[1]

def p_factor_num(p):
    "Factor : NUM"
    p[0] = f"PUSHI {p[1]}\n"

def p_factor_ID(p):
    "Factor : ID"
    if p[1] in parser.vars:
        p[0] = f"PUSHG {parser.vars[p[1]][0]}\n"
    else:
        parser.sucesso = False
        print(f"Variavel {p[1]} nao definida")

def p_factor_Arr(p):
    "Factor : ID '[' Exp ']'"
    if p[1] in parser.arrs:
        p[0] = f"PUSHG {parser.arrs[p[1]][0]}\n" + p[3] + "LOADN\n"
    else:
        parser.sucesso = False
        print(f"Variavel {p[1]} nao definida")

def p_factor_exp(p):
    "Factor : '(' Exp ')'"
    p[0] = p[2]

def p_cond_not(p):
    "Cond : NOT Cond"
    p[0] = p[2] + "NOT\n"

def p_cond_and(p):
    "Cond : Cond AND Cond"
    p[0] = p[2] + "AND\n"

def p_cond_or(p):
    "Cond : Cond OR Cond"
    p[0] = p[2] + "OR\n"

def p_cond_sup(p):
    "Cond : Exp '>' Exp"
    p[0] = p[1] + p[3] + "SUP\n"

def p_cond_supq(p):
    "Cond : Exp '>' '=' Exp"
    p[0] = p[1] + p[4] + "SUPQ\n"

def p_cond_inf(p):
    "Cond : Exp '<' Exp"
    p[0] = p[1] + p[3] + "INF\n"

def p_cond_infq(p):
    "Cond : Exp '<' '=' Exp"
    p[0] = p[1] + p[4] + "INFQ\n"

def p_cond_equals(p):
    "Cond : Exp '=' '=' Exp"
    p[0] = p[1] + p[4] + "EQUAL\n"

def p_cond_nequeals(p):
    "Cond : Exp '!' '=' Exp"
    p[0] = p[1] + p[4] + "EQUAL\nNOT\n"


def p_error(p):
    print('Syntax error! ',p)
    parser.sucesso = False


parser = yacc.yacc()
parser.sucesso = True
parser.vars = {}
parser.arrs = {}
parser.pts = 0
parser.gp = 0


if "-h" in sys.argv:
    print(f"Usage: python {sys.argv[0]} filename(.sus) (-o savefile [optional])")
    sys.exit()
try:
    filename = sys.argv[1]
    output = filename [:-4] + ".out"
    if "-o" in sys.argv:
        output = sys.argv[3]
    if not filename.endswith(".sus"):
        print("Filename has to end with .sus")
        sys.exit()
except (ValueError, IndexError):
    print("Use -h to get instruction")
    sys.exit()

try:
    with open(filename,"r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File not found.")
    sys.exit()


res = parser.parse(content)
allvars = {}
allvars.update(parser.vars)
allvars.update(parser.arrs)

allvars = {k: v for k, v in sorted(allvars.items(), key=lambda item: item[1][0])}

variavies = ""
for v in allvars.keys():
    if allvars[v][1] == 0:
        variavies += "PUSHI 0\n"
    else:
        variavies += f"ALLOC {allvars[v][1]}\n"

res = variavies + "START\n" + res
        
if (parser.sucesso):
    with open(output,"w") as f:
       f.write(res)
    print("Your input was correctly parsed")
else:
    print("Sintax error!")