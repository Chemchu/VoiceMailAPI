from gmailAPIFunctions.gmailAPI import createEmail, getMessages
from tipos.intentions import Intention


class AppManager:

    def __init__(self):
        pass

    def IndentificarAccion(self, token, intent: Intention, steps, query):
        if intent == Intention.ESCRIBIR_CORREO.value[0]:
            return self.CrearCorreo(token, steps, query)

        if intent == Intention.BORRAR_CORREO.value[0]:
            return self.BorrarCorreo(token, steps, query)

        if intent == Intention.CLASIFICAR_CORREO.value[0]:
            return self.ClasificarCorreos(token, steps, query)

        if intent == Intention.LEER_CORREO.value[0]:
            return self.LeerCorreo(token, steps, query)

    def ClasificarCorreos(self, token, steps, query):
        if len(steps) <= 0:
            return "¿Qué tipo de correos quieres clasificar?"

        if len(steps) == 1:
            return "¿Cómo quieres que se llame el label?"

        pass

    def BorrarCorreo(self, token, steps, query):
        if len(steps) <= 0:
            return "¿Qué correo quieres borrar?"

        pass

    def LeerCorreo(self, token, steps, query):
        if len(steps) <= 0:
            return "¿De quién es el correo que quieres que te lea?"

        correos = getMessages(token, 100)
        c = None

        for index in correos:
            try:
                destinatario = query[-1]
                if destinatario in correos[index]["from"]:
                    c = correos[index]
                    break
            except Exception as e:
                print(e)
                pass

        if c == None:
            return {"message": "No hay correos de esa persona", "successful": True}

        return {"message": c["message"], "successful": True}

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
