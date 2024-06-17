import os
from typing import Any

template_path = os.path.join(os.path.dirname(__file__), "templates")


def load_html(filename: str, *params: Any, **kwargs) -> str:
    """
    Retorna o conteúdo de um arquivo template HTML.
    """
    if not filename.endswith(".html"):
        filename += ".html"

    with open(os.path.join(template_path, filename), encoding="UTF-8") as file:
        content = file.read()

    for key, value in kwargs.items():
        content = content.replace("{" + key + "}", str(value))

    return content.format(*params)
