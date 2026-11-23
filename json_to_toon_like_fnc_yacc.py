import sys
import ply.yacc as yacc

# Se importan los tokens (y el lexer) definidos en el archivo de lex
from json_to_toon_lex import tokens, lexer, leer_archivo

# ---------------------------------------------------------------
# YACC: GLC en FNC del JSON de videojuegos -> formato tipo TOON
#
# Versión 2: la misma gramática de json_to_toon_like_yacc.py, pasada a
# Forma Normal de Chomsky (ver FNC.md). Toda producción es
#   A -> B C   (dos no terminales)   o   A -> a   (un terminal).
# La salida es idéntica a la de json_to_toon_like_yacc.py.
#
# ---------------------------------------------------------------


start = 'archivo'   # símbolo inicial

# -------------------- Estructura --------------------

def p_archivo_1(p):
    '''archivo : T_LBRACKET A1'''
    # 1. archivo -> T_LBRACKET A1
    p[0] = ('{' + 'game_id, title, description, release_date, '
            'developer_info{studio, country}, genres[], platforms[], '
            'game_modes[], supported_languages[], age_rating, critic_score'
            + '}:' + '\n' + p[2] + '\n')

def p_archivo_2(p):
    '''archivo : T_LBRACKET T_RBRACKET'''
    # 2. archivo -> T_LBRACKET T_RBRACKET   (arreglo vacío)
    p[0] = ('{' + 'game_id, title, description, release_date, '
            'developer_info{studio, country}, genres[], platforms[], '
            'game_modes[], supported_languages[], age_rating, critic_score'
            + '}' + '\n')

def p_A1(p):
    '''A1 : registros T_RBRACKET'''
    # 3. A1 -> registros T_RBRACKET
    p[0] = p[1]

def p_registros_1(p):
    '''registros : registros B1'''
    # 4. registros -> registros B1
    p[0] = p[1] + '\n' + p[2]

def p_registros_2(p):
    '''registros : T_LBRACE R1'''
    # 5. registros -> T_LBRACE R1   (primer registro)
    p[0] = '  ' + p[2]

def p_registros_3(p):
    '''registros : T_LBRACE R3'''
    # 6. registros -> T_LBRACE R3   (primer registro, solo game_id)
    p[0] = '  ' + p[2]

def p_B1(p):
    '''B1 : T_COMMA registro'''
    # 7. B1 -> T_COMMA registro
    p[0] = p[2]

def p_registro_1(p):
    '''registro : T_LBRACE R1'''
    # 8. registro -> T_LBRACE R1
    p[0] = '  ' + p[2]

def p_registro_2(p):
    '''registro : T_LBRACE R3'''
    # 9. registro -> T_LBRACE R3   (solo game_id)
    p[0] = '  ' + p[2]

def p_R1(p):
    '''R1 : game_id R2'''
    # 10. R1 -> game_id R2
    p[0] = p[1] + ', ' + p[2]

def p_R2(p):
    '''R2 : resto_title T_RBRACE'''
    # 11. R2 -> resto_title T_RBRACE
    p[0] = p[1]

def p_R3(p):
    '''R3 : game_id T_RBRACE'''
    # 12. R3 -> game_id T_RBRACE   (faltan todos los campos después de game_id)
    p[0] = p[1] + ', ' + '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''

# -------------------- Campos --------------------

def p_game_id(p):
    '''game_id : T_K_GAME_ID CV'''
    # 13. game_id -> T_K_GAME_ID CV
    p[0] = p[2]

def p_title(p):
    '''title : T_K_TITLE CV'''
    # 14. title -> T_K_TITLE CV
    p[0] = p[2]

def p_description(p):
    '''description : T_K_DESCRIPTION CV'''
    # 15. description -> T_K_DESCRIPTION CV
    p[0] = p[2]

def p_release_date(p):
    '''release_date : T_K_RELEASE_DATE CV'''
    # 16. release_date -> T_K_RELEASE_DATE CV
    p[0] = p[2]

def p_developer_info(p):
    '''developer_info : T_K_DEVELOPER_INFO CO'''
    # 17. developer_info -> T_K_DEVELOPER_INFO CO
    p[0] = p[2]

def p_genres(p):
    '''genres : T_K_GENRES CL'''
    # 18. genres -> T_K_GENRES CL
    p[0] = p[2]

