import sys
import ply.yacc as yacc

# Se importan los tokens (y el lexer) definidos en el archivo de lex
from json_to_toon_lex import tokens, lexer, leer_archivo

# ---------------------------------------------------------------
# YACC: GLC del JSON de videojuegos -> formato plano tipo TOON
#
#
#  1. archivo     -> LBRACKET registros RBRACKET
#  2. archivo     -> LBRACKET RBRACKET
#  3. registros   -> registros COMMA registro
#  4. registros   -> registro
#  5. registro    -> LBRACE campos RBRACE
#  6. registro    -> LBRACE RBRACE
#  7. campos      -> campos COMMA campo
#  8. campos      -> campo
#  9. campo       -> K_GAME_ID COLON valor
# 10. campo       -> K_TITLE COLON valor
# 11. campo       -> K_DESCRIPTION COLON valor
# 12. campo       -> K_RELEASE_DATE COLON valor
# 13. campo       -> K_AGE_RATING COLON valor
# 14. campo       -> K_CRITIC_SCORE COLON valor
# 15. campo       -> K_DEVELOPER_INFO COLON developer
# 16. campo       -> K_GENRES COLON lista
# 17. campo       -> K_PLATFORMS COLON lista
# 18. campo       -> K_GAME_MODES COLON lista
# 19. campo       -> K_SUPPORTED_LANGUAGES COLON lista
# 20. developer   -> LBRACE campos_dev RBRACE
# 21. developer   -> LBRACE RBRACE
# 22. developer   -> NULL
# 23. campos_dev  -> campos_dev COMMA campo_dev
# 24. campos_dev  -> campo_dev
# 25. campo_dev   -> K_STUDIO COLON valor
# 26. campo_dev   -> K_COUNTRY COLON valor
# 27. lista       -> LBRACKET elementos RBRACKET
# 28. lista       -> LBRACKET RBRACKET
# 29. lista       -> NULL
# 30. elementos   -> elementos COMMA valor
# 31. elementos   -> valor
# 32. valor       -> STRING
# 33. valor       -> NUMBER
# 34. valor       -> NULL
# ---------------------------------------------------------------

start = 'archivo'   # símbolo inicial

# Esquema de la salida, en el mismo orden que el JSON.
# 'simple' = valor, 'objeto' = developer_info{studio, country}, 'lista' = arreglo
ESQUEMA = (
    ('game_id', 'simple'),
    ('title', 'simple'),
    ('description', 'simple'),
    ('release_date', 'simple'),
    ('developer_info', 'objeto'),
    ('genres', 'lista'),
    ('platforms', 'lista'),
    ('game_modes', 'lista'),
    ('supported_languages', 'lista'),
    ('age_rating', 'simple'),
    ('critic_score', 'simple'),
)
CAMPOS_DEV = ('studio', 'country')


def encabezado():
    partes = []
    for campo, tipo in ESQUEMA:
        if tipo == 'objeto':
            partes.append(campo + '{' + ', '.join(CAMPOS_DEV) + '}')
        elif tipo == 'lista':
            partes.append(campo + '[]')
        else:
            partes.append(campo)
    return ', '.join(partes)


def p_archivo_1(p):
    '''archivo : LBRACKET registros RBRACKET'''
    # 1. archivo -> LBRACKET registros RBRACKET
    p[0] = p[2]                      # lista de renglones TOON


def p_archivo_2(p):
    '''archivo : LBRACKET RBRACKET'''
    # 2. archivo -> LBRACKET RBRACKET   (arreglo vacío)
    p[0] = []


def p_registros_1(p):
    '''registros : registros COMMA registro'''
    # 3. registros -> registros COMMA registro
    p[0] = p[1] + [p[3]]


def p_registros_2(p):
    '''registros : registro'''
    # 4. registros -> registro
    p[0] = [p[1]]


def p_registro_1(p):
    '''registro : LBRACE campos RBRACE'''
    # 5. registro -> LBRACE campos RBRACE
    p[0] = armar_renglon(p[2], p.lineno(1))


def p_registro_2(p):
    '''registro : LBRACE RBRACE'''
    # 6. registro -> LBRACE RBRACE   (registro sin campos)
    p[0] = armar_renglon([], p.lineno(1))


def p_campos_1(p):
    '''campos : campos COMMA campo'''
    # 7. campos -> campos COMMA campo
    p[0] = p[1] + [p[3]]


def p_campos_2(p):
    '''campos : campo'''
    # 8. campos -> campo
    p[0] = [p[1]]


def p_campo_simple(p):
    '''campo : K_GAME_ID COLON valor
             | K_TITLE COLON valor
             | K_DESCRIPTION COLON valor
             | K_RELEASE_DATE COLON valor
             | K_AGE_RATING COLON valor
             | K_CRITIC_SCORE COLON valor'''
    # 9-14. campo -> K_xxx COLON valor
    # p[1] es el nombre de la llave (lo pone el lexer), p[3] su valor
    p[0] = (p[1], p[3])


def p_campo_developer(p):
    '''campo : K_DEVELOPER_INFO COLON developer'''
    # 15. campo -> K_DEVELOPER_INFO COLON developer
    p[0] = (p[1], p[3])


def p_campo_lista(p):
    '''campo : K_GENRES COLON lista
             | K_PLATFORMS COLON lista
             | K_GAME_MODES COLON lista
             | K_SUPPORTED_LANGUAGES COLON lista'''
    # 16-19. campo -> K_xxx COLON lista
    p[0] = (p[1], p[3])


