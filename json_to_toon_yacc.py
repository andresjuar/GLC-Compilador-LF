import sys
import ply.yacc as yacc

# Se importan los tokens (y el lexer) definidos en el archivo de lex
from json_to_toon_lex import tokens, lexer, leer_archivo

# ---------------------------------------------------------------
# YACC: GLC del JSON de videojuegos -> formato TOON completo
#
# Salida:
#   juegos[484]:
#     - game_id: SV-2016-001
#       title: Stardew Valley
#       ...
#       developer_info:
#         studio: ConcernedApe
#         country: Estados Unidos
#       genres[3]: Simulacion,RPG,Indie
#       ...
#       critic_score: 89
#     - game_id: HK-2017-002
#       ...
#
# Reglas de TOON que se siguen:
#  - Arreglo raíz  juegos[N]:  y cada registro es un elemento "- " de la lista
#    (2 espacios). El primer campo va en la línea del guion y los demás
#    debajo con 4 espacios; los campos del objeto anidado con 6 espacios.
#  - Cada campo se escribe  llave: valor
#  - Listas en una línea:  llave[N]: a,b,c   (vacía: llave[0]:)
#  - Campo que falta o null -> llave: null.  Si falta developer_info, se
#    escribe el bloque con studio y country en null para conservar su espacio.
#  - Se ponen comillas cuando el texto podría confundirse (ver a_toon).
# ---------------------------------------------------------------

start = 'archivo'   # símbolo inicial


def a_toon(texto):
    """Esta función es para hacer escribir el texto como un valor de toon:
    ya sea que lo deja igual o lo pone entre comillas si TOON lo leería mal
    (vacío, con coma o dos puntos, que parezca número, true/false/null, que empiece con '-' o con espacios).
    No podemos hacer que todo texto esté entre comillas porque esto solo agrega caracteres cuando no siempre
    se necesita y le quita el proósito por el que el formato toon está hecho"""
    sin_signo = texto[1:] if texto.startswith('-') else texto
    parece_numero = sin_signo.replace('.', '', 1).isdigit()
    if (texto == ''
            or ',' in texto or ':' in texto
            or texto in ('true', 'false', 'null')
            or parece_numero
            or texto.startswith('-')
            or texto != texto.strip()):
        return '"' + texto + '"'
    return texto


def contar_elementos(texto):
    """Cuenta los elementos de una lista ya escrita como a,b,"c, d".
    Las comas que están dentro de comillas no separan elementos."""
    n, dentro = 1, False
    for c in texto:
        if c == '"':
            dentro = not dentro
        elif c == ',' and not dentro:
            n += 1
    return n


# ------------------------- Estructura -------------------------

def p_archivo_1(p):
    '''archivo : LBRACKET registros RBRACKET'''
    # 1. archivo -> LBRACKET registros RBRACKET
    # N = número de elementos "  - " que trae p[2] (uno por registro)
    p[0] = 'juegos[' + str(p[2].count('\n  - ') + 1) + ']:' + '\n' + p[2] + '\n'


# Esta regla es para archivos vacíos [], este caso nunca entraría en la
# tarea porque es mínimo 20 registros, pero para completar las reglas
def p_archivo_2(p):
    '''archivo : LBRACKET RBRACKET'''
    # 2. archivo -> LBRACKET RBRACKET   (en TOON un arreglo vacío es  nombre[0]:)
    p[0] = 'juegos[0]:' + '\n'


def p_registros_1(p):
    '''registros : registros COMMA registro'''
    # 3. registros -> registros COMMA registro
    p[0] = p[1] + '\n' + p[3]


def p_registros_2(p):
    '''registros : registro'''
    # 4. registros -> registro
    p[0] = p[1]


def p_registro(p):
    '''registro : LBRACE game_id resto_title RBRACE'''
    # 5. registro -> LBRACE game_id resto_title RBRACE
    # El primer campo va en la misma línea que el guion del elemento
    p[0] = '  - ' + p[2] + p[3]


# ------------------------- game_id -------------------------

def p_game_id(p):
    '''game_id : K_GAME_ID COLON valor'''
    # 6. game_id -> K_GAME_ID COLON valor
    p[0] = 'game_id: ' + p[3]


# ------------------------- title -------------------------

def p_title(p):
    '''title : K_TITLE COLON valor'''
    # 7. title -> K_TITLE COLON valor
    p[0] = 'title: ' + p[3]


def p_resto_title_1(p):
    '''resto_title : COMMA title resto_description'''
    # 8. resto_title -> COMMA title resto_description
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_title_2(p):
    '''resto_title : resto_description'''
    # 9. resto_title -> resto_description   (falta title)
    p[0] = '\n    title: null' + p[1]


# ------------------------- description -------------------------

def p_description(p):
    '''description : K_DESCRIPTION COLON valor'''
    # 10. description -> K_DESCRIPTION COLON valor
    p[0] = 'description: ' + p[3]