def p_platforms(p):
    '''platforms : T_K_PLATFORMS CL'''
    # 19. platforms -> T_K_PLATFORMS CL
    p[0] = p[2]

def p_game_modes(p):
    '''game_modes : T_K_GAME_MODES CL'''
    # 20. game_modes -> T_K_GAME_MODES CL
    p[0] = p[2]

def p_supported_languages(p):
    '''supported_languages : T_K_SUPPORTED_LANGUAGES CL'''
    # 21. supported_languages -> T_K_SUPPORTED_LANGUAGES CL
    p[0] = p[2]

def p_age_rating(p):
    '''age_rating : T_K_AGE_RATING CV'''
    # 22. age_rating -> T_K_AGE_RATING CV
    p[0] = p[2]

def p_studio(p):
    '''studio : T_K_STUDIO CV'''
    # 23. studio -> T_K_STUDIO CV
    p[0] = p[2]

def p_country(p):
    '''country : T_K_COUNTRY CV'''
    # 24. country -> T_K_COUNTRY CV
    p[0] = p[2]

def p_CV(p):
    '''CV : T_COLON valor'''
    # 25. CV -> T_COLON valor
    p[0] = p[2]

def p_CL(p):
    '''CL : T_COLON lista'''
    # 26. CL -> T_COLON lista
    p[0] = p[2]

def p_CO(p):
    '''CO : T_COLON objeto_dev'''
    # 27. CO -> T_COLON objeto_dev
    p[0] = p[2]

# -------------------- Campo + resto (lo que va después de una coma) --------------------

def p_E_title_1(p):
    '''E_title : title resto_description'''
    # 28. E_title -> title resto_description
    p[0] = p[1] + ', ' + p[2]

def p_E_title_2(p):
    '''E_title : T_K_TITLE CV'''
    # 29. E_title -> T_K_TITLE CV   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''

def p_E_desc_1(p):
    '''E_desc : description resto_release_date'''
    # 30. E_desc -> description resto_release_date
    p[0] = p[1] + ', ' + p[2]

def p_E_desc_2(p):
    '''E_desc : T_K_DESCRIPTION CV'''
    # 31. E_desc -> T_K_DESCRIPTION CV   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''

def p_E_release_1(p):
    '''E_release : release_date resto_developer_info'''
    # 32. E_release -> release_date resto_developer_info
    p[0] = p[1] + ', ' + p[2]

def p_E_release_2(p):
    '''E_release : T_K_RELEASE_DATE CV'''
    # 33. E_release -> T_K_RELEASE_DATE CV   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''

def p_E_dev_1(p):
    '''E_dev : developer_info resto_genres'''
    # 34. E_dev -> developer_info resto_genres
    p[0] = p[1] + ', ' + p[2]

def p_E_dev_2(p):
    '''E_dev : T_K_DEVELOPER_INFO CO'''
    # 35. E_dev -> T_K_DEVELOPER_INFO CO   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''

def p_E_genres_1(p):
    '''E_genres : genres resto_platforms'''
    # 36. E_genres -> genres resto_platforms
    p[0] = p[1] + ', ' + p[2]

def p_E_genres_2(p):
    '''E_genres : T_K_GENRES CL'''
    # 37. E_genres -> T_K_GENRES CL   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''

def p_E_plat_1(p):
    '''E_plat : platforms resto_game_modes'''
    # 38. E_plat -> platforms resto_game_modes
    p[0] = p[1] + ', ' + p[2]

def p_E_plat_2(p):
    '''E_plat : T_K_PLATFORMS CL'''
    # 39. E_plat -> T_K_PLATFORMS CL   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''

def p_E_modes_1(p):
    '''E_modes : game_modes resto_supported_languages'''
    # 40. E_modes -> game_modes resto_supported_languages
    p[0] = p[1] + ', ' + p[2]

def p_E_modes_2(p):
    '''E_modes : T_K_GAME_MODES CL'''
    # 41. E_modes -> T_K_GAME_MODES CL   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '[]' + ', ' + '' + ', ' + ''

def p_E_lang_1(p):
    '''E_lang : supported_languages resto_age_rating'''
    # 42. E_lang -> supported_languages resto_age_rating
    p[0] = p[1] + ', ' + p[2]

def p_E_lang_2(p):
    '''E_lang : T_K_SUPPORTED_LANGUAGES CL'''
    # 43. E_lang -> T_K_SUPPORTED_LANGUAGES CL   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + '' + ', ' + ''

