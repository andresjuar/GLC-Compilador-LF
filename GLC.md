# GLC del JSON de videojuegos (versión 1, antes de FNC)

Cada regla concatena su parte de la salida en `p[0]`:

```
juegos[484]{game_id,title,description,release_date,developer_info.studio,developer_info.country,genres,platforms,game_modes,supported_languages,age_rating,critic_score}:
  SV-2016-001,Stardew Valley,"Juego de granja, simulacion y rol.",2016-02-26,ConcernedApe,Estados Unidos,Simulacion;RPG;Indie,...,E10+,89
```

- Los campos van en un orden fijo. `game_id` es obligatorio porque es la llave del registro; cualquier otro campo puede faltar, y en ese caso la regla `resto_X → resto_Y` escribe `null` en su lugar.
- `resto_X` = los campos desde X hasta `critic_score`, donde cada campo presente va precedido de `COMMA`.
- Una tabla TOON solo admite valores simples. Por eso el objeto anidado se aplana en `developer_info.studio` y `developer_info.country`, y cada lista se escribe como un solo valor con sus elementos separados por `;`.
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
| 1  | archivo → LBRACKET registros RBRACKET | 'juegos[' + N + ']{…}:' + '\n' + p[2] + '\n' |
| 2  | archivo → LBRACKET RBRACKET | 'juegos[0]:' + '\n' |
| 3  | registros → registros COMMA registro | p[1] + '\n' + p[3] |
| 4  | registros → registro | p[1] |
| 5  | registro → LBRACE game_id resto_title RBRACE | '  ' + p[2] + ',' + p[3] |
| 6  | game_id → K_GAME_ID COLON valor | p[3] |
| 7  | title → K_TITLE COLON valor | p[3] |
| 8  | resto_title → COMMA title resto_description | p[2] + ',' + p[3] |
| 9  | resto_title → resto_description | 'null' + ',' + p[1] |
| 10 | description → K_DESCRIPTION COLON valor | p[3] |
| 11 | resto_description → COMMA description resto_release_date | p[2] + ',' + p[3] |
| 12 | resto_description → resto_release_date | 'null' + ',' + p[1] |
| 13 | release_date → K_RELEASE_DATE COLON valor | p[3] |
| 14 | resto_release_date → COMMA release_date resto_developer_info | p[2] + ',' + p[3] |
| 15 | resto_release_date → resto_developer_info | 'null' + ',' + p[1] |
| 16 | developer_info → K_DEVELOPER_INFO COLON objeto_dev | p[3] |
| 17 | resto_developer_info → COMMA developer_info resto_genres | p[2] + ',' + p[3] |
| 18 | resto_developer_info → resto_genres | 'null,null' + ',' + p[1] |
| 19 | genres → K_GENRES COLON lista | p[3] |
| 20 | resto_genres → COMMA genres resto_platforms | p[2] + ',' + p[3] |
| 21 | resto_genres → resto_platforms | 'null' + ',' + p[1] |
| 22 | platforms → K_PLATFORMS COLON lista | p[3] |
| 23 | resto_platforms → COMMA platforms resto_game_modes | p[2] + ',' + p[3] |
| 24 | resto_platforms → resto_game_modes | 'null' + ',' + p[1] |
| 25 | game_modes → K_GAME_MODES COLON lista | p[3] |
| 26 | resto_game_modes → COMMA game_modes resto_supported_languages | p[2] + ',' + p[3] |
| 27 | resto_game_modes → resto_supported_languages | 'null' + ',' + p[1] |
| 28 | supported_languages → K_SUPPORTED_LANGUAGES COLON lista | p[3] |
| 29 | resto_supported_languages → COMMA supported_languages resto_age_rating | p[2] + ',' + p[3] |
| 30 | resto_supported_languages → resto_age_rating | 'null' + ',' + p[1] |
| 31 | age_rating → K_AGE_RATING COLON valor | p[3] |
| 32 | resto_age_rating → COMMA age_rating resto_critic_score | p[2] + ',' + p[3] |
| 33 | resto_age_rating → resto_critic_score | 'null' + ',' + p[1] |
| 34 | critic_score → K_CRITIC_SCORE COLON valor | p[3] |
| 35 | resto_critic_score → COMMA critic_score | p[2] |
| 36 | resto_critic_score → ε | 'null' |
| 37 | objeto_dev → LBRACE desde_studio RBRACE | p[2] |
| 38 | objeto_dev → NULL | 'null,null' |
| 39 | desde_studio → studio resto_country | p[1] + ',' + p[2] |
| 40 | desde_studio → desde_country | 'null' + ',' + p[1] |
| 41 | desde_country → country | p[1] |
| 42 | desde_country → ε | 'null' |
| 43 | resto_country → COMMA country | p[2] |
| 44 | resto_country → ε | 'null' |
| 45 | studio → K_STUDIO COLON valor | p[3] |
| 46 | country → K_COUNTRY COLON valor | p[3] |
| 47 | lista → LBRACKET elementos RBRACKET | a_toon(p[2]) |
| 48 | lista → LBRACKET RBRACKET | '""' |
| 49 | lista → NULL | 'null' |
| 50 | elementos → elementos COMMA elemento | p[1] + ';' + p[3] |
| 51 | elementos → elemento | p[1] |
| 52 | elemento → STRING | p[1] |
| 53 | elemento → NUMBER | p[1] |
| 54 | elemento → NULL | 'null' |
| 55 | valor → STRING | a_toon(p[1]) |
| 56 | valor → NUMBER | p[1] |
| 57 | valor → NULL | 'null' |

Ejemplo: si un registro no trae `age_rating`, se usa la regla 33 y en esa columna queda `null`:
`  CH-2017-005,Cuphead,…,Espanol;Ingles,null,86`.

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
