from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import nltk
from os import linesep
import json
import csv


states = ["ak", "al", "ar", "az", "ca", "co", "ct", "de", "fl", "ga", "hi", "ia", "id", "il",
          "in", "ks", "ky", "la", "ma", "md", "me", "mi", "mn", "mo", "ms", "mt", "nc", "nd", "ne", "nh",
          "nj", "nm", "nv", "ny", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "va", "vt",
          "wa", "wi", "wv", "wy"]

states_names = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
                'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
                'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
                'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
                'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
                'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia',
                'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}

nltk.download('stopwords')
nltk.download('punkt')


def getState(data):
    if data["place"] != None and data["place"]["country_code"] == "US":
        state = str(data["place"]["full_name"]).lower().split(", ")
        if len(state) > 1:
            return state[1]


def isState(state):
    if state in states:
        return True
    return False


def analize(words):
    myfile = open("AFINN-111.txt", "r")
    dictionary = {}
    rating = 0

    for line in myfile:
        k = line.split()
        dictionary[k[0]] = k[1]

    words = words.translate(str.maketrans('', '', string.punctuation))
    words_list = word_tokenize(words)
    stopwords = nltk.corpus.stopwords.words('english')

    words_tokenized = [
        word for word in words_list if word.lower() not in stopwords]
    #words_tokenized = [word for word in words_tokenized if word not in string.punctuation]
    words_tokenized = set(w.lower() for w in words_tokenized)

    # print(dictionary)
    # print(words_tokenized)

    for word in words_tokenized:
        if word in dictionary:
            rating = rating + int(dictionary.get(word))

    #print ("Rating:", rating, "\n")
    return rating


def readTweets():
    file = "output.txt"
    analisis = "AFINN-111.txt"
    states_ratings = {}
    states_count = {}

    array = []
    with open(file, "r") as ins:

        for line in ins:
            if (len(line) > 1):  # to avoid empty lines
                data = json.loads(line)
                if "created_at" in data:
                    state = getState(data)
                    if isState(state):
                        if "text" in data:
                            frase = data["text"]
                            print("Phrase:", frase)
                            print("State:", states_names.get(state.upper()))

                            states_ratings[states_names.get(
                                state.upper())] = analize(frase)

                            if state in states_count:
                                states_count[states_names.get(
                                    state.upper())] += 1
                            else:
                                states_count[states_names.get(
                                    state.upper())] = 1

                            #states_count[states_names.get(state.upper())] = [analize(frase)]
                            print("Rating:", states_ratings[states_names.get(state.upper())], "\nNumber of tweets from", states_names.get(
                                state.upper()), ":", states_count[states_names.get(state.upper())])
                            average = (states_ratings[states_names.get(
                                state.upper())]) / (states_count[states_names.get(state.upper())])
                            print("Emotional analysis:", average, "\n")
                            print(states_count)
                            analize(frase)

        print("\nRatings:", states_ratings)
        print("Count:", states_count)


analize("Fud, fraud.., great")

readTweets()
