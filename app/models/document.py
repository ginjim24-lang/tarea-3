import os

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf"}


class Document:
    """Representa un archivo PDF subido por el usuario y sabe validarse y guardarse."""

    def __init__(self, file: FileStorage | None):
        self.file = file
        self.filename = secure_filename(file.filename) if file and file.filename else ""

    def is_valid_pdf(self) -> bool:
        if not self.file or not self.filename:
            return False
        extension = self.filename.rsplit(".", 1)[-1].lower() if "." in self.filename else ""
        return extension in ALLOWED_EXTENSIONS

    def save(self, upload_folder: str) -> str:
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, self.filename)
        self.file.save(path)
        return path
