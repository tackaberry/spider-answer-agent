
from pathlib import Path
import os
from utils import get_shortened, n_tokens
import pandas as pd
import openai
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


openai.api_key = config['default']['openaiApiKey']


def createEmbeddings():
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    folder = 'data/txt'
    entries = os.listdir(folder)

    texts=[]

    for file in os.listdir(folder):
        with open(folder + "/" + file, "r", encoding="UTF-8") as f:
            text = f.read()
            texts.append((file, text))

    df = pd.DataFrame(texts, columns = ['fname', 'text'])

    df['text'] = df.fname + ". " + df.text
    df['n_tokens'] = n_tokens(df.text)

    shortened = get_shortened(df)

    df = pd.DataFrame(shortened, columns = ['text'])
    df['n_tokens'] = n_tokens(df.text)

    df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])

    df.to_csv('data/processed/embeddings.csv')
    df.head()

createEmbeddings()