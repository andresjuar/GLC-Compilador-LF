# GLC del JSON de videojuegos (versión 1, antes de FNC)

G = (N, T, P, S)

**N** (no terminales) = { archivo, registros, registro, campos, campo, developer, campos_dev, campo_dev, lista, elementos, valor }

**T** (terminales / tokens) = { LBRACKET, RBRACKET, LBRACE, RBRACE, COLON, COMMA,
K_GAME_ID, K_TITLE, K_DESCRIPTION, K_RELEASE_DATE, K_DEVELOPER_INFO, K_STUDIO, K_COUNTRY,
K_GENRES, K_PLATFORMS, K_GAME_MODES, K_SUPPORTED_LANGUAGES, K_AGE_RATING, K_CRITIC_SCORE,
STRING, NUMBER, NULL }

**S** (símbolo inicial) = archivo

**P** (producciones):

| #  | Producción |
|----|------------|
| 1  | archivo → LBRACKET registros RBRACKET |
| 2  | archivo → LBRACKET RBRACKET |
| 3  | registros → registros COMMA registro |
| 4  | registros → registro |
| 5  | registro → LBRACE campos RBRACE |
| 6  | registro → LBRACE RBRACE |
| 7  | campos → campos COMMA campo |
| 8  | campos → campo |
| 9  | campo → K_GAME_ID COLON valor |
| 10 | campo → K_TITLE COLON valor |
| 11 | campo → K_DESCRIPTION COLON valor |
| 12 | campo → K_RELEASE_DATE COLON valor |
| 13 | campo → K_AGE_RATING COLON valor |
| 14 | campo → K_CRITIC_SCORE COLON valor |
| 15 | campo → K_DEVELOPER_INFO COLON developer |
| 16 | campo → K_GENRES COLON lista |
| 17 | campo → K_PLATFORMS COLON lista |
| 18 | campo → K_GAME_MODES COLON lista |
| 19 | campo → K_SUPPORTED_LANGUAGES COLON lista |
| 20 | developer → LBRACE campos_dev RBRACE |
| 21 | developer → LBRACE RBRACE |
| 22 | developer → NULL |
| 23 | campos_dev → campos_dev COMMA campo_dev |
| 24 | campos_dev → campo_dev |
| 25 | campo_dev → K_STUDIO COLON valor |
| 26 | campo_dev → K_COUNTRY COLON valor |
| 27 | lista → LBRACKET elementos RBRACKET |
| 28 | lista → LBRACKET RBRACKET |
| 29 | lista → NULL |
| 30 | elementos → elementos COMMA valor |
| 31 | elementos → valor |
| 32 | valor → STRING |
| 33 | valor → NUMBER |
| 34 | valor → NULL |

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

En FNC solo se permiten producciones A → BC o A → a. Esta versión rompe la forma en:

- **Producciones unitarias** (A → B): 4 `registros → registro`, 8 `campos → campo`, 24 `campos_dev → campo_dev`, 31 `elementos → valor`.
- **Lados derechos de 3 símbolos**: 1, 3, 5, 7, 9–20, 23, 25–27, 30.
- **Terminales mezclados con no terminales**: por ejemplo `LBRACKET registros RBRACKET`.
- **Lados derechos de 2 terminales**: 2, 6, 21, 28 (`LBRACE RBRACE`, `LBRACKET RBRACKET`).

Las producciones 22, 29, 32, 33 y 34 (A → a) ya están en FNC. No hay producciones ε.
