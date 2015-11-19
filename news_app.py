# minimal example from:
# http://flask.pocoo.org/docs/quickstart/

import flask
from glob import glob
import json
from newspaper import Article

app = flask.Flask(__name__)

def sum_sentiments(data):
    sent = 0
    for d in data:
        sent += d["sentiment"]
    return sent/len(data)

def clean_text(text):
    removed = text.replace("\n\n", " ")
    clean = filter(lambda x: x in string.printable, removed)
    return "".join(l for l in clean if l not in string.punctuation.replace(".",""))

def tokenize_text(text):
    sents = sent_tokenize(text)
    return [sent for sent in sents if len(sent.split()) >= 5]

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
# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("news.html", 'r') as viz_file:
        return viz_file.read()

@app.route('/ranking', methods=["POST"])
def ranking():
	files = glob('temp/*.json')
	sent_list = []
	for fname in files:
		with open(fname) as data_file:
			data = json.load(data_file)
    		sent = sum_sentiments(data)
    		sent_list.append((fname, sent))
	sents = sorted(sent_list, key=lambda x: x[1])
	ranking = []
	for i, x in enumerate(sents):
		text = x[0].replace('_articles.json', '').replace('temp/', '').replace('_', ' ')
		ranking.append(text)
	results = {"ranking": ranking}
	return flask.jsonify(results)

@app.route('/articles', methods=["POST"])
def article_sentiment():
    print "test"
    data = flask.request.json
    print data
    url = data["example"]
    a = Article(url)
    a.download()
    a.parse()
    text = process_text(a.text)
    results = {"sentiment": objectivity_sentiment(text)}
    return flask.jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
