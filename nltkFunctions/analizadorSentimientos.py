import string
import os
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from tipos.sentimientos import Sentimientos
import nltk
nltk.download('stopwords')
nltk.download('punkt')


class NLTKFunctions:
    stop_words = []

    def __init__(self):
        self.stop_words = stopwords.words('spanish')

    def GetRequestIntention(self, texto: str):
        return

    def GetSentimientoValue(self, texto: str) -> Sentimientos:
        full_path = os.path.realpath(__file__)
        filePath = os.path.dirname(full_path) + "/afinn-ES.txt"
        afinnFile = open(filePath, "r")

        diccionario = {}
        puntuacion = 0

        for linea in afinnFile:
            k = linea.split()
            diccionario[k[0]] = k[1]

        words = texto.translate(str.maketrans('', '', string.punctuation))
        words_list = word_tokenize(words)

        words_tokenized = [
            word for word in words_list if word.lower() not in self.stop_words
        ]
        words_tokenized = set(w.lower() for w in words_tokenized)

        for word in words_tokenized:
            if word in diccionario:
                puntuacion = puntuacion + int(diccionario.get(word))

        #print ("Rating:", rating, "\n")
        if puntuacion == 0:
            return Sentimientos.NEUTRAL

        return Sentimientos.POSITIVO if puntuacion > 0 else Sentimientos.NEGATIVO
