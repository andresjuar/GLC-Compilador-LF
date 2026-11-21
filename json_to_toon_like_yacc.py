import sys
import ply.yacc as yacc

# Se importan los tokens (y el lexer) definidos en el archivo de lex
from json_to_toon_lex import tokens, lexer, leer_archivo

# ---------------------------------------------------------------
# YACC: GLC del JSON de videojuegos -> formato plano tipo TOON
# ---------------------------------------------------------------

start = 'archivo'   # símbolo inicial

def p_archivo_1(p):
    '''archivo : LBRACKET registros RBRACKET'''
    # 1. archivo -> LBRACKET registros RBRACKET
    p[0] = ('{' +  'game_id, title, description, release_date, '
            'developer_info{studio, country}, genres[], platforms[], '
            'game_modes[], supported_languages[], age_rating, critic_score'
             + '}:' + '\n' + p[2] + '\n')

#Esta regla es para archivos vacíos [], este caso nunca entraría en la tarea porque es mínimo 20 registros, pero para completar las reglas
def p_archivo_2(p):
    '''archivo : LBRACKET RBRACKET'''
    # 2. archivo -> LBRACKET RBRACKET   (arreglo vacío: solo encabezado)
    p[0] =  ('{' + 'game_id, title, description, release_date, '
            'developer_info{studio, country}, genres[], platforms[], '
            'game_modes[], supported_languages[], age_rating, critic_score'
           + '}' + '\n') 


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
    p[0] = '  ' + p[2] + ', ' + p[3]


# ------------------------- game_id -------------------------

def p_game_id(p):
    '''game_id : K_GAME_ID COLON valor'''
    # 6. game_id -> K_GAME_ID COLON valor
    p[0] = p[3]


# ------------------------- title -------------------------

def p_title(p):
    '''title : K_TITLE COLON valor'''
    # 7. title -> K_TITLE COLON valor
    p[0] = p[3]


def p_resto_title_1(p):
    '''resto_title : COMMA title resto_description'''
    # 8. resto_title -> COMMA title resto_description
    p[0] = p[2] + ', ' + p[3]


def p_resto_title_2(p):
    '''resto_title : resto_description'''
    # 9. resto_title -> resto_description   (falta title)
    p[0] = '' + ', ' + p[1]


# ------------------------- description -------------------------

def p_description(p):
    '''description : K_DESCRIPTION COLON valor'''
    # 10. description -> K_DESCRIPTION COLON valor
    p[0] = p[3]


def p_resto_description_1(p):
    '''resto_description : COMMA description resto_release_date'''
    # 11. resto_description -> COMMA description resto_release_date
    p[0] = p[2] + ', ' + p[3]


def p_resto_description_2(p):
    '''resto_description : resto_release_date'''
    # 12. resto_description -> resto_release_date   (falta description)
    p[0] = '' + ', ' + p[1]


# ------------------------- release_date -------------------------

def p_release_date(p):
    '''release_date : K_RELEASE_DATE COLON valor'''
    # 13. release_date -> K_RELEASE_DATE COLON valor
    p[0] = p[3]


def p_resto_release_date_1(p):
    '''resto_release_date : COMMA release_date resto_developer_info'''
    # 14. resto_release_date -> COMMA release_date resto_developer_info
    p[0] = p[2] + ', ' + p[3]


def p_resto_release_date_2(p):
    '''resto_release_date : resto_developer_info'''
    # 15. resto_release_date -> resto_developer_info   (falta release_date)
    p[0] = '' + ', ' + p[1]


# ------------------------- developer_info -------------------------

def p_developer_info(p):
    '''developer_info : K_DEVELOPER_INFO COLON objeto_dev'''
    # 16. developer_info -> K_DEVELOPER_INFO COLON objeto_dev
    p[0] = p[3]


def p_resto_developer_info_1(p):
    '''resto_developer_info : COMMA developer_info resto_genres'''
    # 17. resto_developer_info -> COMMA developer_info resto_genres
    p[0] = p[2] + ', ' + p[3]


def p_resto_developer_info_2(p):
    '''resto_developer_info : resto_genres'''
    # 18. resto_developer_info -> resto_genres   (falta developer_info)
    p[0] = '{, }' + ', ' + p[1]