def p_E_age_1(p):
    '''E_age : age_rating resto_critic_score'''
    # 44. E_age -> age_rating resto_critic_score
    p[0] = p[1] + ', ' + p[2]

def p_E_age_2(p):
    '''E_age : T_K_AGE_RATING CV'''
    # 45. E_age -> T_K_AGE_RATING CV   (último campo presente; los siguientes faltan)
    p[0] = p[2] + ', ' + ''

def p_E_critic(p):
    '''E_critic : T_K_CRITIC_SCORE CV'''
    # 46. E_critic -> T_K_CRITIC_SCORE CV   (último campo presente)
    p[0] = p[2]

# -------------------- Cadena resto_* (cada una puede empezar en cualquier campo posterior) --------------------

def p_resto_critic_score_1(p):
    '''resto_critic_score : T_COMMA E_critic'''
    # 47. resto_critic_score -> T_COMMA E_critic
    p[0] = p[2]

def p_resto_age_rating_1(p):
    '''resto_age_rating : T_COMMA E_age'''
    # 48. resto_age_rating -> T_COMMA E_age
    p[0] = p[2]

def p_resto_age_rating_2(p):
    '''resto_age_rating : T_COMMA E_critic'''
    # 49. resto_age_rating -> T_COMMA E_critic   (falta age_rating)
    p[0] = '' + ', ' + p[2]

def p_resto_supported_languages_1(p):
    '''resto_supported_languages : T_COMMA E_lang'''
    # 50. resto_supported_languages -> T_COMMA E_lang
    p[0] = p[2]

def p_resto_supported_languages_2(p):
    '''resto_supported_languages : T_COMMA E_age'''
    # 51. resto_supported_languages -> T_COMMA E_age   (falta supported_languages)
    p[0] = '[]' + ', ' + p[2]

def p_resto_supported_languages_3(p):
    '''resto_supported_languages : T_COMMA E_critic'''
    # 52. resto_supported_languages -> T_COMMA E_critic   (falta supported_languages, age_rating)
    p[0] = '[]' + ', ' + '' + ', ' + p[2]

def p_resto_game_modes_1(p):
    '''resto_game_modes : T_COMMA E_modes'''
    # 53. resto_game_modes -> T_COMMA E_modes
    p[0] = p[2]

def p_resto_game_modes_2(p):
    '''resto_game_modes : T_COMMA E_lang'''
    # 54. resto_game_modes -> T_COMMA E_lang   (falta game_modes)
    p[0] = '[]' + ', ' + p[2]

def p_resto_game_modes_3(p):
    '''resto_game_modes : T_COMMA E_age'''
    # 55. resto_game_modes -> T_COMMA E_age   (falta game_modes, supported_languages)
    p[0] = '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_game_modes_4(p):
    '''resto_game_modes : T_COMMA E_critic'''
    # 56. resto_game_modes -> T_COMMA E_critic   (falta game_modes, supported_languages, age_rating)
    p[0] = '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]

def p_resto_platforms_1(p):
    '''resto_platforms : T_COMMA E_plat'''
    # 57. resto_platforms -> T_COMMA E_plat
    p[0] = p[2]

def p_resto_platforms_2(p):
    '''resto_platforms : T_COMMA E_modes'''
    # 58. resto_platforms -> T_COMMA E_modes   (falta platforms)
    p[0] = '[]' + ', ' + p[2]

def p_resto_platforms_3(p):
    '''resto_platforms : T_COMMA E_lang'''
    # 59. resto_platforms -> T_COMMA E_lang   (falta platforms, game_modes)
    p[0] = '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_platforms_4(p):
    '''resto_platforms : T_COMMA E_age'''
    # 60. resto_platforms -> T_COMMA E_age   (falta platforms, game_modes, supported_languages)
    p[0] = '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_platforms_5(p):
    '''resto_platforms : T_COMMA E_critic'''
    # 61. resto_platforms -> T_COMMA E_critic   (falta platforms, game_modes, supported_languages, age_rating)
    p[0] = '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]

def p_resto_genres_1(p):
    '''resto_genres : T_COMMA E_genres'''
    # 62. resto_genres -> T_COMMA E_genres
    p[0] = p[2]

def p_resto_genres_2(p):
    '''resto_genres : T_COMMA E_plat'''
    # 63. resto_genres -> T_COMMA E_plat   (falta genres)
    p[0] = '[]' + ', ' + p[2]