def p_resto_description_1(p):
    '''resto_description : COMMA description resto_release_date'''
    # 11. resto_description -> COMMA description resto_release_date
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_description_2(p):
    '''resto_description : resto_release_date'''
    # 12. resto_description -> resto_release_date   (falta description)
    p[0] = '\n    description: null' + p[1]


# ------------------------- release_date -------------------------

def p_release_date(p):
    '''release_date : K_RELEASE_DATE COLON valor'''
    # 13. release_date -> K_RELEASE_DATE COLON valor
    p[0] = 'release_date: ' + p[3]


def p_resto_release_date_1(p):
    '''resto_release_date : COMMA release_date resto_developer_info'''
    # 14. resto_release_date -> COMMA release_date resto_developer_info
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_release_date_2(p):
    '''resto_release_date : resto_developer_info'''
    # 15. resto_release_date -> resto_developer_info   (falta release_date)
    p[0] = '\n    release_date: null' + p[1]


# ------------------------- developer_info -------------------------

def p_developer_info(p):
    '''developer_info : K_DEVELOPER_INFO COLON objeto_dev'''
    # 16. developer_info -> K_DEVELOPER_INFO COLON objeto_dev
    p[0] = 'developer_info:' + p[3]


def p_resto_developer_info_1(p):
    '''resto_developer_info : COMMA developer_info resto_genres'''
    # 17. resto_developer_info -> COMMA developer_info resto_genres
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_developer_info_2(p):
    '''resto_developer_info : resto_genres'''
    # 18. resto_developer_info -> resto_genres   (falta developer_info:
    #     se escribe el bloque con sus dos campos en null)
    p[0] = ('\n    developer_info:'
            + '\n      studio: null'
            + '\n      country: null'
            + p[1])


# ------------------------- genres -------------------------

def p_genres(p):
    '''genres : K_GENRES COLON lista'''
    # 19. genres -> K_GENRES COLON lista
    p[0] = 'genres' + p[3]


def p_resto_genres_1(p):
    '''resto_genres : COMMA genres resto_platforms'''
    # 20. resto_genres -> COMMA genres resto_platforms
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_genres_2(p):
    '''resto_genres : resto_platforms'''
    # 21. resto_genres -> resto_platforms   (falta genres)
    p[0] = '\n    genres: null' + p[1]


# ------------------------- platforms -------------------------

def p_platforms(p):
    '''platforms : K_PLATFORMS COLON lista'''
    # 22. platforms -> K_PLATFORMS COLON lista
    p[0] = 'platforms' + p[3]


def p_resto_platforms_1(p):
    '''resto_platforms : COMMA platforms resto_game_modes'''
    # 23. resto_platforms -> COMMA platforms resto_game_modes
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_platforms_2(p):
    '''resto_platforms : resto_game_modes'''
    # 24. resto_platforms -> resto_game_modes   (falta platforms)
    p[0] = '\n    platforms: null' + p[1]


# ------------------------- game_modes -------------------------

def p_game_modes(p):
    '''game_modes : K_GAME_MODES COLON lista'''
    # 25. game_modes -> K_GAME_MODES COLON lista
    p[0] = 'game_modes' + p[3]


def p_resto_game_modes_1(p):
    '''resto_game_modes : COMMA game_modes resto_supported_languages'''
    # 26. resto_game_modes -> COMMA game_modes resto_supported_languages
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_game_modes_2(p):
    '''resto_game_modes : resto_supported_languages'''
    # 27. resto_game_modes -> resto_supported_languages   (falta game_modes)
    p[0] = '\n    game_modes: null' + p[1]


# ------------------------- supported_languages -------------------------

def p_supported_languages(p):
    '''supported_languages : K_SUPPORTED_LANGUAGES COLON lista'''
    # 28. supported_languages -> K_SUPPORTED_LANGUAGES COLON lista
    p[0] = 'supported_languages' + p[3]


def p_resto_supported_languages_1(p):
    '''resto_supported_languages : COMMA supported_languages resto_age_rating'''
    # 29. resto_supported_languages -> COMMA supported_languages resto_age_rating
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_supported_languages_2(p):
    '''resto_supported_languages : resto_age_rating'''
    # 30. resto_supported_languages -> resto_age_rating   (falta supported_languages)
    p[0] = '\n    supported_languages: null' + p[1]


# ------------------------- age_rating -------------------------

def p_age_rating(p):
    '''age_rating : K_AGE_RATING COLON valor'''
    # 31. age_rating -> K_AGE_RATING COLON valor
    p[0] = 'age_rating: ' + p[3]


def p_resto_age_rating_1(p):
    '''resto_age_rating : COMMA age_rating resto_critic_score'''
    # 32. resto_age_rating -> COMMA age_rating resto_critic_score
    p[0] = '\n    ' + p[2] + p[3]


def p_resto_age_rating_2(p):
    '''resto_age_rating : resto_critic_score'''
    # 33. resto_age_rating -> resto_critic_score   (falta age_rating)
    p[0] = '\n    age_rating: null' + p[1]


# ------------------------- critic_score -------------------------