# ------------------------- genres -------------------------

def p_genres(p):
    '''genres : K_GENRES COLON lista'''
    # 19. genres -> K_GENRES COLON lista
    p[0] = p[3]


def p_resto_genres_1(p):
    '''resto_genres : COMMA genres resto_platforms'''
    # 20. resto_genres -> COMMA genres resto_platforms
    p[0] = p[2] + ', ' + p[3]


def p_resto_genres_2(p):
    '''resto_genres : resto_platforms'''
    # 21. resto_genres -> resto_platforms   (falta genres)
    p[0] = '[]' + ', ' + p[1]


# ------------------------- platforms -------------------------

def p_platforms(p):
    '''platforms : K_PLATFORMS COLON lista'''
    # 22. platforms -> K_PLATFORMS COLON lista
    p[0] = p[3]


def p_resto_platforms_1(p):
    '''resto_platforms : COMMA platforms resto_game_modes'''
    # 23. resto_platforms -> COMMA platforms resto_game_modes
    p[0] = p[2] + ', ' + p[3]


def p_resto_platforms_2(p):
    '''resto_platforms : resto_game_modes'''
    # 24. resto_platforms -> resto_game_modes   (falta platforms)
    p[0] = '[]' + ', ' + p[1]


# ------------------------- game_modes -------------------------

def p_game_modes(p):
    '''game_modes : K_GAME_MODES COLON lista'''
    # 25. game_modes -> K_GAME_MODES COLON lista
    p[0] = p[3]


def p_resto_game_modes_1(p):
    '''resto_game_modes : COMMA game_modes resto_supported_languages'''
    # 26. resto_game_modes -> COMMA game_modes resto_supported_languages
    p[0] = p[2] + ', ' + p[3]


def p_resto_game_modes_2(p):
    '''resto_game_modes : resto_supported_languages'''
    # 27. resto_game_modes -> resto_supported_languages   (falta game_modes)
    p[0] = '[]' + ', ' + p[1]


# ------------------------- supported_languages -------------------------

def p_supported_languages(p):
    '''supported_languages : K_SUPPORTED_LANGUAGES COLON lista'''
    # 28. supported_languages -> K_SUPPORTED_LANGUAGES COLON lista
    p[0] = p[3]


def p_resto_supported_languages_1(p):
    '''resto_supported_languages : COMMA supported_languages resto_age_rating'''
    # 29. resto_supported_languages -> COMMA supported_languages resto_age_rating
    p[0] = p[2] + ', ' + p[3]


def p_resto_supported_languages_2(p):
    '''resto_supported_languages : resto_age_rating'''
    # 30. resto_supported_languages -> resto_age_rating   (falta supported_languages)
    p[0] = '[]' + ', ' + p[1]


# ------------------------- age_rating -------------------------

def p_age_rating(p):
    '''age_rating : K_AGE_RATING COLON valor'''
    # 31. age_rating -> K_AGE_RATING COLON valor
    p[0] = p[3]


def p_resto_age_rating_1(p):
    '''resto_age_rating : COMMA age_rating resto_critic_score'''
    # 32. resto_age_rating -> COMMA age_rating resto_critic_score
    p[0] = p[2] + ', ' + p[3]


def p_resto_age_rating_2(p):
    '''resto_age_rating : resto_critic_score'''
    # 33. resto_age_rating -> resto_critic_score   (falta age_rating)
    p[0] = '' + ', ' + p[1]


# ------------------------- critic_score -------------------------

def p_critic_score(p):
    '''critic_score : K_CRITIC_SCORE COLON valor'''
    # 34. critic_score -> K_CRITIC_SCORE COLON valor
    p[0] = p[3]


def p_resto_critic_score_1(p):
    '''resto_critic_score : COMMA critic_score'''
    # 35. resto_critic_score -> COMMA critic_score
    p[0] = p[2]


def p_resto_critic_score_2(p):
    '''resto_critic_score : '''
    # 36. resto_critic_score -> ε   (falta critic_score)
    p[0] = ''


# ------------------- objeto anidado developer_info -------------------

