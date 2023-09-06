from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import spacy

# session = HTMLSession()
# url = 'https://sg.finance.yahoo.com/'

# r = session.get(url)

# r.html.render(sleep=1, scrolldown=3)

# articles = r.html.find("js-content-viewer Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) not-isInStreamVideoEnabled wafer-destroyed")

# print(articles)

session = HTMLSession()
url = 'https://finance.yahoo.com/news'

r = session.get(url)
print(r.status_code)

r.html.render(sleep=1, scrolldown=10)


# page = requests.get(url)

soup = BeautifulSoup(r.html.html, 'html.parser')
articles = soup.find_all(id='Main')
for article in articles:
    print(article.text)
print(len(articles))

# Load English tokenizer, tagger, parser and NER
# nlp = spacy.load("en_core_web_sm")

# Process whole documents
# text = articles
# doc = nlp(text)

# Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)