def p_critic_score(p):
    '''critic_score : K_CRITIC_SCORE COLON valor'''
    # 34. critic_score -> K_CRITIC_SCORE COLON valor
    p[0] = 'critic_score: ' + p[3]


def p_resto_critic_score_1(p):
    '''resto_critic_score : COMMA critic_score'''
    # 35. resto_critic_score -> COMMA critic_score
    p[0] = '\n    ' + p[2]


def p_resto_critic_score_2(p):
    '''resto_critic_score : '''
    # 36. resto_critic_score -> ε   (falta critic_score)
    p[0] = '\n    critic_score: null'


# ------------------- objeto anidado developer_info -------------------
# Sus campos van debajo de "developer_info:" con 6 espacios

def p_objeto_dev_1(p):
    '''objeto_dev : LBRACE desde_studio RBRACE'''
    # 37. objeto_dev -> LBRACE desde_studio RBRACE
    p[0] = p[2]


def p_objeto_dev_2(p):
    '''objeto_dev : NULL'''
    # 38. objeto_dev -> NULL
    p[0] = '\n      studio: null' + '\n      country: null'


def p_desde_studio_1(p):
    '''desde_studio : studio resto_country'''
    # 39. desde_studio -> studio resto_country
    p[0] = '\n      ' + p[1] + p[2]


def p_desde_studio_2(p):
    '''desde_studio : desde_country'''
    # 40. desde_studio -> desde_country   (falta studio)
    p[0] = '\n      studio: null' + p[1]


def p_desde_country_1(p):
    '''desde_country : country'''
    # 41. desde_country -> country
    p[0] = '\n      ' + p[1]


def p_desde_country_2(p):
    '''desde_country : '''
    # 42. desde_country -> ε   (falta country)
    p[0] = '\n      country: null'


def p_resto_country_1(p):
    '''resto_country : COMMA country'''
    # 43. resto_country -> COMMA country
    p[0] = '\n      ' + p[2]


def p_resto_country_2(p):
    '''resto_country : '''
    # 44. resto_country -> ε   (falta country)
    p[0] = '\n      country: null'


def p_studio(p):
    '''studio : K_STUDIO COLON valor'''
    # 45. studio -> K_STUDIO COLON valor
    p[0] = 'studio: ' + p[3]


def p_country(p):
    '''country : K_COUNTRY COLON valor'''
    # 46. country -> K_COUNTRY COLON valor
    p[0] = 'country: ' + p[3]


# ------------------------- listas -------------------------
# Lista en una línea:  [N]: a,b,c   (la llave la pone la regla del campo)

def p_lista_1(p):
    '''lista : LBRACKET elementos RBRACKET'''
    # 47. lista -> LBRACKET elementos RBRACKET
    p[0] = '[' + str(contar_elementos(p[2])) + ']: ' + p[2]


def p_lista_2(p):
    '''lista : LBRACKET RBRACKET'''
    # 48. lista -> LBRACKET RBRACKET   (arreglo vacío)
    p[0] = '[0]:'


def p_lista_3(p):
    '''lista : NULL'''
    # 49. lista -> NULL
    p[0] = ': null'


def p_elementos_1(p):
    '''elementos : elementos COMMA elemento'''
    # 50. elementos -> elementos COMMA elemento
    p[0] = p[1] + ',' + p[3]


def p_elementos_2(p):
    '''elementos : elemento'''
    # 51. elementos -> elemento
    p[0] = p[1]


def p_elemento_1(p):
    '''elemento : STRING'''
    # 52. elemento -> STRING   (entre comillas solo si TOON lo necesita)
    p[0] = a_toon(p[1])


def p_elemento_2(p):
    '''elemento : NUMBER'''
    # 53. elemento -> NUMBER
    p[0] = p[1]


def p_elemento_3(p):
    '''elemento : NULL'''
    # 54. elemento -> NULL
    p[0] = 'null'


# ------------------------- valores -------------------------

def p_valor_1(p):
    '''valor : STRING'''
    # 55. valor -> STRING   (entre comillas solo si TOON lo necesita)
    p[0] = a_toon(p[1])


def p_valor_2(p):
    '''valor : NUMBER'''
    # 56. valor -> NUMBER
    p[0] = p[1]


def p_valor_3(p):
    '''valor : NULL'''
    # 57. valor -> NULL
    p[0] = 'null'


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
        texto = leer_archivo(sys.argv[1])
        salida = sys.argv[2] if len(sys.argv) > 2 else 'salida_toon.toon'

        resultado = parser.parse(texto, lexer=lexer)

        if lexer.errores or parser.errores or resultado is None:
            print(f"\nEl archivo NO es válido: {lexer.errores} error(es) léxico(s), "
                  f"{parser.errores} error(es) de sintaxis. No se generó la salida.")
        else:
            with open(salida, 'w', encoding='utf-8') as f:
                f.write(resultado)

            # registros TOON = elementos "  - " de la lista
            print(f"Registros TOON escritos: {resultado.count(chr(10) + '  - ')} -> {salida}")
    else:
        print("Falta archivo de entrada")
