import os
import sys

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import json

nlp = en_core_web_sm.load()

path = 'temp/podcast-data-generator-'+ sys.argv[1] +'/podcasts_palettes'
files = os.listdir(path)


def read_json_file(filepath):
    # read file
    fullpath = path +'/'+ filepath
    with open(fullpath, 'r') as myfile:
        file = myfile.read()
    # parse file
    podcast = json.loads(file)
    return podcast

def parse_entities(text):
    entities = {}
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ in entities:
            entities[entity.label_].append(entity.text)
        else:
            entities[entity.label_] = [entity.text]
    return entities

for i in range (0, len(files)):
    pod = read_json_file(files[i])
    try:
        pod['entities'] = parse_entities(pod['description'])
    except:
        print('error')
        continue

    episodes = []

    for ep in pod['items']:
        try:
            ep['entities'] = parse_entities(ep['content'])
        except:
            print('error')
            continue
        episodes.append(ep)

    pod['items'] = episodes
    jsonFile =  open('temp/podcasts-with-entities/'+files[i], 'w') 
    jsonFile.write(json.dumps(pod, indent=4))
    jsonFile.close()
    print('{:.2%} done.'.format(i/len(files))*100)