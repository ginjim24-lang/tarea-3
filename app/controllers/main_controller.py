from flask import Blueprint, current_app, render_template, request

from app.models.comparator import Comparator
from app.models.document import Document
from app.models.message import Message
from app.models.spell_checker import RevisorOrtografico

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    message = Message.get_welcome_message()
    return render_template("index.html", message=message.text)


@main_bp.route("/comparar", methods=["POST"])
def comparar():
    referencia = Document(request.files.get("referencia"))
    etiqueta = Document(request.files.get("etiqueta"))

    errores = []
    if not referencia.is_valid_pdf():
        errores.append("El archivo de información de referencia debe ser un PDF.")
    if not etiqueta.is_valid_pdf():
        errores.append("El archivo del arte de la etiqueta debe ser un PDF.")

    if errores:
        message = Message.get_welcome_message()
        return render_template("index.html", message=message.text, errores=errores)

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    referencia.save(upload_folder)
    etiqueta.save(upload_folder)

    texto_referencia = referencia.extract_text()
    texto_etiqueta = etiqueta.extract_text()

    palabras_referencia, palabras_etiqueta = Comparator.comparar(
        texto_referencia, texto_etiqueta
    )

    _, palabras_sospechosas = RevisorOrtografico.revisar(texto_etiqueta)
    sospechosas_set = set(palabras_sospechosas)

    palabras_etiqueta_vista = [
        {
            "texto": palabra.texto,
            "estado": palabra.estado,
            "es_sospechosa": palabra.texto in sospechosas_set,
        }
        for palabra in palabras_etiqueta
    ]

    return render_template(
        "resultado.html",
        referencia_nombre=referencia.filename,
        etiqueta_nombre=etiqueta.filename,
        palabras_referencia=palabras_referencia,
        palabras_etiqueta=palabras_etiqueta_vista,
        palabras_sospechosas=palabras_sospechosas,
    )
