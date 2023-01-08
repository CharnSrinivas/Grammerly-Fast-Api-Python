from fastapi import FastAPI
from lib.utils import split_into_sentences, correct_grammar_sentences, get_emotion
from gingerit.gingerit import GingerIt
# from lib.paraphraser import get_paraphrases
parser = GingerIt()

app = FastAPI()
from pydantic import BaseModel

class Body(BaseModel):
    text: str

@app.post('/paraphrase')
def para_phrase(body:Body):
    print(body)
    print(body)
    if body and body.text:
        text = body.text
        sentences = split_into_sentences(text)
        phrases= get_paraphrases(sentences)
        if len(sentences) >0 and phrases is None:
            return ({"error":"Invalid sentences! Please check the grammar and try again"})
        return ({'data':phrases})
    else:
        return ({"error": "'text' field is not provided"})

@app.post('/grammar')
def grammar(body:Body):
    print((body.text))
    if body and body.text:
        text = body.text
        corrected = correct_grammar_sentences(text=text)
        return ({'data':corrected})
    else:
        return ({"error": "'text' field is not provided"})

@app.post('/emotion')
def emotion(body:Body):
    if body and body.text:
        text = body.text
        text_emotion = get_emotion(text=text)
        return ({'data':text_emotion})
    else:
        return ({"error": "'text' field is not provided"})