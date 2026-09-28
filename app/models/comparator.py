import difflib
from dataclasses import dataclass


@dataclass
class PalabraComparada:
    texto: str
    estado: str  # "igual", "falta_en_etiqueta" o "solo_en_etiqueta"


class Comparator:
    """Compara el texto de referencia contra el de la etiqueta.

    Ignora mayusculas/minusculas y saltos de linea: normaliza cada texto a
    una lista de palabras en minusculas antes de compararlas.
    """

    @staticmethod
    def _tokenizar(texto: str) -> list[str]:
        return texto.split()

    @classmethod
    def comparar(
        cls, texto_referencia: str, texto_etiqueta: str
    ) -> tuple[list[PalabraComparada], list[PalabraComparada]]:
        palabras_ref = cls._tokenizar(texto_referencia)
        palabras_etq = cls._tokenizar(texto_etiqueta)

        normal_ref = [p.lower() for p in palabras_ref]
        normal_etq = [p.lower() for p in palabras_etq]

        matcher = difflib.SequenceMatcher(None, normal_ref, normal_etq)

        resultado_referencia: list[PalabraComparada] = []
        resultado_etiqueta: list[PalabraComparada] = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                resultado_referencia += [
                    PalabraComparada(p, "igual") for p in palabras_ref[i1:i2]
                ]
                resultado_etiqueta += [
                    PalabraComparada(p, "igual") for p in palabras_etq[j1:j2]
                ]
            elif tag == "delete":
                resultado_referencia += [
                    PalabraComparada(p, "falta_en_etiqueta") for p in palabras_ref[i1:i2]
                ]
            elif tag == "insert":
                resultado_etiqueta += [
                    PalabraComparada(p, "solo_en_etiqueta") for p in palabras_etq[j1:j2]
                ]
            elif tag == "replace":
                resultado_referencia += [
                    PalabraComparada(p, "falta_en_etiqueta") for p in palabras_ref[i1:i2]
                ]
                resultado_etiqueta += [
                    PalabraComparada(p, "solo_en_etiqueta") for p in palabras_etq[j1:j2]
                ]

        return resultado_referencia, resultado_etiqueta