def p_resto_genres_3(p):
    '''resto_genres : T_COMMA E_modes'''
    # 64. resto_genres -> T_COMMA E_modes   (falta genres, platforms)
    p[0] = '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_genres_4(p):
    '''resto_genres : T_COMMA E_lang'''
    # 65. resto_genres -> T_COMMA E_lang   (falta genres, platforms, game_modes)
    p[0] = '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_genres_5(p):
    '''resto_genres : T_COMMA E_age'''
    # 66. resto_genres -> T_COMMA E_age   (falta genres, platforms, game_modes, supported_languages)
    p[0] = '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_genres_6(p):
    '''resto_genres : T_COMMA E_critic'''
    # 67. resto_genres -> T_COMMA E_critic   (falta genres, platforms, game_modes, supported_languages, age_rating)
    p[0] = '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]

def p_resto_developer_info_1(p):
    '''resto_developer_info : T_COMMA E_dev'''
    # 68. resto_developer_info -> T_COMMA E_dev
    p[0] = p[2]

def p_resto_developer_info_2(p):
    '''resto_developer_info : T_COMMA E_genres'''
    # 69. resto_developer_info -> T_COMMA E_genres   (falta developer_info)
    p[0] = '{, }' + ', ' + p[2]

def p_resto_developer_info_3(p):
    '''resto_developer_info : T_COMMA E_plat'''
    # 70. resto_developer_info -> T_COMMA E_plat   (falta developer_info, genres)
    p[0] = '{, }' + ', ' + '[]' + ', ' + p[2]

def p_resto_developer_info_4(p):
    '''resto_developer_info : T_COMMA E_modes'''
    # 71. resto_developer_info -> T_COMMA E_modes   (falta developer_info, genres, platforms)
    p[0] = '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_developer_info_5(p):
    '''resto_developer_info : T_COMMA E_lang'''
    # 72. resto_developer_info -> T_COMMA E_lang   (falta developer_info, genres, platforms, game_modes)
    p[0] = '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_developer_info_6(p):
    '''resto_developer_info : T_COMMA E_age'''
    # 73. resto_developer_info -> T_COMMA E_age   (falta developer_info, genres, platforms, game_modes, supported_languages)
    p[0] = '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_developer_info_7(p):
    '''resto_developer_info : T_COMMA E_critic'''
    # 74. resto_developer_info -> T_COMMA E_critic   (falta developer_info, genres, platforms, game_modes, supported_languages, age_rating)
    p[0] = '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]

def p_resto_release_date_1(p):
    '''resto_release_date : T_COMMA E_release'''
    # 75. resto_release_date -> T_COMMA E_release
    p[0] = p[2]

def p_resto_release_date_2(p):
    '''resto_release_date : T_COMMA E_dev'''
    # 76. resto_release_date -> T_COMMA E_dev   (falta release_date)
    p[0] = '' + ', ' + p[2]

def p_resto_release_date_3(p):
    '''resto_release_date : T_COMMA E_genres'''
    # 77. resto_release_date -> T_COMMA E_genres   (falta release_date, developer_info)
    p[0] = '' + ', ' + '{, }' + ', ' + p[2]

def p_resto_release_date_4(p):
    '''resto_release_date : T_COMMA E_plat'''
    # 78. resto_release_date -> T_COMMA E_plat   (falta release_date, developer_info, genres)
    p[0] = '' + ', ' + '{, }' + ', ' + '[]' + ', ' + p[2]

def p_resto_release_date_5(p):
    '''resto_release_date : T_COMMA E_modes'''
    # 79. resto_release_date -> T_COMMA E_modes   (falta release_date, developer_info, genres, platforms)
    p[0] = '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_release_date_6(p):
    '''resto_release_date : T_COMMA E_lang'''
    # 80. resto_release_date -> T_COMMA E_lang   (falta release_date, developer_info, genres, platforms, game_modes)
    p[0] = '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_release_date_7(p):
    '''resto_release_date : T_COMMA E_age'''
    # 81. resto_release_date -> T_COMMA E_age   (falta release_date, developer_info, genres, platforms, game_modes, supported_languages)
    p[0] = '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_release_date_8(p):
    '''resto_release_date : T_COMMA E_critic'''
    # 82. resto_release_date -> T_COMMA E_critic   (falta release_date, developer_info, genres, platforms, game_modes, supported_languages, age_rating)
    p[0] = '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]

