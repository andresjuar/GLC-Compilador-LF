import sys
import ply.yacc as yacc

# Se importan los tokens (y el lexer) definidos en el archivo de lex
from html_ex1_lex_ER import tokens, lexer

start = 'html'   # símbolo inicial

def p_html(p):
    '''html : HTML_S content HTML_E'''
    # 1. html -> t_HTML_S content t_HTML_E
    p[0] = p[1] + p[2] + p[3] 
    #se concatenan todos los elementos de la regla

#codificar todas las reglas de la GLC del HTML ejemplo1 visto en clase

def p_content(p):
    '''content : header body'''
    # 2. content -> header body
    p[0] = p[1] + p[2]


def p_header(p):
    '''header : HEAD_S title HEAD_E'''
    # 3. header -> t_HEAD_S title t_HEAD_E
    p[0] = p[1] + p[2] + p[3]


def p_title(p):
    '''title : TITLE_S text TITLE_E'''
    # 4. title -> t_TITLE_S text t_TITLE_E
    p[0] = p[2] 


def p_body(p):
    '''body : BODY_S h1 paragraphs BODY_E'''
    # 5. body -> t_BODY_S h1 paragraphs t_BODY_E
    p[0] = p[1] + p[2] + p[3] + p[4]


def p_h1(p):
    '''h1 : H1_S text H1_E'''
    # 6. h1 -> t_H1_S text t_H1_E
    p[0] = p[1] + p[2] + p[3]


def p_paragraphs(p):
    '''paragraphs : paragraphs paragraph
                  | '''
    # 7. paragraphs -> paragraphs paragraph | ε
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ''


def p_paragraph(p):
    '''paragraph : P_S text P_E'''
    # 8. paragraph -> t_P_S text t_P_E
    p[0] = p[1] + p[2] + p[3]


def p_text_1(p):
    '''text : TEXT'''
    # 9. text -> t_TEXT
    p[0] = p[1]


def p_text_2(p):
    '''text : '''
    # 10. text → ε
    p[0] = ''


def p_error(p):
    parser.errores += 1
    if p:
        print(f"  Error de sintaxis: token inesperado {p.type} ({p.value!r}) en la línea {p.lineno}")
    else:
        print("  Error de sintaxis: fin de archivo inesperado")


parser = yacc.yacc()
parser.errores = 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as f:
            ejemplo = f.read()
        f.close()
        print(ejemplo)
        result = parser.parse(ejemplo)
        print("Información de retorno: ", result)
    else:
        print(f"Falta archivo de ENTRADA")
