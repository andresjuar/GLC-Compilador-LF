# GLC del JSON de videojuegos (versión 2, en FNC)
 
Esta es la gramática de `GLC.md` convertida a Forma Normal de Chomsky.
Toda producción es `A → B C` (dos no terminales) o `A → a` (un terminal).
El símbolo inicial sigue siendo `archivo`. No hay `S → ε` porque el lenguaje no acepta la cadena vacía.

Conversión realizada por Andrés Juárez, Alejandro Fernández e Iker Contla
 
## Pasos de la conversión
 
1. **Eliminar ε**: son anulables `resto_critic_score`, `desde_country`, `resto_country` y, por propagación, toda la cadena `resto_*` y `desde_studio`.
2. **Eliminar unitarias**: cada `resto_X` hereda las producciones de todos los `resto_Y` posteriores.
3. **Elimina los terminales del lado derecho (RHS-Right-Hand Side)**
4. **Elimine RHS con más de dos no terminales.**
Nombres nuevos:
- `E_*` = lo que sigue a una coma: el campo y su resto, o solo el campo.
- `CV`, `CL`, `CO` = `COLON` seguido de `valor`, `lista` u `objeto_dev` (compartidos por todos los campos).
- `A1`, `B1`, `R1`–`R3`, `O1`, `L1`, `V1` = auxiliares para los pasos 3 y 4.
- Desaparecen `critic_score` y `desde_country` por ser símbolos inútiles.

## Producciones
 
