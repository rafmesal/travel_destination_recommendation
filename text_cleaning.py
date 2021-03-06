import pandas as pd
import numpy as np
import pickle
import gensim
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk


def lemmatize_and_stem(text):
    """
    Lemmatize and stem text
    """
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos="v"))


def preprocess(text):
    """Lowercase, lemmatize, and stem text"""
    result = []
    stopwords = [
        "a",
        "about",
        "above",
        "across",
        "after",
        "afterwards",
        "again",
        "against",
        "all",
        "almost",
        "alone",
        "along",
        "already",
        "also",
        "although",
        "always",
        "am",
        "among",
        "amongst",
        "amoungst",
        "amount",
        "an",
        "and",
        "another",
        "any",
        "anyhow",
        "anyone",
        "anything",
        "anyway",
        "anywhere",
        "are",
        "around",
        "as",
        "at",
        "back",
        "be",
        "became",
        "because",
        "become",
        "becomes",
        "becoming",
        "been",
        "before",
        "beforehand",
        "behind",
        "being",
        "below",
        "beside",
        "besides",
        "between",
        "beyond",
        "bill",
        "both",
        "bottom",
        "but",
        "by",
        "call",
        "can",
        "cannot",
        "cant",
        "co",
        "computer",
        "con",
        "could",
        "couldnt",
        "cry",
        "de",
        "describe",
        "detail",
        "did",
        "didn",
        "do",
        "does",
        "doesn",
        "doing",
        "don",
        "done",
        "down",
        "due",
        "during",
        "each",
        "eg",
        "eight",
        "either",
        "eleven",
        "else",
        "elsewhere",
        "empty",
        "enough",
        "etc",
        "even",
        "ever",
        "every",
        "everyone",
        "everything",
        "everywhere",
        "except",
        "few",
        "fifteen",
        "fifty",
        "fill",
        "find",
        "fire",
        "first",
        "five",
        "for",
        "former",
        "formerly",
        "forty",
        "found",
        "four",
        "from",
        "front",
        "full",
        "further",
        "get",
        "give",
        "go",
        "had",
        "has",
        "hasnt",
        "have",
        "he",
        "hence",
        "her",
        "here",
        "hereafter",
        "hereby",
        "herein",
        "hereupon",
        "hers",
        "herself",
        "him",
        "himself",
        "his",
        "how",
        "however",
        "hundred",
        "i",
        "ie",
        "if",
        "in",
        "inc",
        "indeed",
        "interest",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "just",
        "keep",
        "kg",
        "km",
        "last",
        "latter",
        "latterly",
        "least",
        "less",
        "ltd",
        "made",
        "make",
        "many",
        "may",
        "me",
        "meanwhile",
        "might",
        "mill",
        "mine",
        "more",
        "moreover",
        "most",
        "mostly",
        "move",
        "much",
        "must",
        "my",
        "myself",
        "name",
        "namely",
        "neither",
        "never",
        "nevertheless",
        "next",
        "nine",
        "no",
        "nobody",
        "none",
        "noone",
        "nor",
        "not",
        "nothing",
        "now",
        "nowhere",
        "of",
        "off",
        "often",
        "on",
        "once",
        "one",
        "only",
        "onto",
        "or",
        "other",
        "others",
        "otherwise",
        "our",
        "ours",
        "ourselves",
        "out",
        "over",
        "own",
        "part",
        "per",
        "perhaps",
        "please",
        "put",
        "quite",
        "rather",
        "re",
        "really",
        "regarding",
        "same",
        "say",
        "see",
        "seem",
        "seemed",
        "seeming",
        "seems",
        "serious",
        "several",
        "she",
        "should",
        "show",
        "side",
        "since",
        "sincere",
        "six",
        "sixty",
        "so",
        "some",
        "somehow",
        "someone",
        "something",
        "sometime",
        "sometimes",
        "somewhere",
        "still",
        "such",
        "system",
        "take",
        "ten",
        "than",
        "that",
        "the",
        "their",
        "them",
        "themselves",
        "then",
        "thence",
        "there",
        "thereafter",
        "thereby",
        "therefore",
        "therein",
        "thereupon",
        "these",
        "they",
        "thick",
        "thin",
        "third",
        "this",
        "those",
        "though",
        "three",
        "through",
        "throughout",
        "thru",
        "thus",
        "to",
        "together",
        "too",
        "top",
        "toward",
        "towards",
        "twelve",
        "twenty",
        "two",
        "un",
        "under",
        "unless",
        "until",
        "up",
        "upon",
        "us",
        "used",
        "using",
        "various",
        "very",
        "via",
        "was",
        "we",
        "well",
        "were",
        "what",
        "whatever",
        "when",
        "whence",
        "whenever",
        "where",
        "whereafter",
        "whereas",
        "whereby",
        "wherein",
        "whereupon",
        "wherever",
        "whether",
        "which",
        "while",
        "whither",
        "who",
        "whoever",
        "whole",
        "whom",
        "whose",
        "why",
        "will",
        "with",
        "within",
        "without",
        "would",
        "yet",
        "you",
        "your",
        "yours",
        "yourself",
        "yourselves",
        "danube",
        "austria",
        "hallstatt",
        "salzburg",
        "tirol",
        "vienna",
        "antwerp",
        "bruges",
        "brussels",
        "ghent",
        "belgium",
        "mostar",
        "sarajevo",
        "bosnia-herzegovina",
        "dalmatian",
        "dubrovnik",
        "hvar",
        "istria",
        "korčula",
        "zagreb",
        "croatia",
        "aarhus",
        "copenhagen",
        "ærø",
        "denmark",
        "bath",
        "blackpool",
        "brighton",
        "cambridge",
        "canterbury",
        "cornwall",
        "cotswolds",
        "dover",
        "durham",
        "glastonbury",
        "ironbridge",
        "liverpool",
        "london",
        "oxford",
        "portsmouth",
        "stonehenge",
        "avebury",
        "stratford",
        "warwick",
        "coventry",
        "windsor",
        "york",
        "england",
        "tallinn",
        "estonia",
        "helsinki",
        "finland",
        "aix",
        "en",
        "albi",
        "alsace",
        "annecy",
        "antibes",
        "arles",
        "avignon",
        "bayeux",
        "brittany",
        "burgundy",
        "carcassonne",
        "cassis",
        "chamonix",
        "chartres",
        "collioure",
        "colmar",
        "côtes",
        "du",
        "rhône",
        "dordogne",
        "french",
        "basque",
        "country",
        "honfleur",
        "languedoc",
        "roussillon",
        "loire",
        "luberon",
        "lyon",
        "marseille",
        "monaco",
        "mont",
        "michel",
        "normandy",
        "paris",
        "provence",
        "reims",
        "verdun",
        "rouen",
        "sarlat",
        "la",
        "canéda",
        "strasbourg",
        "versailles",
        "villefranche",
        "sur",
        "mer",
        "france",
        "baden",
        "bavaria",
        "bavarian",
        "berlin",
        "cologne",
        "dresden",
        "frankfurt",
        "hamburg",
        "mosel",
        "munich",
        "nürnberg",
        "rhine",
        "rothenburg",
        "tauber",
        "germany",
        "trier",
        "würzburg",
        "athens",
        "delphi",
        "greek",
        "hydra",
        "kardamyli",
        "mani",
        "monemvasia",
        "mykonos",
        "nafplio",
        "olympia",
        "peloponnese",
        "santorini",
        "greece",
        "budapest",
        "eger",
        "hungary",
        "aran",
        "belfast",
        "connemara",
        "mayo",
        "clare",
        "burren",
        "county",
        "donegal",
        "derry",
        "dingle",
        "dublin",
        "galway",
        "kenmare",
        "kerry",
        "kilkenny",
        "cashel",
        "kinsale",
        "cobh",
        "portrush",
        "antrim",
        "waterford",
        "wexford",
        "ireland",
        "amalfi",
        "assisi",
        "capri",
        "cinque",
        "terre",
        "civita",
        "bagnoregio",
        "dolomites",
        "florence",
        "italian",
        "lucca",
        "milan",
        "naples",
        "orvieto",
        "pisa",
        "pompeii",
        "herculaneum",
        "ravenna",
        "rome",
        "sicily",
        "siena",
        "sorrento",
        "tuscan",
        "tuscany",
        "venice",
        "italy",
        "amsterdam",
        "delft",
        "edam",
        "haarlem",
        "hague",
        "netherlands",
        "bergen",
        "norwegian",
        "fjords",
        "oslo",
        "norway",
        "auschwitz",
        "birkenau",
        "gdańsk",
        "kraków",
        "warsaw",
        "poland",
        "algarve",
        "coimbra",
        "douro",
        "lisbon",
        "nazaré",
        "porto",
        "sintra",
        "évora",
        "óbidos",
        "portugal",
        "petersburg",
        "russia",
        "edinburgh",
        "glasgow",
        "isle",
        "skye",
        "oban",
        "mull",
        "iona",
        "scottish",
        "highlands",
        "andrews",
        "scotland",
        "bratislava",
        "slovakia",
        "slovenia",
        "bled",
        "ljubljana",
        "slovenia",
        "andalucía",
        "barcelona",
        "camino",
        "santiago",
        "costa",
        "sol",
        "córdoba",
        "granada",
        "madrid",
        "pamplona",
        "salamanca",
        "san",
        "sebastián",
        "santiago",
        "compostela",
        "sevilla",
        "spanish",
        "basque",
        "toledo",
        "spain",
        "kalmar",
        "stockholm",
        "sweden",
        "appenzell",
        "bern",
        "berner",
        "oberland",
        "gimmelwald",
        "geneva",
        "luzern",
        "zermatt",
        "zürich",
        "switzerland",
        "ephesus",
        "istanbul",
        "turkey",
        "wales",
        "northern",
        "north",
        "eastern",
        "east",
        "southern",
        "south",
        "western",
        "west",
        "language",
        "europe",
        "european",
        "nation",
        "black",
        "polish",
        "german",
        "croatian",
        "swiss",
        "irish",
        "russian",
        "norman",
        "roman",
        "state",
        "turkish",
        "center",
        "nice",
        "portuguese",
        "ii",
        "split",
        "data",
        "period",
        "way",
        "population",
        "government",
        "election",
        "work",
        "land",
        "municipal",
        "center",
        "st",
        "english",
        "th",
        "know",
        "breton",
        "andalusia",
        "mediterranean",
        "scandinavia",
        "area",
        "street",
        "road",
        "station",
        "hungarian",
        "austrian",
        "le",
        "xiv",
        "ottoman",
        "peninsula",
        "byzantine",
        "district",
        "number",
        "dutch",
        "belgian",
        "nation",
        "venetian",
        "ft",
        "providence",
        "republic",
        "capital",
        "british",
        "tyrol",
        "nuremberg",
        "uk",
        "britain",
        "cornish",
        "louis",
        "include",
        "includes",
        "central",
        "center"
    ]
    for token in simple_preprocess(text):
        if token not in stopwords:
            result.append(lemmatize_and_stem(token))
    return result


def get_aggregate_score(lda_model, bow_corpus, i=0):
    """
    Get the combined aggregate score for topics using rick_steves and wikipedia
    """
    # scores for each summary. There are 213 cities.
    rick_steves = lda_model[bow_corpus[i]]
    wikipedia = lda_model[bow_corpus[i+213]]

    # some wiki summaries have probability of 0 which does not automatically
    # appear in scoring of lda. Adds the 0 score
    if len(wikipedia) != 5:
        indices = []
        for item in wikipedia:
            indices.append(item[0])
        for index in list(range(5)):
            if index not in indices:
                wikipedia.append((index, 0))

    # generate the aggregate score as mean value
    aggregate = {}
    for index, score in rick_steves:
        rs_score = score
        wiki_score = wikipedia[index][1]
        aggregate[index] = np.mean([score, wiki_score])
    return aggregate


def replace_periods(string):
    """Replaces periods with nothing"""
    return string.replace('.', '')
