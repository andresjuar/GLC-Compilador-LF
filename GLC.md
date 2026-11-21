# GLC del JSON de videojuegos (versión 1, antes de FNC)

Cada regla concatena su parte de la salida en `p[0]`, y el resultado es TOON completo:

```
juegos[484]:
  - game_id: SV-2016-001
    title: Stardew Valley
    description: "Juego de granja, simulacion y rol."
    release_date: 2016-02-26
    developer_info:
      studio: ConcernedApe
      country: Estados Unidos
    genres[3]: Simulacion,RPG,Indie
    platforms[4]: PC,Nintendo Switch,PS4,Xbox One
    game_modes[2]: Un jugador,Multijugador en linea
    supported_languages[3]: Espanol,Ingles,Frances
    age_rating: E10+
    critic_score: 89
  - game_id: HK-2017-002
    ...
```

- Cada registro es un elemento `- ` de la lista `juegos[N]:`. El primer campo va en la línea del guion, los demás debajo con 4 espacios y los campos de `developer_info` con 6 espacios.
- Los campos van en un orden fijo. `game_id` es obligatorio porque es la llave del registro; cualquier otro campo puede faltar, y en ese caso la regla `resto_X → resto_Y` escribe `llave: null` en su lugar. Si falta `developer_info`, se escribe su bloque con `studio: null` y `country: null`.
- `resto_X` = los campos desde X hasta `critic_score`, donde cada campo presente va precedido de `COMMA`.
- Las listas van en una línea: `llave[N]: a,b,c` (vacía: `llave[0]:`). `contar_elementos` calcula N.
- `a_toon(texto)` pone comillas solo cuando TOON lo necesita: texto vacío, con `,` o `:`, que parezca número, `true`/`false`/`null`, que empiece con `-` o con espacios.

G = (N, T, P, S)

**N** (no terminales) = { archivo, registros, registro,
game_id, title, description, release_date, developer_info, genres, platforms, game_modes,
supported_languages, age_rating, critic_score,
resto_title, resto_description, resto_release_date, resto_developer_info, resto_genres,
resto_platforms, resto_game_modes, resto_supported_languages, resto_age_rating, resto_critic_score,
objeto_dev, desde_studio, desde_country, resto_country, studio, country,
lista, elementos, elemento, valor }

**T** (terminales / tokens) = { LBRACKET, RBRACKET, LBRACE, RBRACE, COLON, COMMA,
K_GAME_ID, K_TITLE, K_DESCRIPTION, K_RELEASE_DATE, K_DEVELOPER_INFO, K_STUDIO, K_COUNTRY,
K_GENRES, K_PLATFORMS, K_GAME_MODES, K_SUPPORTED_LANGUAGES, K_AGE_RATING, K_CRITIC_SCORE,
STRING, NUMBER, NULL }

**S** (símbolo inicial) = archivo

**P** (producciones). La numeración es la misma que usa PLY en `parser.out`.