def p_objeto_dev_1(p):
    '''objeto_dev : LBRACE desde_studio RBRACE'''
    # 37. objeto_dev -> LBRACE desde_studio RBRACE
    p[0] = '{' + p[2] + '}'


def p_objeto_dev_2(p):
    '''objeto_dev : NULL'''
    # 38. objeto_dev -> NULL
    p[0] = '{, }'


def p_desde_studio_1(p):
    '''desde_studio : studio resto_country'''
    # 39. desde_studio -> studio resto_country
    p[0] = p[1] + ', ' + p[2]


def p_desde_studio_2(p):
    '''desde_studio : desde_country'''
    # 40. desde_studio -> desde_country   (falta studio)
    p[0] = '' + ', ' + p[1]


def p_desde_country_1(p):
    '''desde_country : country'''
    # 41. desde_country -> country
    p[0] = p[1]


def p_desde_country_2(p):
    '''desde_country : '''
    # 42. desde_country -> ε   (falta country)
    p[0] = ''


def p_resto_country_1(p):
    '''resto_country : COMMA country'''
    # 43. resto_country -> COMMA country
    p[0] = p[2]


def p_resto_country_2(p):
    '''resto_country : '''
    # 44. resto_country -> ε   (falta country)
    p[0] = ''


def p_studio(p):
    '''studio : K_STUDIO COLON valor'''
    # 45. studio -> K_STUDIO COLON valor
    p[0] = p[3]


def p_country(p):
    '''country : K_COUNTRY COLON valor'''
    # 46. country -> K_COUNTRY COLON valor
    p[0] = p[3]


# ------------------------- listas -------------------------

def p_lista_1(p):
    '''lista : LBRACKET elementos RBRACKET'''
    # 47. lista -> LBRACKET elementos RBRACKET
    p[0] = '[' + p[2] + ']'


def p_lista_2(p):
    '''lista : LBRACKET RBRACKET'''
    # 48. lista -> LBRACKET RBRACKET   (arreglo vacío)
    p[0] = '[]'


def p_lista_3(p):
    '''lista : NULL'''
    # 49. lista -> NULL
    p[0] = '[]'


def p_elementos_1(p):
    '''elementos : elementos COMMA valor'''
    # 50. elementos -> elementos COMMA valor
    p[0] = p[1] + ', ' + p[3]


def p_elementos_2(p):
    '''elementos : valor'''
    # 51. elementos -> valor
    p[0] = p[1]


# ------------------------- valores -------------------------

def p_valor_1(p):
    '''valor : STRING'''
    # 52. valor -> STRING
    # Si el texto trae coma (el delimitador de TOON) se pone entre comillas
    if ',' in p[1]:
        p[0] = '"' + p[1] + '"'
    else:
        p[0] = p[1]


def p_valor_2(p):
    '''valor : NUMBER'''
    # 53. valor -> NUMBER
    p[0] = p[1]


def p_valor_3(p):
    '''valor : NULL'''
    # 54. valor -> NULL   (se deja el espacio vacío)
    p[0] = ''


def p_error(p):
    parser.errores += 1
    if p:
        print(f"  Error de sintaxis: token inesperado {p.type} ({p.value!r}) en la línea {p.lineno}")
    else:
        print("  Error de sintaxis: fin de archivo inesperado")


parser = yacc.yacc()
parser.errores = 0
parser.ultimo_id = '?'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        texto = leer_archivo(sys.argv[1])
        salida = 'salida_toon.txt'

        resultado = parser.parse(texto, lexer=lexer)

        if lexer.errores or parser.errores or resultado is None:
            print(f"\nEl archivo NO es válido: {lexer.errores} error(es) léxico(s), "
                  f"{parser.errores} error(es) de sintaxis. No se generó la salida.")
        else:
            #Agregamos el registros encontrados porque esto se acerca mas a lo que es un formato toon
            registros_encontrados = resultado.count(chr(10)) - 1
            with open(salida, 'w', encoding='utf-8') as f:
                f.write(f'juegos[{registros_encontrados}]' + resultado)

            #print(resultado)
            # renglones TOON = renglones del resultado menos el encabezado
            print(f"Registros TOON escritos: {registros_encontrados} -> {salida}")
    else:
        print("Falta archivo de entrada")
