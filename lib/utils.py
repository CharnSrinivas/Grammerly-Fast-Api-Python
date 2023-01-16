import re
import torch

from textblob import TextBlob
from gramformer import Gramformer

gf = Gramformer(models = 1, use_gpu=False) # 1=corrector, 2=detectorgf = 

def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_seed(1212)


def split_into_sentences(text):
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    digits = "([0-9])"
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text:
        text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms+" "+starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" +
                  alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets +
                  "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" "+suffixes+"[.] "+starters, " \\1<stop> \\2", text)
    text = re.sub(" "+suffixes+"[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if "\"" in text:
        text = text.replace(".\"", "\".")
    if "!" in text:
        text = text.replace("!\"", "\"!")
    if "?" in text:
        text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    print('sentences ', sentences)
    # if len(sentences) > 1:
    # sentences = sentences[:-1]    
    result = []
    for  s in sentences:
        phrase = s.strip()
        if phrase is None or phrase == '':
            continue
        result.append(phrase)
    return result


def correct_grammar_sentences(text):
    corrected_results = []
    sentences = split_into_sentences(text=text)
    for sentence in sentences:
        corrected_sentences = list(gf.correct(input_sentence=sentence,max_candidates=1))[0]
        edits = gf.get_edits(cor=corrected_sentences,orig=sentence)

        res ={
            'original':sentence,
            'corrected':corrected_sentences,
            'edits':edits
        }
        corrected_results.append(res)
    return corrected_results


def get_emotion(text):
    text_blob  = TextBlob(text)
    sentiment = text_blob.sentiment
    # Create two new columns 'Subjectivity' & 'Polarity
    def get_sentiment(polarity):
        if polarity > 0.5:
            return "VERY HAPPY"
        elif polarity > 0.3:
            return "HAPPY"
        elif polarity >= 0:
            return "NEUTRAL"
        elif polarity > -0.2:
            return "SAD"
        else:
            return "VERY SAD"

    return get_sentiment(sentiment.polarity)