```
# ── Estructura general ──
archivo   -> T_LBRACKET A1 | T_LBRACKET T_RBRACKET
A1        -> registros T_RBRACKET
registros -> registros B1 | T_LBRACE R1 | T_LBRACE R3
B1        -> T_COMMA registro
registro  -> T_LBRACE R1 | T_LBRACE R3
R1        -> game_id R2
R2        -> resto_title T_RBRACE
R3        -> game_id T_RBRACE
 
# ── Campos ──
game_id             -> T_K_GAME_ID CV
title               -> T_K_TITLE CV
description         -> T_K_DESCRIPTION CV
release_date        -> T_K_RELEASE_DATE CV
developer_info      -> T_K_DEVELOPER_INFO CO
genres              -> T_K_GENRES CL
platforms           -> T_K_PLATFORMS CL
game_modes          -> T_K_GAME_MODES CL
supported_languages -> T_K_SUPPORTED_LANGUAGES CL
age_rating          -> T_K_AGE_RATING CV
studio              -> T_K_STUDIO CV
country             -> T_K_COUNTRY CV
 
CV -> T_COLON valor
CL -> T_COLON lista
CO -> T_COLON objeto_dev
 
# ── Campo + resto (lo que va después de una coma) ──
E_title   -> title resto_description | T_K_TITLE CV
E_desc    -> description resto_release_date | T_K_DESCRIPTION CV
E_release -> release_date resto_developer_info | T_K_RELEASE_DATE CV
E_dev     -> developer_info resto_genres | T_K_DEVELOPER_INFO CO
E_genres  -> genres resto_platforms | T_K_GENRES CL
E_plat    -> platforms resto_game_modes | T_K_PLATFORMS CL
E_modes   -> game_modes resto_supported_languages | T_K_GAME_MODES CL
E_lang    -> supported_languages resto_age_rating | T_K_SUPPORTED_LANGUAGES CL
E_age     -> age_rating resto_critic_score | T_K_AGE_RATING CV
E_critic  -> T_K_CRITIC_SCORE CV
 
# ── Cadena resto_* (cada una acepta empezar en cualquier campo posterior) ──
resto_critic_score -> T_COMMA E_critic
 
resto_age_rating -> T_COMMA E_age | T_COMMA E_critic
 
resto_supported_languages -> T_COMMA E_lang | T_COMMA E_age | T_COMMA E_critic
 
resto_game_modes -> T_COMMA E_modes | T_COMMA E_lang | T_COMMA E_age
  | T_COMMA E_critic
 
resto_platforms -> T_COMMA E_plat | T_COMMA E_modes | T_COMMA E_lang
  | T_COMMA E_age | T_COMMA E_critic
 
resto_genres -> T_COMMA E_genres | T_COMMA E_plat | T_COMMA E_modes
  | T_COMMA E_lang | T_COMMA E_age | T_COMMA E_critic
 
resto_developer_info -> T_COMMA E_dev | T_COMMA E_genres | T_COMMA E_plat
  | T_COMMA E_modes | T_COMMA E_lang | T_COMMA E_age | T_COMMA E_critic
 
resto_release_date -> T_COMMA E_release | T_COMMA E_dev | T_COMMA E_genres
  | T_COMMA E_plat | T_COMMA E_modes | T_COMMA E_lang
  | T_COMMA E_age | T_COMMA E_critic
 
resto_description -> T_COMMA E_desc | T_COMMA E_release | T_COMMA E_dev
  | T_COMMA E_genres | T_COMMA E_plat | T_COMMA E_modes
  | T_COMMA E_lang | T_COMMA E_age | T_COMMA E_critic
 
resto_title -> T_COMMA E_title | T_COMMA E_desc | T_COMMA E_release
  | T_COMMA E_dev | T_COMMA E_genres | T_COMMA E_plat
  | T_COMMA E_modes | T_COMMA E_lang | T_COMMA E_age
  | T_COMMA E_critic
 
# ── developer_info ──
objeto_dev    -> T_LBRACE O1 | T_LBRACE T_RBRACE | NULL
O1            -> desde_studio T_RBRACE
desde_studio  -> studio resto_country | T_K_STUDIO CV | T_K_COUNTRY CV
resto_country -> T_COMMA country
 
# ── Listas y valores ──
lista     -> T_LBRACKET L1 | T_LBRACKET T_RBRACKET | NULL
L1        -> elementos T_RBRACKET
elementos -> elementos V1 | STRING | NUMBER | NULL
V1        -> T_COMMA valor
valor     -> STRING | NUMBER | NULL
 
# ── Producciones de terminales ──
T_LBRACKET -> LBRACKET
T_RBRACKET -> RBRACKET
T_LBRACE   -> LBRACE
T_RBRACE   -> RBRACE
T_COLON    -> COLON
T_COMMA    -> COMMA
T_K_GAME_ID -> K_GAME_ID
T_K_TITLE -> K_TITLE
T_K_DESCRIPTION -> K_DESCRIPTION
T_K_RELEASE_DATE -> K_RELEASE_DATE
T_K_DEVELOPER_INFO -> K_DEVELOPER_INFO
T_K_STUDIO -> K_STUDIO
T_K_COUNTRY -> K_COUNTRY
T_K_GENRES -> K_GENRES
T_K_PLATFORMS -> K_PLATFORMS
T_K_GAME_MODES -> K_GAME_MODES
T_K_SUPPORTED_LANGUAGES -> K_SUPPORTED_LANGUAGES
T_K_AGE_RATING -> K_AGE_RATING
T_K_CRITIC_SCORE -> K_CRITIC_SCORE
```

## Implementación

| Versión | GLC original | GLC en FNC | Producciones |
|---|---|---|---|
| TOON completo | `json_to_toon_yacc.py` (57) | `json_to_toon_fnc_yacc.py` | 143 |
| Tipo TOON | `json_to_toon_like_yacc.py` (54) | `json_to_toon_like_fnc_yacc.py` | 140 |


## Producciones numeradas: tipo TOON (`json_to_toon_like_fnc_yacc.py`)

