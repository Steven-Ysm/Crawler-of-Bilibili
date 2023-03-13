from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import codecs

train = []

fp = codecs.open('D:\大学\毛泽东思想概论\\b站爬虫\第五次\LDA\第七集弹幕文本清洗.txt','r',encoding='utf8')
for line in fp:
    if line != '':
        line = line.split()
        train.append([w for w in line])

dictionary = corpora.Dictionary(train)

corpus = [dictionary.doc2bow(text) for text in train]

lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=2, passes=200)
# num_topics：主题数目
# passes：训练伦次
# num_words：每个主题下输出的term的数目

for topic in lda.print_topics(num_words = 10):
    termNumber = topic[0]
    print(topic[0], ':', sep='')
    listOfTerms = topic[1].split('+')
    for term in listOfTerms:
        listItems = term.split('*')
        print('  ', listItems[1], '(', listItems[0], ')', sep='')
