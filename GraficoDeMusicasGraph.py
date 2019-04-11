import pandas as pd
import numpy as np
import scipy as sp
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *

StopWordsPT = ["de" , "a" , "o" , "que" , "e" , "do" , "da" , "em" , "um" , "para" , "é" , "com" , "não" , "uma" , "os" , "no" , 
                    "se" , "na" , "por" , "mais" , "as" , "dos" , "como" , "mas" , "foi" , "ao" , "ele" , "das" , "tem" , "à" , "seu" , 
                    "sua" , "ou" , "ser" , "quando" , "muito" , "há" , "nos" , "já" , "está" , "eu" , "também" , "só" , "pelo" , "pela" , 
                    "até" , "isso" , "ela" , "entre" , "era" , "depois" , "sem" , "mesmo" , "aos" , "ter" , "seus" , "quem" , "nas" , 
                    "me" , "esse" , "eles" , "estão" , "você" , "tinha" , "foram" , "essa" , "num" , "nem" , "suas" , "meu" , "às" , "minha" , 
                    "têm" , "numa" , "pelos" , "elas" , "havia" , "seja" , "qual" , "será" , "nós" , "tenho" , "lhe" , "deles" , "essas" , 
                    "esses" , "pelas" , "este" , "fosse" , "dele" , "tu" , "te" , "vocês" , "vos" , "lhes" , "meus" , "minhas", "teu" , 
                    "tua" , "teus" , "tuas" , "nosso" , "nossa" , "nossos" , "nossas" , "dela" , "delas" , "esta" , "estes" , "estas", 
                    "aquele" , "aquela" , "aqueles" , "aquelas" , "isto" , "aquilo", "estou" , "está" , "estamos" , "estão" , "estive" , "esteve",
                    "estivemos" , "estiveram" , "estava" , "estávamos" , "estavam" , "estivera" , "estivéramos" , "esteja" , "estejamos" , "estejam",
                    "estivesse" , "estivéssemos" , "estivessem" , "estiver" , "estivermos" , "estiverem" , "hei" , "há" , "havemos" , "hão" , "houve",
                    "houvemos" , "houveram" , "houvera" , "houvéramos" , "haja" , "hajamos" , "hajam" , "houvesse" , "houvéssemos" , "houvessem",
                    "houver" , "houvermos" , "houverem" , "houverei" , "houverá" , "houveremos" , "houverão" , "houveria" , "houveríamos" , "houveriam",
                    "sou" , "somos" , "são" , "era" , "éramos" , "eram" , "fui" , "foi" , "fomos" , "foram" , "fora" , "fôramos" , "seja" , "sejamos" , "sejam" , "fosse",
                    "fôssemos" , "fossem" , "for" , "formos" , "forem" , "serei" , "será" , "seremos" , "serão" , "seria" , "seríamos" , "seriam" , "tenho",
                    "tem" , "temos" , "tém" , "tinha" , "tínhamos" , "tinham" , "tive" , "teve" , "tivemos" , "tiveram" , "tivera" , "tivéramos" , "tenha",
                    "tenhamos" , "tenham" , "tivesse" , "tivéssemos" , "tivessem" , "tiver" , "tivermos" , "tiverem" , "terei" , "terá" , "teremos",
                    "terão" , "teria" , "teríamos" , "teriam", "tô", "pro", "pra" ]

StopWordsEN = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your',
                'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', 
                "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
                'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
                'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 
                'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 
                'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 
                'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 
                "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 
                'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', 
                "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', 
                "weren't", 'won', "won't", 'wouldn', "wouldn't"]

CsvName = "Michael Jackson.csv"
HtmlName = "Michael Jackson Words Frequencies.html"
color = ["yellow", "blue", "red", "green"]
data = pd.read_csv(CsvName, encoding='utf_8', engine='python',
                    index_col=["Songs"]) 


data = data.reindex(data.sum().sort_values().index, axis=1)
data = data.iloc[:, ::-1]
for word in StopWordsEN:
  try:
    data = data.drop(columns=word)
  except:
    pass

AxisY = []
for column in data.columns:
    if data[column].sum()>0:
        AxisY.append(data[column].sum())


print(AxisY)




trace1 = {
    "y": AxisY,
    "x":[word for word in range(0,len(data.columns))],
    "line": {"shape": "linear"}, 
    "marker": {"color": "rgb(164,194,244)"}, 
    "mode": "lines+markers", 
    "text": [column for column in data.columns],
    "type": "scatter"
}


data = Data([trace1])
layout = {
  "title": "Words Frequencies in Michael Jackson Songs", 
  "xaxis": {
    "showgrid": False, 
    "title": "Words"
  }, 
  "yaxis": {
    "showline": False, 
    "title": "Frequency"
  }
}
fig = Figure(data=data, layout=layout)

plot(fig, filename= HtmlName)

### python GraficoDeMusicasGraph.py version 0.5

