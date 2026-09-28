class Message:
    def __init__(self, text: str):
        self.text = text

    @staticmethod
    def get_welcome_message() -> "Message":
        return Message("¡Bienvenido a la app Flask con arquitectura MVC!")