| # | Producción | p[0] |
|---|------------|------|
| 1 | archivo → T_LBRACKET A1 | `('{' + 'game_id, title, description, release_date, ' 'developer_info{studio, country}, genres[], platforms[], ' 'game_modes[], supported_languages[], age_rating, critic_score' + '}:' + '\n' + p[2] + '\n')` |
| 2 | archivo → T_LBRACKET T_RBRACKET | `('{' + 'game_id, title, description, release_date, ' 'developer_info{studio, country}, genres[], platforms[], ' 'game_modes[], supported_languages[], age_rating, critic_score' + '}' + '\n')` |
| 3 | A1 → registros T_RBRACKET | `p[1]` |
| 4 | registros → registros B1 | `p[1] + '\n' + p[2]` |
| 5 | registros → T_LBRACE R1 | `'  ' + p[2]` |
| 6 | registros → T_LBRACE R3 | `'  ' + p[2]` |
| 7 | B1 → T_COMMA registro | `p[2]` |
| 8 | registro → T_LBRACE R1 | `'  ' + p[2]` |
| 9 | registro → T_LBRACE R3 | `'  ' + p[2]` |
| 10 | R1 → game_id R2 | `p[1] + ', ' + p[2]` |
| 11 | R2 → resto_title T_RBRACE | `p[1]` |
| 12 | R3 → game_id T_RBRACE | `p[1] + ', ' + '' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 13 | game_id → T_K_GAME_ID CV | `p[2]` |
| 14 | title → T_K_TITLE CV | `p[2]` |
| 15 | description → T_K_DESCRIPTION CV | `p[2]` |
| 16 | release_date → T_K_RELEASE_DATE CV | `p[2]` |
| 17 | developer_info → T_K_DEVELOPER_INFO CO | `p[2]` |
| 18 | genres → T_K_GENRES CL | `p[2]` |
| 19 | platforms → T_K_PLATFORMS CL | `p[2]` |
| 20 | game_modes → T_K_GAME_MODES CL | `p[2]` |
| 21 | supported_languages → T_K_SUPPORTED_LANGUAGES CL | `p[2]` |
| 22 | age_rating → T_K_AGE_RATING CV | `p[2]` |
| 23 | studio → T_K_STUDIO CV | `p[2]` |
| 24 | country → T_K_COUNTRY CV | `p[2]` |
| 25 | CV → T_COLON valor | `p[2]` |
| 26 | CL → T_COLON lista | `p[2]` |
| 27 | CO → T_COLON objeto_dev | `p[2]` |
| 28 | E_title → title resto_description | `p[1] + ', ' + p[2]` |
| 29 | E_title → T_K_TITLE CV | `p[2] + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 30 | E_desc → description resto_release_date | `p[1] + ', ' + p[2]` |
| 31 | E_desc → T_K_DESCRIPTION CV | `p[2] + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 32 | E_release → release_date resto_developer_info | `p[1] + ', ' + p[2]` |
| 33 | E_release → T_K_RELEASE_DATE CV | `p[2] + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 34 | E_dev → developer_info resto_genres | `p[1] + ', ' + p[2]` |
| 35 | E_dev → T_K_DEVELOPER_INFO CO | `p[2] + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 36 | E_genres → genres resto_platforms | `p[1] + ', ' + p[2]` |
| 37 | E_genres → T_K_GENRES CL | `p[2] + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 38 | E_plat → platforms resto_game_modes | `p[1] + ', ' + p[2]` |
| 39 | E_plat → T_K_PLATFORMS CL | `p[2] + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 40 | E_modes → game_modes resto_supported_languages | `p[1] + ', ' + p[2]` |
| 41 | E_modes → T_K_GAME_MODES CL | `p[2] + ', ' + '[]' + ', ' + '' + ', ' + ''` |
| 42 | E_lang → supported_languages resto_age_rating | `p[1] + ', ' + p[2]` |
| 43 | E_lang → T_K_SUPPORTED_LANGUAGES CL | `p[2] + ', ' + '' + ', ' + ''` |
| 44 | E_age → age_rating resto_critic_score | `p[1] + ', ' + p[2]` |
| 45 | E_age → T_K_AGE_RATING CV | `p[2] + ', ' + ''` |
| 46 | E_critic → T_K_CRITIC_SCORE CV | `p[2]` |
| 47 | resto_critic_score → T_COMMA E_critic | `p[2]` |
| 48 | resto_age_rating → T_COMMA E_age | `p[2]` |
| 49 | resto_age_rating → T_COMMA E_critic | `'' + ', ' + p[2]` |
| 50 | resto_supported_languages → T_COMMA E_lang | `p[2]` |
| 51 | resto_supported_languages → T_COMMA E_age | `'[]' + ', ' + p[2]` |
| 52 | resto_supported_languages → T_COMMA E_critic | `'[]' + ', ' + '' + ', ' + p[2]` |
| 53 | resto_game_modes → T_COMMA E_modes | `p[2]` |
| 54 | resto_game_modes → T_COMMA E_lang | `'[]' + ', ' + p[2]` |
| 55 | resto_game_modes → T_COMMA E_age | `'[]' + ', ' + '[]' + ', ' + p[2]` |
| 56 | resto_game_modes → T_COMMA E_critic | `'[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]` |
| 57 | resto_platforms → T_COMMA E_plat | `p[2]` |
| 58 | resto_platforms → T_COMMA E_modes | `'[]' + ', ' + p[2]` |
| 59 | resto_platforms → T_COMMA E_lang | `'[]' + ', ' + '[]' + ', ' + p[2]` |
| 60 | resto_platforms → T_COMMA E_age | `'[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 61 | resto_platforms → T_COMMA E_critic | `'[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]` |
| 62 | resto_genres → T_COMMA E_genres | `p[2]` |
| 63 | resto_genres → T_COMMA E_plat | `'[]' + ', ' + p[2]` |
| 64 | resto_genres → T_COMMA E_modes | `'[]' + ', ' + '[]' + ', ' + p[2]` |
| 65 | resto_genres → T_COMMA E_lang | `'[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 66 | resto_genres → T_COMMA E_age | `'[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 67 | resto_genres → T_COMMA E_critic | `'[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]` |
| 68 | resto_developer_info → T_COMMA E_dev | `p[2]` |
| 69 | resto_developer_info → T_COMMA E_genres | `'{, }' + ', ' + p[2]` |
| 70 | resto_developer_info → T_COMMA E_plat | `'{, }' + ', ' + '[]' + ', ' + p[2]` |
| 71 | resto_developer_info → T_COMMA E_modes | `'{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 72 | resto_developer_info → T_COMMA E_lang | `'{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 73 | resto_developer_info → T_COMMA E_age | `'{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 74 | resto_developer_info → T_COMMA E_critic | `'{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]` |
| 75 | resto_release_date → T_COMMA E_release | `p[2]` |
| 76 | resto_release_date → T_COMMA E_dev | `'' + ', ' + p[2]` |
| 77 | resto_release_date → T_COMMA E_genres | `'' + ', ' + '{, }' + ', ' + p[2]` |
| 78 | resto_release_date → T_COMMA E_plat | `'' + ', ' + '{, }' + ', ' + '[]' + ', ' + p[2]` |
| 79 | resto_release_date → T_COMMA E_modes | `'' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 80 | resto_release_date → T_COMMA E_lang | `'' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 81 | resto_release_date → T_COMMA E_age | `'' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 82 | resto_release_date → T_COMMA E_critic | `'' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]` |
| 83 | resto_description → T_COMMA E_desc | `p[2]` |
| 84 | resto_description → T_COMMA E_release | `'' + ', ' + p[2]` |
| 85 | resto_description → T_COMMA E_dev | `'' + ', ' + '' + ', ' + p[2]` |
| 86 | resto_description → T_COMMA E_genres | `'' + ', ' + '' + ', ' + '{, }' + ', ' + p[2]` |
| 87 | resto_description → T_COMMA E_plat | `'' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + p[2]` |
| 88 | resto_description → T_COMMA E_modes | `'' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 89 | resto_description → T_COMMA E_lang | `'' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 90 | resto_description → T_COMMA E_age | `'' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 91 | resto_description → T_COMMA E_critic | `'' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]` |
| 92 | resto_title → T_COMMA E_title | `p[2]` |
| 93 | resto_title → T_COMMA E_desc | `'' + ', ' + p[2]` |
| 94 | resto_title → T_COMMA E_release | `'' + ', ' + '' + ', ' + p[2]` |
| 95 | resto_title → T_COMMA E_dev | `'' + ', ' + '' + ', ' + '' + ', ' + p[2]` |
| 96 | resto_title → T_COMMA E_genres | `'' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + p[2]` |
| 97 | resto_title → T_COMMA E_plat | `'' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + p[2]` |
| 98 | resto_title → T_COMMA E_modes | `'' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 99 | resto_title → T_COMMA E_lang | `'' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 100 | resto_title → T_COMMA E_age | `'' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + p[2]` |
| 101 | resto_title → T_COMMA E_critic | `'' + ', ' + '' + ', ' + '' + ', ' + '{, }' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '[]' + ', ' + '' + ', ' + p[2]` |
| 102 | objeto_dev → T_LBRACE O1 | `'{' + p[2] + '}'` |
| 103 | objeto_dev → T_LBRACE T_RBRACE | `'{, }'` |
| 104 | objeto_dev → NULL | `'{, }'` |
| 105 | O1 → desde_studio T_RBRACE | `p[1]` |
| 106 | desde_studio → studio resto_country | `p[1] + ', ' + p[2]` |
| 107 | desde_studio → T_K_STUDIO CV | `p[2] + ', ' + ''` |
| 108 | desde_studio → T_K_COUNTRY CV | `'' + ', ' + p[2]` |
| 109 | resto_country → T_COMMA country | `p[2]` |
| 110 | lista → T_LBRACKET L1 | `'[' + p[2] + ']'` |
| 111 | lista → T_LBRACKET T_RBRACKET | `'[]'` |
| 112 | lista → NULL | `'[]'` |
| 113 | L1 → elementos T_RBRACKET | `p[1]` |
| 114 | elementos → elementos V1 | `p[1] + ', ' + p[2]` |
| 115 | elementos → STRING | p[1] (entre comillas si trae coma) |
| 116 | elementos → NUMBER | `p[1]` |
| 117 | elementos → NULL | `''` |
| 118 | V1 → T_COMMA valor | `p[2]` |
| 119 | valor → STRING | p[1] (entre comillas si trae coma) |
| 120 | valor → NUMBER | `p[1]` |
| 121 | valor → NULL | `''` |
| 122 | T_LBRACKET → LBRACKET | `p[1]` |
| 123 | T_RBRACKET → RBRACKET | `p[1]` |
| 124 | T_LBRACE → LBRACE | `p[1]` |
| 125 | T_RBRACE → RBRACE | `p[1]` |
| 126 | T_COLON → COLON | `p[1]` |
| 127 | T_COMMA → COMMA | `p[1]` |
| 128 | T_K_GAME_ID → K_GAME_ID | `p[1]` |
| 129 | T_K_TITLE → K_TITLE | `p[1]` |
| 130 | T_K_DESCRIPTION → K_DESCRIPTION | `p[1]` |
| 131 | T_K_RELEASE_DATE → K_RELEASE_DATE | `p[1]` |
| 132 | T_K_DEVELOPER_INFO → K_DEVELOPER_INFO | `p[1]` |
| 133 | T_K_STUDIO → K_STUDIO | `p[1]` |
| 134 | T_K_COUNTRY → K_COUNTRY | `p[1]` |
| 135 | T_K_GENRES → K_GENRES | `p[1]` |
| 136 | T_K_PLATFORMS → K_PLATFORMS | `p[1]` |
| 137 | T_K_GAME_MODES → K_GAME_MODES | `p[1]` |
| 138 | T_K_SUPPORTED_LANGUAGES → K_SUPPORTED_LANGUAGES | `p[1]` |
| 139 | T_K_AGE_RATING → K_AGE_RATING | `p[1]` |
| 140 | T_K_CRITIC_SCORE → K_CRITIC_SCORE | `p[1]` |

