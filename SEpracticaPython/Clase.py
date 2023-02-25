import urllib.request
import re
import nltk
from inscriptis import get_text
from nltk import word_tokenize, sent_tokenize
from googletrans import Translator

translator = Translator()

#nltk.download()

cadena = """Cristiano Ronaldo dos Santos Aveiro GOIH ComM, born 5 February 1985) is a Portuguese professional footballer
who plays as a forward for and captains both Saudi Professional League club Al Nassr and the Portugal national team. Widely regarded as one of the greatest players of all time, 
Ronaldo has won five Ballon d'Or awards[note 3] and four European Golden Shoes, the most by a European player. He has won 34 trophies in his career, including seven league titles, 
five UEFA Champions Leagues, the UEFA European Championship and the UEFA Nations League. Ronaldo holds the records for most appearances (183), goals (140), and assists (42) 
in the Champions League, goals in the European Championship (14), international goals (118), and joint-most international appearances (196). He is one of the few players
to have made over 1,100 professional career appearances, and has scored over 820 official senior career goals for club and country. 
Ronaldo began his senior career with Sporting CP, before signing with Manchester United in 2003, winning the FA Cup in his first season. He would also go on to win three consecutive 
Premier League titles, the Champions League and the FIFA Club World Cup; at age 23, he won his first Ballon d'Or. Ronaldo was the subject of the then-most expensive association 
football transfer when he signed for Real Madrid in 2009 in a transfer worth €94 million (£80 million). He became a key contributor and formed an attacking trio with 
Karim Benzema and Gareth Bale which was integral to the team winning four Champions League wins from 2014 to 2018, including La Décima. During this period, he won back-to-back
Ballons d'Or in 2013 and 2014, and again in 2016 and 2017, and was runner-up three times behind Lionel Messi, his perceived career rival. He also became the club's all-time top 
goalscorer and the all-time top scorer in the Champions League, and finished as the competition's top scorer for six consecutive seasons between 2012 and 2018. With Real,
Ronaldo won two La Liga titles, two Copa del Rey, four Champions Leagues, three UEFA Super Cup and three Club World Cups. In 2018, he signed for Juventus in a transfer worth 
an initial €100 million (£88 million), the most expensive transfer for an Italian club and for a player over 30 years old. He won two Serie A titles, two Supercoppa Italiana 
trophies and a Coppa Italia, became the inaugural Serie A Most Valuable Player and the first footballer to finish as top scorer in the English, Spanish and Italian leagues, 
before returning to Manchester United in 2021. He left in 2022, after his contract with the club was terminated. In 2023, Ronaldo signed for Al Nassr. 
"""
#enlace = "https://es.wikipedia.org/wiki/Python"
#html = urllib.request.urlopen(enlace).read().decode('utf-8')
text = get_text(cadena)

print("############################################")

#Removing square brackets and extra spaces
formatted_article_text = re.sub('[^a-zA-z]', ' ', text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(text)
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

#CALCULA LA FRASE QUE MAS SE REPITE
sentence_scores ={}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 40:
                if sent not in  sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#REALIZA EL RESUMEN CON LAS MEJORES FRASES
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)

summary = translator.translate(summary, dest='es').text
print(summary)