def p_resto_description_1(p):
    '''resto_description : T_COMMA E_desc'''
    # 83. resto_description -> T_COMMA E_desc
    p[0] = p[2]

def p_resto_description_2(p):
    '''resto_description : T_COMMA E_release'''
    # 84. resto_description -> T_COMMA E_release   (falta description)
    p[0] = '' + ', ' + p[2]

def p_resto_description_3(p):
    '''resto_description : T_COMMA E_dev'''
    # 85. resto_description -> T_COMMA E_dev   (falta description, release_date)
    p[0] = '' + ', ' + '' + ', ' + p[2]

def p_resto_description_4(p):
    '''resto_description : T_COMMA E_genres'''
    # 86. resto_description -> T_COMMA E_genres   (falta description, release_date, developer_info)
    p[0] = '' + ', ' + '' + ', ' + '{, }' + ', ' + p[2]

def p_resto_description_5(p):
    '''resto_description : T_COMMA E_plat'''
    # 87. resto_description -> T_COMMA E_plat   (falta description, release_date, developer_info, genres)
    p[0] = '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + p[2]

def p_resto_description_6(p):
    '''resto_description : T_COMMA E_modes'''
    # 88. resto_description -> T_COMMA E_modes   (falta description, release_date, developer_info, genres, platforms)
    p[0] = '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_description_7(p):
    '''resto_description : T_COMMA E_lang'''
    # 89. resto_description -> T_COMMA E_lang   (falta description, release_date, developer_info, genres, platforms, game_modes)
    p[0] = '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_description_8(p):
    '''resto_description : T_COMMA E_age'''
    # 90. resto_description -> T_COMMA E_age   (falta description, release_date, developer_info, genres, platforms, game_modes, supported_languages)
    p[0] = '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_description_9(p):
    '''resto_description : T_COMMA E_critic'''
    # 91. resto_description -> T_COMMA E_critic   (falta description, release_date, developer_info, genres, platforms, game_modes, supported_languages, age_rating)
    p[0] = '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]

def p_resto_title_1(p):
    '''resto_title : T_COMMA E_title'''
    # 92. resto_title -> T_COMMA E_title
    p[0] = p[2]

def p_resto_title_2(p):
    '''resto_title : T_COMMA E_desc'''
    # 93. resto_title -> T_COMMA E_desc   (falta title)
    p[0] = '' + ', ' + p[2]

def p_resto_title_3(p):
    '''resto_title : T_COMMA E_release'''
    # 94. resto_title -> T_COMMA E_release   (falta title, description)
    p[0] = '' + ', ' + '' + ', ' + p[2]

def p_resto_title_4(p):
    '''resto_title : T_COMMA E_dev'''
    # 95. resto_title -> T_COMMA E_dev   (falta title, description, release_date)
    p[0] = '' + ', ' + '' + ', ' + '' + ', ' + p[2]

def p_resto_title_5(p):
    '''resto_title : T_COMMA E_genres'''
    # 96. resto_title -> T_COMMA E_genres   (falta title, description, release_date, developer_info)
    p[0] = '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + p[2]

def p_resto_title_6(p):
    '''resto_title : T_COMMA E_plat'''
    # 97. resto_title -> T_COMMA E_plat   (falta title, description, release_date, developer_info, genres)
    p[0] = '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + p[2]

def p_resto_title_7(p):
    '''resto_title : T_COMMA E_modes'''
    # 98. resto_title -> T_COMMA E_modes   (falta title, description, release_date, developer_info, genres, platforms)
    p[0] = '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_title_8(p):
    '''resto_title : T_COMMA E_lang'''
    # 99. resto_title -> T_COMMA E_lang   (falta title, description, release_date, developer_info, genres, platforms, game_modes)
    p[0] = '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_title_9(p):
    '''resto_title : T_COMMA E_age'''
    # 100. resto_title -> T_COMMA E_age   (falta title, description, release_date, developer_info, genres, platforms, game_modes, supported_languages)
    p[0] = '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]

def p_resto_title_10(p):
    '''resto_title : T_COMMA E_critic'''
    # 101. resto_title -> T_COMMA E_critic   (falta title, description, release_date, developer_info, genres, platforms, game_modes, supported_languages, age_rating)
    p[0] = '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]

# -------------------- Objeto anidado developer_info --------------------

