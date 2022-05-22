from enum import Enum


class Intention(Enum):
    ESCRIBIR_CORREO = 'crearCorreo',
    LEER_CORREO = "leerCorreo",
    BORRAR_CORREO = "borrarCorreo",
    CLASIFICAR_CORREO = "clasificarCorreo"
