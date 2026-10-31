"""Exibição do corretor comum aos capítulos do livro.

A configuração é incorporada na mesma saída HTML do motor para funcionar
com as saídas isoladas de células Jupyter e com a publicação estática MyST.
"""

import json
from pathlib import Path

_MARCADOR = "<!-- MARCADOR_CONFIG_CORRETOR -->"
_MARCADOR_JS = "<!-- MARCADOR_JS_CORRETOR -->"
_MODELO = Path(__file__).with_name("corretor_compartilhado.html")
_SCRIPT = Path(__file__).with_name("corretor.js")


def gerar_html(configuracao):
    """Gera a saída autocontida sem modificar o motor JavaScript original."""
    modelo = _MODELO.read_text(encoding="utf-8")
    if modelo.count(_MARCADOR) != 1 or modelo.count(_MARCADOR_JS) != 1:
        raise ValueError("O modelo do corretor deve conter os dois marcadores.")
    config_json = json.dumps(configuracao, ensure_ascii=False).replace(
        "<", "\\u003c"
    ).replace(">", "\\u003e").replace("&", "\\u0026")
    configuracao_embutida = (
        '<script type="application/json" data-configuracao-corretor>'
        + config_json
        + "</script>"
    )
    script = "<script>\n" + _SCRIPT.read_text(encoding="utf-8") + "</script>"
    return modelo.replace(_MARCADOR, configuracao_embutida, 1).replace(
        _MARCADOR_JS, script, 1
    )


def exibir_corretor(configuracao):
    """Mostra o corretor e preserva sua saída HTML no notebook."""
    from IPython.display import HTML, display

    display(HTML(gerar_html(configuracao)))
