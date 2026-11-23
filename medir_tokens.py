import sys
import io
import json
import contextlib
import importlib

import json_to_toon_lex as lx

# ---------------------------------------------------------------
# Mide cuántos tokens de un modelo de lenguaje (LLM) "gasta" la misma
# información escrita en JSON, en TOON y en el formato tipo TOON.
#
# Los tokens se cuentan con tiktoken (el tokenizador de OpenAI, el que
# usan las comparaciones de TOON). Si no está instalado, el script
# muestra caracteres y una estimación de ~4 caracteres por token.
#   Instalarlo:  py -m pip install tiktoken
#
# Las salidas TOON y tipo TOON se generan aquí mismo con los YACC del
# proyecto, así siempre se mide la versión actual.
#
# NOTA: la librería json se usa SOLO en este script de medición, para
# tener como referencia el JSON compacto (sin espacios ni saltos). El
# proyecto (lexer y yacc) no la usa.
#
# Uso:  py medir_tokens.py juegos.json
# ---------------------------------------------------------------

try:
    import tiktoken
    CODIFICACION = tiktoken.get_encoding('o200k_base')   # GPT-4o y posteriores
except ImportError:
    CODIFICACION = None


def contar_tokens_llm(texto):
    if CODIFICACION is None:
        return None
    return len(CODIFICACION.encode(texto))


def generar(modulo, texto, prefijo_juegos=False):
    """Corre el parser de un módulo YACC y devuelve el texto de salida."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        mod = importlib.import_module(modulo)
        lex = lx.lexer.clone()
        lex.errores = 0
        lex.lineno = 1
        mod.parser.errores = 0
        resultado = mod.parser.parse(texto, lexer=lex)
    if prefijo_juegos:
        # json_to_toon_like_yacc.py agrega juegos[N] en su main
        resultado = f'juegos[{resultado.count(chr(10)) - 1}]' + resultado
    return resultado


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Falta archivo de entrada')
        sys.exit(1)

    texto_json = lx.leer_archivo(sys.argv[1])
    formatos = [
        ('JSON (archivo original)', texto_json),
        ('JSON compacto (referencia)', json.dumps(json.loads(texto_json), ensure_ascii=False,
                                                  separators=(',', ':'))),
        ('TOON completo', generar('json_to_toon_yacc', texto_json)),
        ('Tipo TOON', generar('json_to_toon_like_yacc', texto_json, prefijo_juegos=True)),
    ]

    base = contar_tokens_llm(texto_json)
    base_chars = len(texto_json)
    print(f'Archivo: {sys.argv[1]}')
    if CODIFICACION is None:
        print('(tiktoken no está instalado: se muestran caracteres y una estimación '
              'de tokens = caracteres / 4)\n')
        print(f'  {"Formato":<30}{"caracteres":>12}{"~tokens":>10}{"vs JSON":>10}')
        for nombre, t in formatos:
            print(f'  {nombre:<30}{len(t):>12,}{len(t) // 4:>10,}'
                  f'{(len(t) - base_chars) / base_chars * 100:>+9.0f}%')
    else:
        print(f'Tokenizador: tiktoken {CODIFICACION.name}\n')
        print(f'  {"Formato":<30}{"caracteres":>12}{"tokens":>10}{"vs JSON":>10}')
        for nombre, t in formatos:
            n = contar_tokens_llm(t)
            print(f'  {nombre:<30}{len(t):>12,}{n:>10,}{(n - base) / base * 100:>+9.0f}%')