def p_developer_1(p):
    '''developer : LBRACE campos_dev RBRACE'''
    # 20. developer -> LBRACE campos_dev RBRACE
    p[0] = p[2]


def p_developer_2(p):
    '''developer : LBRACE RBRACE'''
    # 21. developer -> LBRACE RBRACE   (objeto anidado vacío)
    p[0] = []


def p_developer_3(p):
    '''developer : NULL'''
    # 22. developer -> NULL
    p[0] = []


def p_campos_dev_1(p):
    '''campos_dev : campos_dev COMMA campo_dev'''
    # 23. campos_dev -> campos_dev COMMA campo_dev
    p[0] = p[1] + [p[3]]


def p_campos_dev_2(p):
    '''campos_dev : campo_dev'''
    # 24. campos_dev -> campo_dev
    p[0] = [p[1]]


def p_campo_dev(p):
    '''campo_dev : K_STUDIO COLON valor
                 | K_COUNTRY COLON valor'''
    # 25-26. campo_dev -> K_STUDIO COLON valor | K_COUNTRY COLON valor
    p[0] = (p[1], p[3])


def p_lista_1(p):
    '''lista : LBRACKET elementos RBRACKET'''
    # 27. lista -> LBRACKET elementos RBRACKET
    p[0] = p[2]


def p_lista_2(p):
    '''lista : LBRACKET RBRACKET'''
    # 28. lista -> LBRACKET RBRACKET   (arreglo vacío)
    p[0] = []


def p_lista_3(p):
    '''lista : NULL'''
    # 29. lista -> NULL
    p[0] = []


def p_elementos_1(p):
    '''elementos : elementos COMMA valor'''
    # 30. elementos -> elementos COMMA valor
    p[0] = p[1] + [p[3]]


def p_elementos_2(p):
    '''elementos : valor'''
    # 31. elementos -> valor
    p[0] = [p[1]]


def p_valor_1(p):
    '''valor : STRING
             | NUMBER'''
    # 32-33. valor -> STRING | NUMBER
    p[0] = p[1]


def p_valor_2(p):
    '''valor : NULL'''
    # 34. valor -> NULL   (se trata como campo vacío)
    p[0] = ''


def p_error(p):
    parser.errores += 1
    if p:
        print(f"  Error de sintaxis: token inesperado {p.type} ({p.value!r}) en la línea {p.lineno}")
    else:
        print("  Error de sintaxis: fin de archivo inesperado")


# ---------------------------------------------------------------
# Funciones auxiliares (formato de salida y validación)
# ---------------------------------------------------------------

def formato_valor(v):
    """Si el valor contiene el delimitador (coma) se pone entre comillas,
    como hace TOON, para que la salida no sea ambigua."""
    if ',' in v:
        return '"' + v + '"'
    return v


def buscar(pares, llave):
    """Busca una llave en la lista de pares (llave, valor).
    Devuelve None si la llave no existe."""
    for k, v in pares:
        if k == llave:
            return v
    return None


def armar_renglon(pares, linea):
    """Convierte un registro en un renglón TOON. Si una llave no existe o
    está vacía, se deja su espacio vacío en la salida."""
    parser.num_registro += 1
    n = parser.num_registro
    donde = f"Registro {n} (línea {linea})"
    columnas = []

    for campo, tipo in ESQUEMA:
        v = buscar(pares, campo)
        if v is None:
            parser.avisos.append(f"{donde}: falta la llave '{campo}'")

        if tipo == 'simple':
            if v is None:
                v = ''
            elif v == '':
                parser.avisos.append(f"{donde}: '{campo}' está vacío")
            columnas.append(formato_valor(v))

        elif tipo == 'lista':
            if v is None:
                v = []
            elif v == []:
                parser.avisos.append(f"{donde}: '{campo}' es una lista vacía")
            columnas.append('[' + ', '.join(formato_valor(e) for e in v) + ']')

        else:   # objeto developer_info
            if v is None:
                v = []
            sub = []
            for sc in CAMPOS_DEV:
                sv = buscar(v, sc)
                if sv is None:
                    if v:
                        parser.avisos.append(f"{donde}: falta la llave '{campo}.{sc}'")
                    sv = ''
                elif sv == '':
                    parser.avisos.append(f"{donde}: '{campo}.{sc}' está vacío")
                sub.append(formato_valor(sv))
            columnas.append('{' + ', '.join(sub) + '}')

    return ', '.join(columnas)


parser = yacc.yacc()
parser.errores = 0
parser.num_registro = 0
parser.avisos = []

if __name__ == '__main__':
    if len(sys.argv) > 1:
        texto = leer_archivo(sys.argv[1])
        salida = sys.argv[2] if len(sys.argv) > 2 else 'salida_toon.txt'

        renglones = parser.parse(texto, lexer=lexer)

        if lexer.errores or parser.errores or renglones is None:
            print(f"\nEl archivo NO es válido: {lexer.errores} error(es) léxico(s), "
                  f"{parser.errores} error(es) de sintaxis. No se generó la salida.")
        else:
            print("Validación de estructura:")
            for aviso in parser.avisos:
                print("  " + aviso)
            if not parser.avisos:
                print("  Todos los registros están completos.")

            with open(salida, 'w', encoding='utf-8') as f:
                f.write(encabezado() + '\n')
                for r in renglones:
                    f.write(r + '\n')

            print(f"\n{encabezado()}")
            for r in renglones:
                print(r)
            print(f"\nRegistros leídos: {parser.num_registro} | "
                  f"Renglones TOON escritos: {len(renglones)} -> {salida}")
    else:
        print("Falta archivo de ENTRADA")
