# coding=utf-8
"""
Módulo de Detecção e Analise de Sentimento.
https://pytorch.org/get-started/locally/
pip3 install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
"""
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np


class SentimentAnalysis:
    """ Classe para fazer a analise de sentimentos. """

    def __init__(self):
        # Instantiate Model
        self._tokenizer = AutoTokenizer.from_pretrained(
            'nlptown/bert-base-multilingual-uncased-sentiment')
        self._model = AutoModelForSequenceClassification.from_pretrained(
            'nlptown/bert-base-multilingual-uncased-sentiment')

    def calculate(self, text):
        """ Faz o cálculo do sentimento no texto informado. """
        # Encode and Calculate Sentiment
        tokens = self._tokenizer.encode(text, return_tensors='pt')
        # print(tokens)
        # print(tokenizer.decode(tokens[0]))
        result = self._model(tokens)
        return int(torch.argmax(result.logits)) + 1


if __name__ == '__main__':
    analyser = SentimentAnalysis()
    frases = [
        'I hated this, absolutely the worst',
        'This is amazing, I love it. GREAT!',
        'Meh, it was okay!',
        "It was good but could've been better. Great"
    ]
    for t in frases:
        print(t, analyser.calculate(t))

    # Collect Reviews
    r = requests.get('https://www.yelp.com/biz/mejico-sydney-2')
    soup = BeautifulSoup(r.text, 'html.parser')
    regex = re.compile('.*comment.*')
    results = soup.find_all('p', {'class': regex})
    reviews = [result.text for result in results]

    # Load Reviews into DataFrame and Score
    df = pd.DataFrame(np.array(reviews), columns=['review'])
    print(df)
    df['sentiment'] = df['review'].apply(lambda x: analyser.calculate(x[:512]))
    print(df)
