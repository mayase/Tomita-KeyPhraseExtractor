from KeyPhrases import *
import json

with open('./articles/0001.txt') as data_file:
    data = json.load(data_file)
    result = getKeyPhrasesOnly(data['article'])
    print(result)
