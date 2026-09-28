import os
import re

from spylls.hunspell import Dictionary

UNIDADES = {
    "mg", "ml", "g", "kg", "kcal", "cal", "l", "oz", "lb", "mcg", "ui", "%",
}

_PATRON_NUMERO = re.compile(r"^\d+([.,]\d+)?[a-zA-Z%]*$")

_RUTA_DICCIONARIO = os.path.join(os.path.dirname(__file__), "..", "data", "es_ES")


class RevisorOrtografico:
    """Revisa la ortografia en español de un texto usando el diccionario Hunspell.

    Ignora numeros (200, 3.5) y numeros pegados a una unidad de medida
    (200g, 5ml, 10kcal) para no marcarlos como faltas de ortografia.
    """

    _dictionary = Dictionary.from_files(_RUTA_DICCIONARIO)

    @classmethod
    def _limpiar(cls, palabra: str) -> str:
        """Quita signos de puntuacion al inicio/final (comas, puntos, parentesis...)."""
        return re.sub(r"^[^\wáéíóúñü]+|[^\wáéíóúñü]+$", "", palabra, flags=re.IGNORECASE)

    @classmethod
    def _es_ignorable(cls, palabra_limpia: str) -> bool:
        if not palabra_limpia:
            return True
        if palabra_limpia.lower() in UNIDADES:
            return True
        if _PATRON_NUMERO.match(palabra_limpia):
            return True
        return False

    @classmethod
    def revisar(cls, texto: str) -> tuple[list[tuple[str, bool]], list[str]]:
        """Devuelve (palabra, es_sospechosa) por cada palabra, y la lista de sospechosas."""
        resultado: list[tuple[str, bool]] = []
        sospechosas: list[str] = []

        for palabra in texto.split():
            limpia = cls._limpiar(palabra)

            if cls._es_ignorable(limpia):
                resultado.append((palabra, False))
                continue

            es_sospechosa = not cls._dictionary.lookup(limpia)
            resultado.append((palabra, es_sospechosa))
            if es_sospechosa:
                sospechosas.append(palabra)

        return resultado, sospechosas
