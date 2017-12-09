import re

text = ''

articles = re.split('\s*Art\.\s([0-9]{1,3}).\s*', text)[1:]
articles_dict = {}
for number, article in zip(articles[::2], articles[1::2]):
    articles_dict[number] = article.strip()
