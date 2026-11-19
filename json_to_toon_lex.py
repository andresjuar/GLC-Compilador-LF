import sys
import ply.lex as lex

# ---------------------------------------------------------------
# LEXER: JSON de catálogo de videojuegos -> tokens
# ---------------------------------------------------------------

# Lista de tokens (terminales de la GLC)
tokens = (
    # Símbolos estructurales del JSON
    'LBRACKET', 'RBRACKET',     # [ ]
    'LBRACE', 'RBRACE',         # { }
    'COLON', 'COMMA',           # : ,
    # Llaves (keys) específicas del formato
    'K_GAME_ID',
    'K_TITLE',
    'K_DESCRIPTION',
    'K_RELEASE_DATE',
    'K_DEVELOPER_INFO',
    'K_STUDIO',
    'K_COUNTRY',
    'K_GENRES',
    'K_PLATFORMS',
    'K_GAME_MODES',
    'K_SUPPORTED_LANGUAGES',
    'K_AGE_RATING',
    'K_CRITIC_SCORE',
    # Valores
    'STRING',
    'NUMBER',
    'NULL',
)

# ER de los símbolos estructurales
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_COLON    = r':'
t_COMMA    = r','

# ER de las llaves.
# Se definen como funciones ANTES de STRING porque PLY prueba las
# funciones en el orden en que aparecen; así "title" se reconoce
# como K_TITLE y no como un STRING cualquiera.
# t.value se queda con el nombre de la llave sin comillas.

def t_K_GAME_ID(t):
    r'"game_id"'
    t.value = 'game_id'
    return t

def t_K_TITLE(t):
    r'"title"'
    t.value = 'title'
    return t

def t_K_DESCRIPTION(t):
    r'"description"'
    t.value = 'description'
    return t

def t_K_RELEASE_DATE(t):
    r'"release_date"'
    t.value = 'release_date'
    return t

def t_K_DEVELOPER_INFO(t):
    r'"developer_info"'
    t.value = 'developer_info'
    return t

def t_K_STUDIO(t):
    r'"studio"'
    t.value = 'studio'
    return t

def t_K_COUNTRY(t):
    r'"country"'
    t.value = 'country'
    return t

def t_K_GENRES(t):
    r'"genres"'
    t.value = 'genres'
    return t

def t_K_PLATFORMS(t):
    r'"platforms"'
    t.value = 'platforms'
    return t

def t_K_GAME_MODES(t):
    r'"game_modes"'
    t.value = 'game_modes'
    return t

def t_K_SUPPORTED_LANGUAGES(t):
    r'"supported_languages"'
    t.value = 'supported_languages'
    return t

def t_K_AGE_RATING(t):
    r'"age_rating"'
    t.value = 'age_rating'
    return t

def t_K_CRITIC_SCORE(t):
    r'"critic_score"'
    t.value = 'critic_score'
    return t

# ER de una cadena: comillas, cero o más caracteres permitidos, comillas.
# Con * (estrella de Kleene) se acepta la cadena vacía "".
# No incluye la comilla " dentro, así que la cadena termina en la
# siguiente comilla. Se quitan las comillas del valor.
def t_STRING(t):
    r'"[a-zA-Z0-9áéíóúÁÉÍÓÚÑñüÜ \.,;:#_/+!?&\'-]*"'
    t.value = t.value[1:-1]
    return t

# ER de un número: signo opcional, uno o más dígitos y
# opcionalmente un punto seguido de uno o más dígitos.
#   NUMBER = (-|ε) [0-9]+ ( \.[0-9]+ | ε )
t_NUMBER = r'-?[0-9]+(\.[0-9]+)?'

# ER del valor nulo
t_NULL = r'null'

# Blancos entre tokens: se ignoran (no son token).
t_ignore = ' \t\r'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)   # solo cuenta líneas, no genera token


def t_error(t):
    print(f"Error léxico: carácter no válido {t.value[0]!r} en la línea {t.lexer.lineno}")
    t.lexer.errores += 1
    t.lexer.skip(1)


lexer = lex.lex()
lexer.errores = 0


def leer_archivo(ruta):
    """Lee el archivo de entrada como texto plano (sin librería json).
    La separación en campos la hace el lexer con las ER."""
    with open(ruta, encoding='utf-8') as f:
        contenido = f.read()
    return contenido


if __name__ == '__main__':
    if len(sys.argv) > 1:
        texto = leer_archivo(sys.argv[1])
        print(texto)
        lexer.input(texto)

        conteo = {}
        print(f"{'LÍNEA':>5}  {'POS':>5}  {'TOKEN':<22} VALOR")
        print('-' * 66)
        for tok in lexer:
            # LexToken(tipo, valor, línea, posición)
            print(f"{tok.lineno:>5}  {tok.lexpos:>5}  {tok.type:<22} {tok.value!r}")
            conteo[tok.type] = conteo.get(tok.type, 0) + 1

        print('-' * 66)
        print("Resumen de tokens:")
        for tipo in tokens:
            print(f"  {tipo:<22} {conteo.get(tipo, 0)}")
        print(f"Errores léxicos: {lexer.errores}")
    else:
        print("Falta archivo para VALIDACIÓN")
