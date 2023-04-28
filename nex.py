import os
import sys
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import json
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

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
        podcast_description = strip_tags(pod['description'])
        pod['entities'] = parse_entities(podcast_description)
    except:
        print('error')
        continue

    episodes = []

    for ep in pod['items']:
        try:
            episode_description = strip_tags(ep['content'])
            ep['entities'] = parse_entities(episode_description)
        except:
            print('error')
            continue
        episodes.append(ep)

    pod['items'] = episodes
    jsonFile =  open('temp/podcasts-with-entities/'+files[i], 'w') 
    jsonFile.write(json.dumps(pod, indent=4))
    jsonFile.close()
    print('{:.2%} done.'.format(i/len(files))*100)