| #  | Producción | p[0] |
|----|------------|------|
| 1  | archivo → LBRACKET registros RBRACKET | `'juegos[' + N + ']:' + '\n' + p[2] + '\n'` |
| 2  | archivo → LBRACKET RBRACKET | `'juegos[0]:' + '\n'` |
| 3  | registros → registros COMMA registro | `p[1] + '
' + p[3]` |
| 4  | registros → registro | `p[1]` |
| 5  | registro → LBRACE game_id resto_title RBRACE | `'  - ' + p[2] + p[3]` |
| 6  | game_id → K_GAME_ID COLON valor | `'game_id: ' + p[3]` |
| 7  | title → K_TITLE COLON valor | `'title: ' + p[3]` |
| 8  | resto_title → COMMA title resto_description | `'\n    ' + p[2] + p[3]` |
| 9  | resto_title → resto_description | `'\n    title: null' + p[1]` |
| 10 | description → K_DESCRIPTION COLON valor | `'description: ' + p[3]` |
| 11 | resto_description → COMMA description resto_release_date | `'\n    ' + p[2] + p[3]` |
| 12 | resto_description → resto_release_date | `'\n    description: null' + p[1]` |
| 13 | release_date → K_RELEASE_DATE COLON valor | `'release_date: ' + p[3]` |
| 14 | resto_release_date → COMMA release_date resto_developer_info | `'\n    ' + p[2] + p[3]` |
| 15 | resto_release_date → resto_developer_info | `'\n    release_date: null' + p[1]` |
| 16 | developer_info → K_DEVELOPER_INFO COLON objeto_dev | `'developer_info:' + p[3]` |
| 17 | resto_developer_info → COMMA developer_info resto_genres | `'\n    ' + p[2] + p[3]` |
| 18 | resto_developer_info → resto_genres | `'\n    developer_info:' + '\n      studio: null' + '\n      country: null' + p[1]` |
| 19 | genres → K_GENRES COLON lista | `'genres' + p[3]` |
| 20 | resto_genres → COMMA genres resto_platforms | `'\n    ' + p[2] + p[3]` |
| 21 | resto_genres → resto_platforms | `'\n    genres: null' + p[1]` |
| 22 | platforms → K_PLATFORMS COLON lista | `'platforms' + p[3]` |
| 23 | resto_platforms → COMMA platforms resto_game_modes | `'\n    ' + p[2] + p[3]` |
| 24 | resto_platforms → resto_game_modes | `'\n    platforms: null' + p[1]` |
| 25 | game_modes → K_GAME_MODES COLON lista | `'game_modes' + p[3]` |
| 26 | resto_game_modes → COMMA game_modes resto_supported_languages | `'\n    ' + p[2] + p[3]` |
| 27 | resto_game_modes → resto_supported_languages | `'\n    game_modes: null' + p[1]` |
| 28 | supported_languages → K_SUPPORTED_LANGUAGES COLON lista | `'supported_languages' + p[3]` |
| 29 | resto_supported_languages → COMMA supported_languages resto_age_rating | `'\n    ' + p[2] + p[3]` |
| 30 | resto_supported_languages → resto_age_rating | `'\n    supported_languages: null' + p[1]` |
| 31 | age_rating → K_AGE_RATING COLON valor | `'age_rating: ' + p[3]` |
| 32 | resto_age_rating → COMMA age_rating resto_critic_score | `'\n    ' + p[2] + p[3]` |
| 33 | resto_age_rating → resto_critic_score | `'\n    age_rating: null' + p[1]` |
| 34 | critic_score → K_CRITIC_SCORE COLON valor | `'critic_score: ' + p[3]` |
| 35 | resto_critic_score → COMMA critic_score | `'\n    ' + p[2]` |
| 36 | resto_critic_score → ε | `'\n    critic_score: null'` |
| 37 | objeto_dev → LBRACE desde_studio RBRACE | `p[2]` |
| 38 | objeto_dev → NULL | `'\n      studio: null' + '\n      country: null'` |
| 39 | desde_studio → studio resto_country | `'\n      ' + p[1] + p[2]` |
| 40 | desde_studio → desde_country | `'\n      studio: null' + p[1]` |
| 41 | desde_country → country | `'\n      ' + p[1]` |
| 42 | desde_country → ε | `'\n      country: null'` |
| 43 | resto_country → COMMA country | `'\n      ' + p[2]` |
| 44 | resto_country → ε | `'\n      country: null'` |
| 45 | studio → K_STUDIO COLON valor | `'studio: ' + p[3]` |
| 46 | country → K_COUNTRY COLON valor | `'country: ' + p[3]` |
| 47 | lista → LBRACKET elementos RBRACKET | `'[' + contar_elementos(p[2]) + ']: ' + p[2]` |
| 48 | lista → LBRACKET RBRACKET | `'[0]:'` |
| 49 | lista → NULL | `': null'` |
| 50 | elementos → elementos COMMA elemento | `p[1] + ',' + p[3]` |
| 51 | elementos → elemento | `p[1]` |
| 52 | elemento → STRING | `a_toon(p[1])` |
| 53 | elemento → NUMBER | `p[1]` |
| 54 | elemento → NULL | `'null'` |
| 55 | valor → STRING | `a_toon(p[1])` |
| 56 | valor → NUMBER | `p[1]` |
| 57 | valor → NULL | `'null'` |

Ejemplo: si un registro no trae `age_rating`, se usa la regla 33 y se escribe `age_rating: null`:

```
  - game_id: CH-2017-005
    ...
    supported_languages[2]: Espanol,Ingles
    age_rating: null
    critic_score: 86
```

## ER de los terminales

| Token | ER |
|-------|----|
| LBRACKET | `\[` |
| RBRACKET | `\]` |
| LBRACE | `\{` |
| RBRACE | `\}` |
| COLON | `:` |
| COMMA | `,` |
| K_GAME_ID | `"game_id"` |
| K_TITLE | `"title"` |
| K_DESCRIPTION | `"description"` |
| K_RELEASE_DATE | `"release_date"` |
| K_DEVELOPER_INFO | `"developer_info"` |
| K_STUDIO | `"studio"` |
| K_COUNTRY | `"country"` |
| K_GENRES | `"genres"` |
| K_PLATFORMS | `"platforms"` |
| K_GAME_MODES | `"game_modes"` |
| K_SUPPORTED_LANGUAGES | `"supported_languages"` |
| K_AGE_RATING | `"age_rating"` |
| K_CRITIC_SCORE | `"critic_score"` |
| STRING | `"[a-zA-Z0-9áéíóúÁÉÍÓÚÑñüÜ \.,;:#_/+!?&'-]*"` |
| NUMBER | `-?[0-9]+(\.[0-9]+)?` |
| NULL | `null` |

## Por qué todavía no está en FNC

En FNC solo se permiten producciones A → BC o A → a (y S → ε si el lenguaje la acepta). Esta versión rompe la forma en:

- **Producciones ε**: 36, 42, 44.
- **Producciones unitarias** (A → B): 4, 9, 12, 15, 18, 21, 24, 27, 30, 33, 40, 41, 51.
- **Lados derechos de 3 o 4 símbolos**: 1, 3, 5, 6–8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34, 37, 45–47, 50.
- **Terminales mezclados con no terminales**: por ejemplo `COMMA critic_score` (35, 43) o `LBRACE desde_studio RBRACE`.
- **Lados derechos de 2 terminales**: 2, 48 (`LBRACKET RBRACKET`).

Ya están en FNC: 38, 39, 49, 52–57.
