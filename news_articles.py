import newspaper
import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from textblob import TextBlob
import json
from pymongo import MongoClient

def clean_text(text):
	removed = text.replace("\n\n", " ")
	clean = filter(lambda x: x in string.printable, removed)
	return "".join(l for l in clean if l not in string.punctuation.replace(".",""))

def tokenize_text(text):
	sents = sent_tokenize(text)
	return sents

def objectivity_sentiment(text):
	sentiments = []
	for sent in text:
		sentiments.append(TextBlob(sent).sentiment[1])
	if len(sentiments) == 0:
		return []
	else:
		return sum(sentiments) / float(len(sentiments))

def process_text(text):
	clean = clean_text(text)
	tokens = tokenize_text(clean)
	return tokens

def get_articles(name, url):
	paper = newspaper.build(url, memoize_articles=False)
	print "Newspaper is finished building, number of articles: ", paper.size()
	article_list = []
	for article in paper.articles:
		art = {}
		article.download()
		article.parse()
		text = process_text(article.text)
		title = clean_text(article.title)
		if len(text) > 5:
			art["title"] = title
			art["authors"] = article.authors
			art["text"] = text
			art["sentiment"] = objectivity_sentiment(text)
			article_list.append(art)

	filename = name + '_articles.json'
	with open(filename, 'w') as fp:
		json.dump(article_list, fp, indent=4, sort_keys=True)
	return

#client = MongoClient()

news_df = pd.read_csv("news_articles2.csv")

names = news_df['outlet'].tolist()
urls = news_df['url'].tolist()
for n, u in zip(names,urls):
	print "Getting Articles for:", n
	get_articles(n,u)
	#db = client.news_outlets
	#source = db[n]
	#for article in articles:
	#	source.save(article)


