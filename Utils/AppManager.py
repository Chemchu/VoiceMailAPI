from gmailAPIFunctions.gmailAPI import createEmail
from tipos.intentions import Intention


class AppManager:

    def __init__(self):
        pass

    def IndentificarAccion(self, token, intent: Intention, steps, query):
        if intent == Intention.ESCRIBIR_CORREO.value[0]:
            return self.CrearCorreo(token, steps, query)

        if intent == Intention.BORRAR_CORREO.value[0]:
            pass

        if intent == Intention.CLASIFICAR_CORREO.value[0]:
            pass

        if intent == Intention.LEER_CORREO.value[0]:
            pass

    def CrearCorreo(self, token, steps, query):
        if len(steps) <= 0:
            return "¿A quién va dirigido el correo?"

        if len(steps) == 1:
            return "¿Cuál es el asunto del correo?"

        if len(steps) == 2:
            return "¿Cuál es el contenido del correo?"

        print(query)

        correoDestinatarioLN = query[1].split("arroba")
        destinatarioIzquierda = correoDestinatarioLN[0].split()
        destinatarioDerecha = correoDestinatarioLN[1].split()

        destinatario = ''.join([str(elem) for elem in destinatarioIzquierda])
        destinatario = destinatario + "@" + \
            ''.join([str(elem) for elem in destinatarioDerecha])

        # Enviar correo al destinatario
        createEmail(token=token, subject=query[2],
                    text=query[3], to=destinatario)

        return "DONE"
