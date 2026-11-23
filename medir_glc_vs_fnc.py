import sys
import io
import gc
import time
import contextlib
import importlib

import json_to_toon_lex as lx

# ---------------------------------------------------------------
# Compara la GLC original contra su versión en FNC, para las dos
# salidas (TOON completo y tipo TOON), con el mismo archivo JSON.
#
# Medidas:
#  - Tamaño de la gramática: producciones, no terminales y estados
#    de la tabla LALR que construye PLY.
#  - Pasos del análisis: tokens leídos (shift) y producciones
#    aplicadas (reduce). Cada reduce es un paso de la derivación.
#  - Tiempo: lo que tarda parser.parse() (mejor promedio de varias rondas).
#  - En FNC toda derivación de una cadena de n tokens usa exactamente
#    2n - 1 producciones: n del tipo A -> a y n - 1 del tipo A -> B C.
#
# Uso:  py medir_glc_vs_fnc.py juegos.json
# ---------------------------------------------------------------

VERSIONES = [
    ('TOON completo', 'json_to_toon_yacc', 'json_to_toon_fnc_yacc'),
    ('Tipo TOON', 'json_to_toon_like_yacc', 'json_to_toon_like_fnc_yacc'),
]
REPETICIONES = 10
RONDAS = 5


class ContadorPasos:
    """Recibe la bitácora de PLY (parse con debug) y cuenta shift y reduce."""
    def __init__(self):
        self.shift = 0
        self.reduce = 0

    def debug(self, msg, *args):
        if msg.startswith('Action : Shift'):
            self.shift += 1

    def info(self, msg, *args):
        if msg.startswith('Action : Reduce'):
            self.reduce += 1

    def error(self, msg, *args):
        pass

    warning = critical = error


def nuevo_lexer():
    lex = lx.lexer.clone()
    lex.errores = 0
    lex.lineno = 1
    return lex


def contar_tokens(texto):
    lex = nuevo_lexer()
    lex.input(texto)
    return sum(1 for _ in lex)


def medir(mod, texto):
    parser = mod.parser
    datos = {
        'producciones': len(parser.productions) - 1,   # sin la regla S' -> archivo que agrega PLY
        'no terminales': len({p.name for p in parser.productions[1:]}),
        'estados LALR': len(parser.action),
    }

    # Pasos del análisis (shift / reduce)
    contador = ContadorPasos()
    parser.parse(texto, lexer=nuevo_lexer(), debug=contador)
    datos['shift (tokens)'] = contador.shift
    datos['reduce (pasos de derivación)'] = contador.reduce

    # Tiempo de parser.parse(): una corrida de calentamiento y luego el
    # mejor promedio de RONDAS rondas (así afecta menos lo que haga la PC)
    # El recolector de basura se apaga mientras se mide (como hace timeit),
    # si no, el que se mide después sale más lento solo por el orden.
    resultado = parser.parse(texto, lexer=nuevo_lexer())
    mejor = None
    gc.collect()
    gc.disable()
    try:
        for _ in range(RONDAS):
            inicio = time.perf_counter()
            for _ in range(REPETICIONES):
                parser.parse(texto, lexer=nuevo_lexer())
            promedio = (time.perf_counter() - inicio) / REPETICIONES * 1000
            mejor = promedio if mejor is None else min(mejor, promedio)
    finally:
        gc.enable()
    datos['tiempo (ms)'] = mejor
    return datos, resultado


def fila(nombre, a, b, decimales=0):
    if decimales:
        va, vb = f'{a:.{decimales}f}', f'{b:.{decimales}f}'
    else:
        va, vb = str(a), str(b)
    cambio = f'{(b - a) / a * 100:+.0f}%' if a else '-'
    print(f'  {nombre:<30}{va:>12}{vb:>12}{cambio:>10}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Falta archivo de entrada')
        sys.exit(1)

    texto = lx.leer_archivo(sys.argv[1])
    n_tokens = contar_tokens(texto)
    print(f'Archivo: {sys.argv[1]}  ({n_tokens} tokens)\n')

    for titulo, original, fnc in VERSIONES:
        # Al importar, PLY construye las tablas e imprime mensajes; se ocultan
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            m_glc = importlib.import_module(original)
            m_fnc = importlib.import_module(fnc)
            d_glc, r_glc = medir(m_glc, texto)
            d_fnc, r_fnc = medir(m_fnc, texto)

        print(f'== {titulo}: {original}.py vs {fnc}.py')
        print(f'  {"":<30}{"GLC":>12}{"FNC":>12}{"cambio":>10}')
        for k in d_glc:
            fila(k, d_glc[k], d_fnc[k], 2 if k.startswith('tiempo') else 0)
        print(f'  Salida idéntica: {"sí" if r_glc == r_fnc else "NO"}')
        print(f'  En FNC, reduce = 2 x tokens - 1 = {2 * n_tokens - 1}: '
              f'{"sí" if d_fnc["reduce (pasos de derivación)"] == 2 * n_tokens - 1 else "no"}\n')