## Producciones numeradas: TOON completo (`json_to_toon_fnc_yacc.py`)

| # | Producción | p[0] |
|---|------------|------|
| 1 | archivo → T_LBRACKET A1 | `'juegos[' + str(p[2].count('\n  - ') + 1) + ']:' + '\n' + p[2] + '\n'` |
| 2 | archivo → T_LBRACKET T_RBRACKET | `'juegos[0]:' + '\n'` |
| 3 | A1 → registros T_RBRACKET | `p[1]` |
| 4 | registros → registros B1 | `p[1] + '\n' + p[2]` |
| 5 | registros → T_LBRACE R1 | `'  - ' + p[2]` |
| 6 | registros → T_LBRACE R3 | `'  - ' + p[2]` |
| 7 | B1 → T_COMMA registro | `p[2]` |
| 8 | registro → T_LBRACE R1 | `'  - ' + p[2]` |
| 9 | registro → T_LBRACE R3 | `'  - ' + p[2]` |
| 10 | R1 → game_id R2 | `p[1] + p[2]` |
| 11 | R2 → resto_title T_RBRACE | `p[1]` |
| 12 | R3 → game_id T_RBRACE | `p[1] + '\n    title: null' + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 13 | game_id → T_K_GAME_ID CV | `'game_id: ' + p[2]` |
| 14 | title → T_K_TITLE CV | `'title: ' + p[2]` |
| 15 | description → T_K_DESCRIPTION CV | `'description: ' + p[2]` |
| 16 | release_date → T_K_RELEASE_DATE CV | `'release_date: ' + p[2]` |
| 17 | developer_info → T_K_DEVELOPER_INFO CO | `'developer_info:' + p[2]` |
| 18 | genres → T_K_GENRES CL | `'genres' + p[2]` |
| 19 | platforms → T_K_PLATFORMS CL | `'platforms' + p[2]` |
| 20 | game_modes → T_K_GAME_MODES CL | `'game_modes' + p[2]` |
| 21 | supported_languages → T_K_SUPPORTED_LANGUAGES CL | `'supported_languages' + p[2]` |
| 22 | age_rating → T_K_AGE_RATING CV | `'age_rating: ' + p[2]` |
| 23 | studio → T_K_STUDIO CV | `'studio: ' + p[2]` |
| 24 | country → T_K_COUNTRY CV | `'country: ' + p[2]` |
| 25 | CV → T_COLON valor | `p[2]` |
| 26 | CL → T_COLON lista | `p[2]` |
| 27 | CO → T_COLON objeto_dev | `p[2]` |
| 28 | E_title → title resto_description | `'\n    ' + p[1] + p[2]` |
| 29 | E_title → T_K_TITLE CV | `'\n    title: ' + p[2] + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 30 | E_desc → description resto_release_date | `'\n    ' + p[1] + p[2]` |
| 31 | E_desc → T_K_DESCRIPTION CV | `'\n    description: ' + p[2] + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 32 | E_release → release_date resto_developer_info | `'\n    ' + p[1] + p[2]` |
| 33 | E_release → T_K_RELEASE_DATE CV | `'\n    release_date: ' + p[2] + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 34 | E_dev → developer_info resto_genres | `'\n    ' + p[1] + p[2]` |
| 35 | E_dev → T_K_DEVELOPER_INFO CO | `'\n    developer_info:' + p[2] + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 36 | E_genres → genres resto_platforms | `'\n    ' + p[1] + p[2]` |
| 37 | E_genres → T_K_GENRES CL | `'\n    genres' + p[2] + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 38 | E_plat → platforms resto_game_modes | `'\n    ' + p[1] + p[2]` |
| 39 | E_plat → T_K_PLATFORMS CL | `'\n    platforms' + p[2] + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 40 | E_modes → game_modes resto_supported_languages | `'\n    ' + p[1] + p[2]` |
| 41 | E_modes → T_K_GAME_MODES CL | `'\n    game_modes' + p[2] + '\n    supported_languages: null' + '\n    age_rating: null' + '\n    critic_score: null'` |
| 42 | E_lang → supported_languages resto_age_rating | `'\n    ' + p[1] + p[2]` |
| 43 | E_lang → T_K_SUPPORTED_LANGUAGES CL | `'\n    supported_languages' + p[2] + '\n    age_rating: null' + '\n    critic_score: null'` |
| 44 | E_age → age_rating resto_critic_score | `'\n    ' + p[1] + p[2]` |
| 45 | E_age → T_K_AGE_RATING CV | `'\n    age_rating: ' + p[2] + '\n    critic_score: null'` |
| 46 | E_critic → T_K_CRITIC_SCORE CV | `'\n    critic_score: ' + p[2]` |
| 47 | resto_critic_score → T_COMMA E_critic | `p[2]` |
| 48 | resto_age_rating → T_COMMA E_age | `p[2]` |
| 49 | resto_age_rating → T_COMMA E_critic | `'\n    age_rating: null' + p[2]` |
| 50 | resto_supported_languages → T_COMMA E_lang | `p[2]` |
| 51 | resto_supported_languages → T_COMMA E_age | `'\n    supported_languages: null' + p[2]` |
| 52 | resto_supported_languages → T_COMMA E_critic | `'\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 53 | resto_game_modes → T_COMMA E_modes | `p[2]` |
| 54 | resto_game_modes → T_COMMA E_lang | `'\n    game_modes: null' + p[2]` |
| 55 | resto_game_modes → T_COMMA E_age | `'\n    game_modes: null' + '\n    supported_languages: null' + p[2]` |
| 56 | resto_game_modes → T_COMMA E_critic | `'\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 57 | resto_platforms → T_COMMA E_plat | `p[2]` |
| 58 | resto_platforms → T_COMMA E_modes | `'\n    platforms: null' + p[2]` |
| 59 | resto_platforms → T_COMMA E_lang | `'\n    platforms: null' + '\n    game_modes: null' + p[2]` |
| 60 | resto_platforms → T_COMMA E_age | `'\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + p[2]` |
| 61 | resto_platforms → T_COMMA E_critic | `'\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 62 | resto_genres → T_COMMA E_genres | `p[2]` |
| 63 | resto_genres → T_COMMA E_plat | `'\n    genres: null' + p[2]` |
| 64 | resto_genres → T_COMMA E_modes | `'\n    genres: null' + '\n    platforms: null' + p[2]` |
| 65 | resto_genres → T_COMMA E_lang | `'\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + p[2]` |
| 66 | resto_genres → T_COMMA E_age | `'\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + p[2]` |
| 67 | resto_genres → T_COMMA E_critic | `'\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 68 | resto_developer_info → T_COMMA E_dev | `p[2]` |
| 69 | resto_developer_info → T_COMMA E_genres | `'\n    developer_info:' + '\n      studio: null' + '\n      country: null' + p[2]` |
| 70 | resto_developer_info → T_COMMA E_plat | `'\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + p[2]` |
| 71 | resto_developer_info → T_COMMA E_modes | `'\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + p[2]` |
| 72 | resto_developer_info → T_COMMA E_lang | `'\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + p[2]` |
| 73 | resto_developer_info → T_COMMA E_age | `'\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + p[2]` |
| 74 | resto_developer_info → T_COMMA E_critic | `'\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 75 | resto_release_date → T_COMMA E_release | `p[2]` |
| 76 | resto_release_date → T_COMMA E_dev | `'\n    release_date: null' + p[2]` |
| 77 | resto_release_date → T_COMMA E_genres | `'\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + p[2]` |
| 78 | resto_release_date → T_COMMA E_plat | `'\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + p[2]` |
| 79 | resto_release_date → T_COMMA E_modes | `'\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + p[2]` |
| 80 | resto_release_date → T_COMMA E_lang | `'\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + p[2]` |
| 81 | resto_release_date → T_COMMA E_age | `'\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + p[2]` |
| 82 | resto_release_date → T_COMMA E_critic | `'\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 83 | resto_description → T_COMMA E_desc | `p[2]` |
| 84 | resto_description → T_COMMA E_release | `'\n    description: null' + p[2]` |
| 85 | resto_description → T_COMMA E_dev | `'\n    description: null' + '\n    release_date: null' + p[2]` |
| 86 | resto_description → T_COMMA E_genres | `'\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + p[2]` |
| 87 | resto_description → T_COMMA E_plat | `'\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + p[2]` |
| 88 | resto_description → T_COMMA E_modes | `'\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + p[2]` |
| 89 | resto_description → T_COMMA E_lang | `'\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + p[2]` |
| 90 | resto_description → T_COMMA E_age | `'\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + p[2]` |
| 91 | resto_description → T_COMMA E_critic | `'\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 92 | resto_title → T_COMMA E_title | `p[2]` |
| 93 | resto_title → T_COMMA E_desc | `'\n    title: null' + p[2]` |
| 94 | resto_title → T_COMMA E_release | `'\n    title: null' + '\n    description: null' + p[2]` |
| 95 | resto_title → T_COMMA E_dev | `'\n    title: null' + '\n    description: null' + '\n    release_date: null' + p[2]` |
| 96 | resto_title → T_COMMA E_genres | `'\n    title: null' + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + p[2]` |
| 97 | resto_title → T_COMMA E_plat | `'\n    title: null' + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + p[2]` |
| 98 | resto_title → T_COMMA E_modes | `'\n    title: null' + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + p[2]` |
| 99 | resto_title → T_COMMA E_lang | `'\n    title: null' + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + p[2]` |
| 100 | resto_title → T_COMMA E_age | `'\n    title: null' + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + p[2]` |
| 101 | resto_title → T_COMMA E_critic | `'\n    title: null' + '\n    description: null' + '\n    release_date: null' + '\n    developer_info:' + '\n      studio: null' + '\n      country: null' + '\n    genres: null' + '\n    platforms: null' + '\n    game_modes: null' + '\n    supported_languages: null' + '\n    age_rating: null' + p[2]` |
| 102 | objeto_dev → T_LBRACE O1 | `p[2]` |
| 103 | objeto_dev → T_LBRACE T_RBRACE | `'\n      studio: null' + '\n      country: null'` |
| 104 | objeto_dev → NULL | `'\n      studio: null' + '\n      country: null'` |
| 105 | O1 → desde_studio T_RBRACE | `p[1]` |
| 106 | desde_studio → studio resto_country | `'\n      ' + p[1] + p[2]` |
| 107 | desde_studio → T_K_STUDIO CV | `'\n      studio: ' + p[2] + '\n      country: null'` |
| 108 | desde_studio → T_K_COUNTRY CV | `'\n      studio: null' + '\n      country: ' + p[2]` |
| 109 | resto_country → T_COMMA country | `'\n      ' + p[2]` |
| 110 | lista → T_LBRACKET L1 | `'[' + str(contar_elementos(p[2])) + ']: ' + p[2]` |
| 111 | lista → T_LBRACKET T_RBRACKET | `'[0]:'` |
| 112 | lista → NULL | `': null'` |
| 113 | L1 → elementos T_RBRACKET | `p[1]` |
| 114 | elementos → elementos V1 | `p[1] + ',' + p[2]` |
| 115 | elementos → STRING | `a_toon(p[1])` |
| 116 | elementos → NUMBER | `p[1]` |
| 117 | elementos → NULL | `'null'` |
| 118 | V1 → T_COMMA elemento | `p[2]` |
| 119 | elemento → STRING | `a_toon(p[1])` |
| 120 | elemento → NUMBER | `p[1]` |
| 121 | elemento → NULL | `'null'` |
| 122 | valor → STRING | `a_toon(p[1])` |
| 123 | valor → NUMBER | `p[1]` |
| 124 | valor → NULL | `'null'` |
| 125 | T_LBRACKET → LBRACKET | `p[1]` |
| 126 | T_RBRACKET → RBRACKET | `p[1]` |
| 127 | T_LBRACE → LBRACE | `p[1]` |
| 128 | T_RBRACE → RBRACE | `p[1]` |
| 129 | T_COLON → COLON | `p[1]` |
| 130 | T_COMMA → COMMA | `p[1]` |
| 131 | T_K_GAME_ID → K_GAME_ID | `p[1]` |
| 132 | T_K_TITLE → K_TITLE | `p[1]` |
| 133 | T_K_DESCRIPTION → K_DESCRIPTION | `p[1]` |
| 134 | T_K_RELEASE_DATE → K_RELEASE_DATE | `p[1]` |
| 135 | T_K_DEVELOPER_INFO → K_DEVELOPER_INFO | `p[1]` |
| 136 | T_K_STUDIO → K_STUDIO | `p[1]` |
| 137 | T_K_COUNTRY → K_COUNTRY | `p[1]` |
| 138 | T_K_GENRES → K_GENRES | `p[1]` |
| 139 | T_K_PLATFORMS → K_PLATFORMS | `p[1]` |
| 140 | T_K_GAME_MODES → K_GAME_MODES | `p[1]` |
| 141 | T_K_SUPPORTED_LANGUAGES → K_SUPPORTED_LANGUAGES | `p[1]` |
| 142 | T_K_AGE_RATING → K_AGE_RATING | `p[1]` |
| 143 | T_K_CRITIC_SCORE → K_CRITIC_SCORE | `p[1]` |