def p_objeto_dev_1(p):
    '''objeto_dev : T_LBRACE O1'''
    # 102. objeto_dev -> T_LBRACE O1
    p[0] = '{' + p[2] + '}'

def p_objeto_dev_2(p):
    '''objeto_dev : T_LBRACE T_RBRACE'''
    # 103. objeto_dev -> T_LBRACE T_RBRACE   (objeto vacío)
    p[0] = '{, }'

def p_objeto_dev_3(p):
    '''objeto_dev : NULL'''
    # 104. objeto_dev -> NULL
    p[0] = '{, }'

def p_O1(p):
    '''O1 : desde_studio T_RBRACE'''
    # 105. O1 -> desde_studio T_RBRACE
    p[0] = p[1]

def p_desde_studio_1(p):
    '''desde_studio : studio resto_country'''
    # 106. desde_studio -> studio resto_country
    p[0] = p[1] + ', ' + p[2]

def p_desde_studio_2(p):
    '''desde_studio : T_K_STUDIO CV'''
    # 107. desde_studio -> T_K_STUDIO CV   (falta country)
    p[0] = p[2] + ', ' + ''

def p_desde_studio_3(p):
    '''desde_studio : T_K_COUNTRY CV'''
    # 108. desde_studio -> T_K_COUNTRY CV   (falta studio)
    p[0] = '' + ', ' + p[2]

def p_resto_country(p):
    '''resto_country : T_COMMA country'''
    # 109. resto_country -> T_COMMA country
    p[0] = p[2]

# -------------------- Listas y valores --------------------

def p_lista_1(p):
    '''lista : T_LBRACKET L1'''
    # 110. lista -> T_LBRACKET L1
    p[0] = '[' + p[2] + ']'

def p_lista_2(p):
    '''lista : T_LBRACKET T_RBRACKET'''
    # 111. lista -> T_LBRACKET T_RBRACKET   (arreglo vacío)
    p[0] = '[]'

def p_lista_3(p):
    '''lista : NULL'''
    # 112. lista -> NULL
    p[0] = '[]'

def p_L1(p):
    '''L1 : elementos T_RBRACKET'''
    # 113. L1 -> elementos T_RBRACKET
    p[0] = p[1]

def p_elementos_1(p):
    '''elementos : elementos V1'''
    # 114. elementos -> elementos V1
    p[0] = p[1] + ', ' + p[2]

def p_elementos_2(p):
    '''elementos : STRING'''
    # 115. elementos -> STRING
    # Si el texto trae coma (el delimitador) se pone entre comillas
    if ',' in p[1]:
        p[0] = '"' + p[1] + '"'
    else:
        p[0] = p[1]

def p_elementos_3(p):
    '''elementos : NUMBER'''
    # 116. elementos -> NUMBER
    p[0] = p[1]

def p_elementos_4(p):
    '''elementos : NULL'''
    # 117. elementos -> NULL
    p[0] = ''

def p_V1(p):
    '''V1 : T_COMMA valor'''
    # 118. V1 -> T_COMMA valor
    p[0] = p[2]

def p_valor_1(p):
    '''valor : STRING'''
    # 119. valor -> STRING
    # Si el texto trae coma (el delimitador) se pone entre comillas
    if ',' in p[1]:
        p[0] = '"' + p[1] + '"'
    else:
        p[0] = p[1]

def p_valor_2(p):
    '''valor : NUMBER'''
    # 120. valor -> NUMBER
    p[0] = p[1]

def p_valor_3(p):
    '''valor : NULL'''
    # 121. valor -> NULL   (se deja el espacio vacío)
    p[0] = ''

# -------------------- Terminales dentro de reglas de 2 símbolos (A -> a) --------------------

def p_T_LBRACKET(p):
    '''T_LBRACKET : LBRACKET'''
    # 122. T_LBRACKET -> LBRACKET
    p[0] = p[1]

def p_T_RBRACKET(p):
    '''T_RBRACKET : RBRACKET'''
    # 123. T_RBRACKET -> RBRACKET
    p[0] = p[1]

def p_T_LBRACE(p):
    '''T_LBRACE : LBRACE'''
    # 124. T_LBRACE -> LBRACE
    p[0] = p[1]

def p_T_RBRACE(p):
    '''T_RBRACE : RBRACE'''
    # 125. T_RBRACE -> RBRACE
    p[0] = p[1]

