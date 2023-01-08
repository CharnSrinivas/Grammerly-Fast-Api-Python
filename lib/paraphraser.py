from parrot import Parrot
import torch
import warnings
import os
warnings.filterwarnings('ignore')

parrot = None
try:
    if os.path.exists('models/parrot.pth'):
        print("Loading Parrot form disk ..")
        parrot = torch.load('models/parrot.pth')
    else:
        print("Downloading Parrot model..")
        parrot = Parrot(
            model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
        print("Saving parrot model to dis..")
        torch.save(parrot, 'models/parrot.pth')
except Exception as e:
    if os.path.exists('models/parrot.pth'):
        os.remove('models/parrot.pth')
    print("Error while loading parrot module: ")
    print(e)


def get_paraphrases(phrases):
    result = []
    for i, phrase in enumerate(phrases):
        print("-"*100)
        print("Input_phrase: ", phrase)
        print("-"*100)
        para_phrases = parrot.augment(input_phrase=phrase)
        if para_phrases is None or len(para_phrases) == 0:
            return None
        variations = []
        for j, para_phrase in enumerate(para_phrases):
            if para_phrase[0] != phrase:
                variations.append(para_phrase[0])
        result.append({
            "original_phrase": phrase,
            "variations": variations
        })
    return result
