from logging import exception
from gmailAPIFunctions.gmailAPI import createEmail, createLabel, getMessages, moveToLabel
from nltkFunctions import NLTKFunctions
from tipos.intentions import Intention


class AppManager:
    NLTKFunctions = None

    def __init__(self, nltk):
        self.NLTKFunctions = nltk

    def IndentificarAccion(self, token, intent, steps, query):

        # print("###########")
        # print(Intention.CLASIFICAR_CORREO)
        # print(Intention.CLASIFICAR_CORREO.value)
        # print(intent)
        # print("###########")

        if intent == Intention.ESCRIBIR_CORREO.value:
            return self.CrearCorreo(token, steps, query)

        if intent == Intention.BORRAR_CORREO.value:
            return self.BorrarCorreo(token, steps, query)

        if intent == Intention.CLASIFICAR_CORREO.value:
            return self.ClasificarCorreos(token, steps, query)

        if intent == Intention.LEER_CORREO.value:
            return self.LeerCorreo(token, steps, query)

    # def IndentificarQuerySentimientos(self, texto):
    #     return self.NLTKFunctions.GetSentimientoLabelValue(texto)

    def ClasificarCorreos(self, token, steps, query):
        if len(steps) <= 0:
            return "¿Qué tipo de correos quieres clasificar?"

        if len(steps) == 1:
            return "¿Cómo quieres que se llame el label?"

        correos = getMessages(token, 100)
        sentimientoPedido = self.NLTKFunctions.GetSentimientoLabelValue(
            query[1])

        try:
            createLabel(token, query[2])
            print("Label creado!!!!!!!!!!")
        except Exception as e:
            if e == "Label name exists or conflicts":
                print(e)
            pass

        for index in correos:
            try:
                msg = correos[index]["message"]
                sentimiento = self.NLTKFunctions.GetSentimientoValue(msg)
                msg_id = correos[index]["id"]
                if msg_id is None:
                    continue

                if sentimiento.name == sentimientoPedido:
                    moveToLabel(
                        token=token, message_id=msg_id, label_name=query[2])
            except Exception as e:
                print("Excepcion!!:", e)
                pass

        return "DONE"

    def BorrarCorreo(self, token, steps, query):
        if len(steps) <= 0:
            return "¿Qué correo quieres borrar?"

        pass

    def LeerCorreo(self, token, steps, query):
        if len(steps) <= 0:
            return "¿Quién es el remitente del correo?"

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
            return {"message": "Lo siento, no hay correos de esa persona", "successful": True}

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
