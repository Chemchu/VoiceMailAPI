from gmailAPIFunctions.gmailAPI import createEmail
from tipos.intentions import Intention


class AppManager:

    def __init__(self):
        pass

    def IndentificarAccion(self, token, intent: Intention, steps):
        if intent == Intention.ESCRIBIR_CORREO.value[0]:
            return self.CrearCorreo(token, steps)

        if intent == Intention.BORRAR_CORREO.value[0]:
            pass

        if intent == Intention.CLASIFICAR_CORREO.value[0]:
            pass

        if intent == Intention.LEER_CORREO.value[0]:
            pass

    def CrearCorreo(self, token, steps):
        if len(steps) <= 0:
            return "¿A quién va dirigido el correo?"

        if len(steps) == 1:
            return "¿Cuál es el asunto del correo?"

        if len(steps) == 2:
            return "¿Cuál es el contenido del correo?"

        # Enviar correo al destinatario
        createEmail(token=token, subject=steps[1],
                    text=steps[2], to=steps[0])

        return "DONE"
