import ply.lex as lex
import ply.yacc as yacc

# from tree import print_tree_graph

variables = {}

reserved = {
    "print": "PRINT",
    "exit": "EXIT",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "endif": "ENDIF",
    "while": "WHILE",
    "do": "DO",
    "endwhile": "ENDWHILE",
    "for": "FOR",
    "endfor": "ENDFOR",
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
t_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
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
    t.value = int(t.value)
    return t


def t_PRINT(t):
    r"print"
    t.type = reserved.get(t.value, "PRINT")
    return t


def t_IF(t):
    r"if"
    t.type = reserved.get(t.value, "IF")
    return t


def t_THEN(t):
    r"then"
    t.type = reserved.get(t.value, "THEN")
    return t


def t_ELSE(t):
    r"else"
    t.type = reserved.get(t.value, "ELSE")
    return t


def t_ENDIF(t):
    r"endif"
    t.type = reserved.get(t.value, "ENDIF")
    return t


def t_WHILE(t):
    r"while"
    t.type = reserved.get(t.value, "WHILE")
    return t


def t_DO(t):
    r"do"
    t.type = reserved.get(t.value, "DO")
    return t


def t_ENDWHILE(t):
    r"endwhile"
    t.type = reserved.get(t.value, "ENDWHILE")
    return t


def t_FOR(t):
    r"for"
    t.type = reserved.get(t.value, "FOR")
    return t


def t_ENDFOR(t):
    r"endfor"
    t.type = reserved.get(t.value, "ENDFOR")
    return t


def t_COMMENT(t):
    r"\/\/.*"
    pass


def t_EXIT(t):
    r"exit"
    t.type = reserved.get(t.value, "EXIT")
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
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
        case "if":
            if exec_expression(bloc[1]):
                exec_bloc(bloc[2])
            else:
                if bloc[3] != "empty":
                    exec_bloc(bloc[3])
        case "while":
            while exec_expression(bloc[1]):
                exec_bloc(bloc[2])
        case "for":
            exec_bloc(bloc[1])
            while exec_expression(bloc[2]):
                exec_bloc(bloc[4])
                exec_bloc(bloc[3])
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


def p_if_statement(p):
    """statement : IF expression THEN bloc ENDIF
    | IF expression THEN bloc ELSE bloc ENDIF"""

    if len(p) == 6:
        p[0] = ("if", p[2], p[4], "empty")
    else:
        p[0] = ("if", p[2], p[4], p[6])


def p_while_statement(p):
    "statement : WHILE expression DO bloc ENDWHILE"

    p[0] = ("while", p[2], p[4])


def p_for_statement(p):
    "statement : FOR statement SEMICOLON expression SEMICOLON statement DO bloc ENDFOR"

    p[0] = ("for", p[2], p[4], p[6], p[8])


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

a = yacc.parse("print(1+1);a=2+3;b=a+10;c=b;b++;print(a+2);")  # type: ignore
print(variables)
a = yacc.parse("if 1<2 then a=5;b=0; endif;")  # type: ignore
print(variables)
a = yacc.parse("while b<a do b++;print(1); endwhile;")  # type: ignore
print(variables)
a = yacc.parse("for a=0; a<10; a++ do print(a); endfor;")  # type: ignore
print(variables)
