from flask import Blueprint, current_app, render_template, request

from app.models.document import Document
from app.models.message import Message

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

    return render_template(
        "resultado.html",
        referencia_nombre=referencia.filename,
        etiqueta_nombre=etiqueta.filename,
    )
