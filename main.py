import ply.lex as lex
import ply.yacc as yacc

# from tree import print_tree_graph

from dataclasses import dataclass


@dataclass
class Config:
    in_function: bool = False
    returned: bool = False


variables = {}
global_variables = {}
functions = {}
config = Config()

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
    "function": "FUNCTION",
    "endfunction": "ENDFUNCTION",
    "return": "RETURN",
    "global": "GLOBAL",
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
    "EQUALSEQUALS",
    "GREATEREQUALS",
    "LESSEREQUALS",
    "PLUSPLUS",
    "MINUSMINUS",
    "PLUSEQUALS",
    "MINUSEQUALS",
    "TIMESEQUALS",
    "DIVIDEEQUALS",
    "STRING",
    "COMMENT",
    "COMMA",
    "LEFT_ARRAY",
    "RIGHT_ARRAY",
) + tuple(reserved.values())

precedence = (
    ("left", "PLUS", "MINUS", "OR", "GREATER", "LESSER"),
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
t_EQUALSEQUALS = r"=="
t_GREATEREQUALS = r">="
t_LESSEREQUALS = r"<="
t_PLUSPLUS = r"\+\+"
t_MINUSMINUS = r"--"
t_PLUSEQUALS = r"\+="
t_MINUSEQUALS = r"-="
t_TIMESEQUALS = r"\*="
t_DIVIDEEQUALS = r"/="
t_STRING = r"(\").[^\"]*(\")"
t_COMMA = r","
t_LEFT_ARRAY = r"\["
t_RIGHT_ARRAY = r"\]"


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


def t_EXIT(t):
    r"exit"
    t.type = reserved.get(t.value, "EXIT")
    return t


def t_FUNCTION(t):
    r"function"
    t.type = reserved.get(t.value, "FUNCTION")
    return t


def t_ENDFUNCTION(t):
    r"endfunction"
    t.type = reserved.get(t.value, "ENDFUNCTION")
    return t


def t_RETURN(t):
    r"return"
    t.type = reserved.get(t.value, "RETURN")
    return t


def t_COMMENT(t):
    r"\/\/.*"
    pass


def t_GLOBAL(t):
    r"global"
    t.type = reserved.get(t.value, "GLOBAL")
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def exec_bloc(bloc):
    if config.returned and config.in_function:
        return
    match (bloc[0]):
        case "function":
            functions[bloc[1]] = (bloc[2], bloc[3])
        case "call":
            return exec_function_call(bloc[1], bloc[2])
        case "return":
            config.returned = True
            return exec_expression(bloc[1])
        case "assign":
            variables[bloc[1]] = exec_expression(bloc[2])
        case "multiple_assign":
            variables_name = exec_get_variables_name_multi_assign([], bloc[1])
            variables_name.reverse()
            values = exec_assign_array([], bloc[2])
            values.reverse()
            for name, value in zip(variables_name, values):
                variables[name] = value
        case "global_new":
            global_variables[bloc[1]] = exec_expression(bloc[2])
        case "global_exist":
            global_variables[bloc[1]] = variables[bloc[1]]
        case "array":
            new_list = exec_assign_array([], bloc[2])
            new_list.reverse()
            variables[bloc[1]] = new_list
        case "array_assign":
            variables[bloc[1]][exec_expression(bloc[2])] = exec_expression(bloc[3])
        case "increment":
            exec_increment(bloc[1], bloc[2])
        case "fast_assign":
            exec_fast_assign(bloc[1], bloc[2])
        case "print":
            values = exec_assign_array([], bloc[1])
            values.reverse()
            print(" ".join(map(str, values)))
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
            ret = exec_bloc(bloc[1])
            ret_ = exec_bloc(bloc[2])
            return ret_ or ret


def exec_get_variables_name_multi_assign(values, parameters):
    values.append(parameters[1])
    if parameters[2] == "empty":
        return values
    return exec_get_variables_name_multi_assign(values, parameters[2])


def get_height(parameters):
    if parameters[2] == "empty":
        return 0
    return 1 + get_height(parameters[2])


def exec_get_signature(parameters, arguments, func_dict):
    func_dict[parameters[1]] = exec_expression(arguments[1])
    if parameters[2] == "empty":
        return func_dict
    return exec_get_signature(parameters[2], arguments[2], func_dict)


def exec_function_call(name, arguments):
    try:
        parameters, bloc = functions[name]
    except KeyError:
        print(f"Function {name} not found")
        exit()
    if arguments == "empty" and parameters == "empty":
        pass
    elif get_height(parameters) != get_height(arguments):
        print(f"Wrong number of arguments for function {name}")
        exit()
    variables_functions = {}
    if arguments != "empty" and parameters != "empty":
        exec_get_signature(parameters, arguments, variables_functions)
    variables_copy = variables.copy()
    variables.clear()
    variables.update(variables_functions)
    config.in_function = True
    a = exec_bloc(bloc)
    config.returned = False
    config.in_function = False
    variables.clear()
    variables.update(variables_copy)
    return a


def exec_assign_array(values, arguments):
    values.append(exec_expression(arguments[1]))
    if arguments[2] == "empty":
        return values
    return exec_assign_array(values, arguments[2])


def exec_index_array(values, indexs):
    values.append(exec_expression(indexs[1][1]))
    if indexs[2] == "empty":
        return values
    return exec_index_array(values, indexs[2])


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
        try:
            return variables[expression]
        except KeyError:
            try:
                return global_variables[expression]
            except KeyError:
                pass
            if expression.count('"') == 2 or expression.count("'") == 2:
                return expression[1:-1]
            print(f"Variable {expression} not found")
            exit()
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
        case "==":
            return exec_expression(expression[1]) == exec_expression(expression[2])
        case ">=":
            return exec_expression(expression[1]) >= exec_expression(expression[2])
        case "<=":
            return exec_expression(expression[1]) <= exec_expression(expression[2])
        case "call":
            return exec_function_call(expression[1], expression[2])
        case "array_get":
            new_list = exec_index_array([], expression[2])
            value = variables[expression[1]]
            for i in new_list:
                try:
                    value = value[i]
                except KeyError:
                    try:
                        value = global_variables[expression[1]][i]
                    except KeyError:
                        print(f"Variable {expression[1]} not found")
                        exit()
                except TypeError:
                    error_list_str = ""
                    for i in new_list:
                        error_list_str += f"[{i}]"
                    print(f"Variable {expression[1]}{error_list_str} not found")
                    exit()
            return value
        case "array":
            new_list = exec_assign_array([], expression[1])
            new_list.reverse()
            return new_list


def p_start(p):
    """start : bloc"""

    p[0] = ("start", p[1])
    exec_bloc(p[1])


def p_bloc(p):
    """bloc : statement SEMICOLON
    | bloc statement SEMICOLON
    | expression SEMICOLON
    | bloc expression SEMICOLON"""

    if len(p) == 3:
        p[0] = ("bloc", p[1], "empty")
    else:
        p[0] = ("bloc", p[1], p[2])


def p_error(p):
    print(f"Syntax error at line {p.lineno} : {p.value}")


### Utils


def p_statement_exit(p):
    "statement : EXIT"

    print("Bye")
    exit()


def p_statement_print(p):
    "statement : PRINT LPAREN arguments RPAREN"

    p[0] = ("print", p[3])


def p_statement_comment(p):
    "statement : COMMENT"
    pass


### Conditions


def p_if_statement(p):
    """statement : IF expression THEN bloc ENDIF
    | IF expression THEN bloc ELSE bloc ENDIF"""

    if len(p) == 6:
        p[0] = ("if", p[2], p[4], "empty")
    else:
        p[0] = ("if", p[2], p[4], p[6])


### Loops


def p_statement_while(p):
    "statement : WHILE expression DO bloc ENDWHILE"

    p[0] = ("while", p[2], p[4])


def p_statement_for(p):
    "statement : FOR statement SEMICOLON expression SEMICOLON statement DO bloc ENDFOR"

    p[0] = ("for", p[2], p[4], p[6], p[8])


### Functions


def p_statement_parameters(p):
    """parameters : parameters COMMA NAME
    | NAME"""

    if len(p) == 2:
        p[0] = ("parameters", p[1], "empty")
    else:
        p[0] = ("parameters", p[3], p[1])


def p_statement_call_arguments(p):
    """arguments : arguments COMMA expression
    | arguments COMMA STRING
    | STRING
    | expression"""

    if len(p) == 2:
        p[0] = ("arguments", p[1], "empty")
    else:
        p[0] = ("arguments", p[3], p[1])


def p_statement_function(p):
    """statement : FUNCTION NAME LPAREN parameters RPAREN bloc ENDFUNCTION
    | FUNCTION NAME LPAREN RPAREN bloc ENDFUNCTION"""

    if len(p) == 7:
        p[0] = ("function", p[2], "empty", p[5])
    else:
        p[0] = ("function", p[2], p[4], p[6])


def p_statement_call(p):
    """expression : NAME LPAREN arguments RPAREN
    | NAME LPAREN RPAREN"""

    if len(p) == 4:
        p[0] = ("call", p[1], "empty")
    else:
        p[0] = ("call", p[1], p[3])


def p_statement_return(p):
    "statement : RETURN expression"

    p[0] = ("return", p[2])


### Assignments


def p_multiple_assign(p):
    """statement : parameters EQUALS arguments"""

    p[0] = ("multiple_assign", p[1], p[3])


def p_statement_increment(p):
    """statement : NAME PLUSPLUS
    | NAME MINUSMINUS"""

    p[0] = ("increment", p[1], (p[2], p[1]))


def p_statement_assign(p):
    "statement : NAME EQUALS expression"

    p[0] = ("assign", p[1], p[3])


def p_statement_global_exists(p):
    "statement : GLOBAL NAME"

    p[0] = ("global_exist", p[2])


def p_statement_global(p):
    "statement : GLOBAL NAME EQUALS expression"

    p[0] = ("global_new", p[2], p[4])


def p_statement_array(p):
    """statement : NAME EQUALS LEFT_ARRAY arguments RIGHT_ARRAY
    | NAME EQUALS LEFT_ARRAY RIGHT_ARRAY
    """

    if isinstance(p[4], tuple):
        p[0] = ("array", p[1], p[4])
    else:
        p[0] = ("array", p[1], "empty")


def p_statement_array_assign(p):
    "statement : NAME LEFT_ARRAY expression RIGHT_ARRAY EQUALS expression"

    p[0] = ("array_assign", p[1], p[3], p[6])


def p_statement_fast_assign(p):
    """statement : NAME PLUSEQUALS expression
    | NAME MINUSEQUALS expression
    | NAME TIMESEQUALS expression
    | NAME DIVIDEEQUALS expression"""

    p[0] = ("fast_assign", p[1], (p[2], p[1], p[3]))


### Expressions


def p_expression_array(p):
    "expression : LEFT_ARRAY arguments RIGHT_ARRAY"

    p[0] = ("array", p[2], "empty")


def p_expression_array_index(p):
    """index : LEFT_ARRAY arguments RIGHT_ARRAY index
    | LEFT_ARRAY arguments RIGHT_ARRAY"""

    if len(p) == 5:
        p[0] = ("index", p[2], p[4])
    else:
        p[0] = ("index", p[2], "empty")


def p_expression_array_get(p):
    "expression : NAME index"

    p[0] = ("array_get", p[1], p[2])


def p_expression_calc(p):
    """expression : expression PLUS expression
    | expression TIMES expression
    | expression MINUS expression
    | expression DIVIDE expression
    | expression AND expression
    | expression OR expression
    | expression GREATER expression
    | expression LESSER expression
    | expression EQUALSEQUALS expression
    | expression GREATEREQUALS expression
    | expression LESSEREQUALS expression
    """

    p[0] = (p[2], p[1], p[3])


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

from pathlib import Path

try:
    a = yacc.parse(Path("main.brash").read_text())  # type: ignore
except Exception:
    pass
# a = yacc.parse("if 1<2 then a=5;b=0; endif;")  # type: ignore
# print(variables)
# a = yacc.parse("while b<a do b++;print(1); endwhile;")  # type: ignore
# print(variables)
# a = yacc.parse("for a=0; a<10; a++ do print(a); endfor;")  # type: ignore
# print(variables)
