import ply.lex as lex
import ply.yacc as yacc
from genere_tree_graphviz import print_tree_graph

variables = {}

reserved = {
    "print": "PRINT",
    "exit": "EXIT",
}

tokens = (
    "NUMBER",
    "MINUS",
    "PLUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "AND",
    "OR",
    "SEMICOLON",
    "NAME",
    "EQUALS",
    "GREATER",
    "LESSER",
    "PLUSPLUS",
    "MINUSMINUS",
    "PLUSEQUALS",
    "MINUSEQUALS",
    "TIMESEQUALS",
    "DIVIDEEQUALS",
    "STRING",
    "COMMENT",
) + tuple(reserved.values())

precedence = (
    ("nonassoc", "GREATER", "LESSER"),
    ("left", "PLUS", "MINUS", "OR"),
    ("right", "TIMES", "DIVIDE"),
)


t_ignore = " \t"
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_AND = r"&&"
t_OR = r"\|\|"
t_SEMICOLON = r";"
t_EQUALS = r"="
t_GREATER = r">"
t_LESSER = r"<"
t_PLUSPLUS = r"\+\+"
t_MINUSMINUS = r"--"
t_PLUSEQUALS = r"\+="
t_MINUSEQUALS = r"-="
t_TIMESEQUALS = r"\*="
t_DIVIDEEQUALS = r"/="
t_STRING = r"(\"|\')[a-zA-Z_][a-zA-Z0-9_]+(\"|\')"


def t_NUMBER(t):
    r"\d+"
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    try:
        t.type = reserved.get(t.value, "NAME")
        return t
    except LookupError:
        pass


def t_COMMENT(t):
    r"\/\/.*"
    pass


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def exec_bloc(bloc):
    match (bloc[0]):
        case "assign":
            variables[bloc[1]] = exec_expression(bloc[2])
        case "increment":
            exec_increment(bloc[1], bloc[2])
        case "fast_assign":
            exec_fast_assign(bloc[1], bloc[2])
        case "print":
            print(exec_expression(bloc[1]))
        case "bloc":
            exec_bloc(bloc[1])
            exec_bloc(bloc[2])


def exec_increment(name, expression):
    match (expression[0]):
        case "++":
            variables[name] += 1
        case "--":
            variables[name] -= 1


def exec_fast_assign(name, expression):
    match (expression[0]):
        case "+=":
            variables[name] += exec_expression(expression[2])
        case "-=":
            variables[name] -= exec_expression(expression[2])
        case "*=":
            variables[name] *= exec_expression(expression[2])
        case "/=":
            variables[name] /= exec_expression(expression[2])


def exec_expression(expression):
    if isinstance(expression, str):
        return variables[expression]
    if not isinstance(expression, tuple):
        return expression
    match (expression[0]):
        case "+":
            return exec_expression(expression[1]) + exec_expression(expression[2])
        case "-":
            return exec_expression(expression[1]) - exec_expression(expression[2])
        case "*":
            return exec_expression(expression[1]) * exec_expression(expression[2])
        case "/":
            return exec_expression(expression[1]) / exec_expression(expression[2])
        case "&&":
            return exec_expression(expression[1]) and exec_expression(expression[2])
        case "||":
            return exec_expression(expression[1]) or exec_expression(expression[2])
        case ">":
            return exec_expression(expression[1]) > exec_expression(expression[2])
        case "<":
            return exec_expression(expression[1]) < exec_expression(expression[2])


def p_start(p):
    """start : bloc"""
    p[0] = ("start", p[1])
    exec_bloc(p[1])
    print(p[0])
    print_tree_graph(p[0])
    exec_bloc(p[1])


def p_bloc(p):
    """bloc : statement SEMICOLON
    | bloc statement SEMICOLON"""
    if len(p) == 3:
        p[0] = ("bloc", p[1], "empty")
    else:
        p[0] = ("bloc", p[1], p[2])


def p_statement_exit(p):
    "statement : EXIT"
    print("Bye")
    exit()


def p_statement_print(p):
    """statement : PRINT LPAREN expression RPAREN
    | PRINT LPAREN STRING RPAREN"""
    p[0] = ("print", p[3])


def p_statement_assign(p):
    "statement : NAME EQUALS expression"
    p[0] = ("assign", p[1], p[3])


def p_statement_plusplus_minusminus(p):
    """statement : NAME PLUSPLUS
    | NAME MINUSMINUS"""
    p[0] = ("increment", p[1], (p[2], p[1]))


def p_expression_binop_calc(p):
    """expression : expression PLUS expression
    | expression TIMES expression
    | expression MINUS expression
    | expression DIVIDE expression
    | expression AND expression
    | expression OR expression
    | expression GREATER expression
    | expression LESSER expression"""
    p[0] = (p[2], p[1], p[3])


def p_statement_someequals(p):
    """statement : NAME PLUSEQUALS expression
    | NAME MINUSEQUALS expression
    | NAME TIMESEQUALS expression
    | NAME DIVIDEEQUALS expression"""
    p[0] = ("fast_assign", p[1], (p[2], p[1], p[3]))


def p_expression_name(p):
    "expression : NAME"

    p[0] = p[1]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


parser = yacc.yacc()
lexer = lex.lex()

s = "print(1+1);a=2+3;b=a+10;c=b;b++;print(a+2);"
parser.parse(s)
print(variables)
