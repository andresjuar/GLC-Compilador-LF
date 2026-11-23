# GLC del JSON de videojuegos (versión 1, antes de FNC)


La gramática acepta json con este formato:

```
  [{
    "game_id": "SV-2016-001",
    "title": "Stardew Valley",
    "description": "Juego de granja, simulacion y rol.",
    "release_date": "2016-02-26",
    "developer_info": {
      "studio": "ConcernedApe",
      "country": "Estados Unidos"
    },
    "genres": ["Simulacion", "RPG", "Indie"],
    "platforms": ["PC", "Nintendo Switch", "PS4", "Xbox One"],
    "game_modes": ["Un jugador", "Multijugador en linea"],
    "supported_languages": ["Espanol", "Ingles", "Frances"],
    "age_rating": "E10+",
    "critic_score": 89
  }]
```

Para esto, hicimos dos versiones, uno que tiene una salida "toon-like" que es como lo pide la actividad del proyecto, con una línea por registro

eso se puede ver en el archivo `json_to_toon_like_yacc.py`

```
juegos[1]{game_id,title,description,release_date,developer_info.studio,developer_info.country,genres,platforms,game_modes,supported_languages,age_rating,critic_score}:
  SV-2016-001,Stardew Valley,"Juego de granja, simulacion y rol.",2016-02-26,ConcernedApe,Estados Unidos,Simulacion;RPG;Indie,PC;Nintendo Switch;PS4;Xbox One,Un jugador;Multijugador en linea,Espanol;Ingles;Frances,E10+,89
```

También desarrollamos la versión que utiliza las reglas oficiales de toon, el resultado de ese mismo json es este:

esto está en el archivo `json_to_toon_yacc.py`

```
juegos[1]:
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
```

Ambas versiones utilizan las mismas reglas de la GLC, esa GLC se define de la siguiente manera:

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

**P** (Reglas de Producción) también se muestra como se mapea en el parser

| #  | Producción | p[0] |
|----|------------|------|
| 1  | archivo → LBRACKET registros RBRACKET | `'juegos[' + N + ']:' + '\n' + p[2] + '\n'` |
| 2  | archivo → LBRACKET RBRACKET | `'juegos[0]:' + '\n'` |
| 3  | registros → registros COMMA registro | `p[1] + '' + p[3]` |
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

Corregimos lo de la revisión y ambos archivos generan el resultado desde las reglas. Además, el archivo que genera el archivo .toon tiene dos funciones auxiliares que sirven para formatear el string:

La primer función es que se ponen comillas cuando el texto podría confundirse (ver a_toon).
```
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
```

Y la segunda es para contar elementos cuando no es tan facil como para contar el número de comas:
```
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
```

Aún queda por hacer la implementación de las reglas pasadas a la Forma Normal de Chomsky