def p_T_COLON(p):
    '''T_COLON : COLON'''
    # 126. T_COLON -> COLON
    p[0] = p[1]

def p_T_COMMA(p):
    '''T_COMMA : COMMA'''
    # 127. T_COMMA -> COMMA
    p[0] = p[1]

def p_T_K_GAME_ID(p):
    '''T_K_GAME_ID : K_GAME_ID'''
    # 128. T_K_GAME_ID -> K_GAME_ID
    p[0] = p[1]

def p_T_K_TITLE(p):
    '''T_K_TITLE : K_TITLE'''
    # 129. T_K_TITLE -> K_TITLE
    p[0] = p[1]

def p_T_K_DESCRIPTION(p):
    '''T_K_DESCRIPTION : K_DESCRIPTION'''
    # 130. T_K_DESCRIPTION -> K_DESCRIPTION
    p[0] = p[1]

def p_T_K_RELEASE_DATE(p):
    '''T_K_RELEASE_DATE : K_RELEASE_DATE'''
    # 131. T_K_RELEASE_DATE -> K_RELEASE_DATE
    p[0] = p[1]

def p_T_K_DEVELOPER_INFO(p):
    '''T_K_DEVELOPER_INFO : K_DEVELOPER_INFO'''
    # 132. T_K_DEVELOPER_INFO -> K_DEVELOPER_INFO
    p[0] = p[1]

def p_T_K_STUDIO(p):
    '''T_K_STUDIO : K_STUDIO'''
    # 133. T_K_STUDIO -> K_STUDIO
    p[0] = p[1]

def p_T_K_COUNTRY(p):
    '''T_K_COUNTRY : K_COUNTRY'''
    # 134. T_K_COUNTRY -> K_COUNTRY
    p[0] = p[1]

def p_T_K_GENRES(p):
    '''T_K_GENRES : K_GENRES'''
    # 135. T_K_GENRES -> K_GENRES
    p[0] = p[1]

def p_T_K_PLATFORMS(p):
    '''T_K_PLATFORMS : K_PLATFORMS'''
    # 136. T_K_PLATFORMS -> K_PLATFORMS
    p[0] = p[1]

def p_T_K_GAME_MODES(p):
    '''T_K_GAME_MODES : K_GAME_MODES'''
    # 137. T_K_GAME_MODES -> K_GAME_MODES
    p[0] = p[1]

def p_T_K_SUPPORTED_LANGUAGES(p):
    '''T_K_SUPPORTED_LANGUAGES : K_SUPPORTED_LANGUAGES'''
    # 138. T_K_SUPPORTED_LANGUAGES -> K_SUPPORTED_LANGUAGES
    p[0] = p[1]

def p_T_K_AGE_RATING(p):
    '''T_K_AGE_RATING : K_AGE_RATING'''
    # 139. T_K_AGE_RATING -> K_AGE_RATING
    p[0] = p[1]

def p_T_K_CRITIC_SCORE(p):
    '''T_K_CRITIC_SCORE : K_CRITIC_SCORE'''
    # 140. T_K_CRITIC_SCORE -> K_CRITIC_SCORE
    p[0] = p[1]


def p_error(p):
    parser.errores += 1
    if p:
        print(f"  Error de sintaxis: token inesperado {p.type} ({p.value!r}) en la línea {p.lineno}")
    else:
        print("  Error de sintaxis: fin de archivo inesperado")


parser = yacc.yacc(tabmodule='parsetab_toon_like_fnc', debugfile='parser_toon_like_fnc.out')
parser.errores = 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        texto = leer_archivo(sys.argv[1])
        salida = 'salida_toon_like_fnc.txt'

        resultado = parser.parse(texto, lexer=lexer)

        if lexer.errores or parser.errores or resultado is None:
            print(f"\nEl archivo NO es válido: {lexer.errores} error(es) léxico(s), "
                  f"{parser.errores} error(es) de sintaxis. No se generó la salida.")
        else:
            #Agregamos el número de registros encontrados porque esto se acerca mas a lo que es un formato toon
            registros_encontrados = resultado.count(chr(10)) - 1
            with open(salida, 'w', encoding='utf-8') as f:
                f.write(f'juegos[{registros_encontrados}]' + resultado)

            # renglones TOON = renglones del resultado menos el encabezado
            print(f"Registros TOON escritos: {registros_encontrados} -> {salida}")
    else:
        print("Falta archivo de entrada")
