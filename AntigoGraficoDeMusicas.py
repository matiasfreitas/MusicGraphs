import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import cycle
forbiddenWordsPT = ["de" , "a" , "o" , "que" , "e" , "do" , "da" , "em" , "um" , "para" , "é" , "com" , "não" , "uma" , "os" , "no" , 
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

class Word:
    def __init__(self, word, valid, NArtist, nSongs, NOfRepetions):
        self.word = word
        self.valid = valid
        self.nArt = NArtist
        self.arrayArt = []
        self.nSongs = nSongs
        self.listNSongs = []
        self.nRepetions = NOfRepetions
        self.listRepetionsSong = []
        self.listRepetionSongArtists = []
        self.listRepetions = []

    def sumNRepetions(self):
        self.nRepetions += 1

    def sumSong(self,nSongsTotal):
        for song in range(len(self.listRepetionsSong),nSongsTotal-1):
            self.listRepetionsSong.append(0)
        self.listRepetionsSong.append(self.nRepetions)
        self.nSongs += 1
        self.nRepetions = 0

    def appendSong(self,nSongsTotal):
        for song in range(len(self.listRepetionsSong),nSongsTotal):
            self.listRepetionsSong.append(0)

    def sumArt(self,nArtist):
        for Artist in range(len(self.arrayArt),nArtist-1):
            self.arrayArt.append(0)
            self.listNSongs.append(0)
            self.listRepetionSongArtists.append([0])
            self.listRepetions.append(0)
        
        
        if self.listNSongs[nArtist-1]>0:
            self.arrayArt.append(1)
            self.listRepetionSongArtists.append(self.listRepetionsSong)
            
        else:
            self.arrayArt.append(0)
            self.listRepetionSongArtists.append([0])

        self.listRepetions.append(sum(self.listRepetionsSong))
        self.listNSongs.append(self.nSongs)
        self.listRepetionsSong = []
        self.nSongs = 0
        
        
            
    def validate(self):
        self.valid = 1
    
    def desvalidate(self):
        self.valid = 0

    def print(self):
        print(self.word)
        print(self.valid)
        print(self.arrayArt)
        print(self.listNSongs)
        print(self.listRepetions)
        print(self.listRepetionSongArtists)
        
        

def request1MusicPage(link):
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except:
        print ("erro link: " + link)
        return ""
    
def requestMusic(content):
    music = content.find('article')
    if music != None:
        music = content.find('article').get_text
        music = str(music)
        music = music.replace("�", "") 
        music = music.lower()
        music = music.replace("<bound method tag.get_text of <article>", " ")
        music = music.replace("</article>>", " ")
        music = music.replace("<p>", " ")
        music = music.replace("</p>", " ")
        music = music.replace("<br>", " ")
        music = music.replace("<br/>", " ")
        music = music.replace("</br>", " ")
        music = music.replace("'", " ")
        music = music.replace('"', " ")
        music = music.replace("(", " ")
        music = music.replace("', " ")", " ")
        music = music.replace("...", " ")
        music = music.replace("?", " ")
        music = music.replace(",", " ")
        music = music.replace(".", " ")
        music = music.replace("!", " ")
        music = music.replace('“', " ")
        music = music.replace('”', " ")
        music = [1, music]
    else:
        music = [0, ""]
    return music

def requestAuthor(content):
    author = str(content.find(class_ ="cnt-head_title").find("h2").get_text)
    author = author.split('/>')
    author = author[1]
    author = author.split('</a></h2>>')
    author = author[0]
    return author

def request1SingerPage(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def findLinksSingerPage(content):
    linkList = []
    linkString = str(content.find(class_="cnt-list--alp").get_text)
    linkList.append(linkString.split('<a href="'))
    linkString = []
    linkList = linkList[0]
    for x in range(0,len(linkList)):
        linkString.append(linkList[x].split('">'))
    linkList = []
    for x in range(0,len(linkString)):
        linkList.append(linkString[x][0])
        linkList[x] = "https://www.letras.mus.br" + linkList[x]
    linkString= []
    for x in range(0,len(linkList)):
        linkString.append(linkList[x].split('id="'))
        linkString[x] = linkString[x][0]
    linkList = []
    for x in range(0,len(linkString)):
        linkList.append(linkString[x].split('" '))
        linkList[x] = linkList[x][0] 
    del linkList[0]
    return linkList

def TreatmentMusic(stringMusic):
    uniqueListWord = []
    dictOfNumberRepetion = {}
    listWord = stringMusic.split(" ")
    for item in listWord:
        if item in dictOfNumberRepetion:
            dictOfNumberRepetion[item].sumNRepetions
            ### dictOfNumberRepetion[item] = [If is a Valid Word,N of  artists, Number of artists in array,number of songs, number of total repetions, list of number of total repetions for each artist]
        else:
            uniqueListWord.append(item)
            dictOfNumberRepetion[item] = Word(item, 1, 1, 0, 1)
    del uniqueListWord[0]
    return [uniqueListWord, dictOfNumberRepetion]

def takeSecond(elem):
    return elem[1]

def plotArtistGraphBubble(totalDict, ArtistDict,listofWords,NArtist, NAllArtists, ajustValue,totalArtist,color):
    for item in listofWords[NArtist]:
        if ArtistDict[NArtist][item][3] > ajustValue[NArtist] and ArtistDict[NArtist][item][0] :
            x = (totalDict[item][3] - ArtistDict[NArtist][item][3])/(NAllArtists - 1) 
            y = ArtistDict[NArtist][item][3]/totalArtist[NArtist][3]*5000
            plt.scatter(x, y, 
                        marker='o',
                        s = (ArtistDict[NArtist][item][2]*200*(40/ajustValue[NArtist]))**(1/2) ,
                        c = color[NArtist])
            plt.annotate(item,
                        xy=(x, y), 
                        xytext=(x-0.4, y-0.2),
                        bbox=dict(boxstyle='round',
                                    fc='white',
                                    alpha=0.1))

def plotArtistGraphBar(totalDict,listofWords, NAllArtists,totalArtist,color):
    count = 0
    width = 0.1
    ax = plt.subplot(111)
    for item in listofWords:
        height = []
        for singer in range(0,NAllArtists):
            print(totalDict[item].listRepetions[singer])
            height.append(totalDict[item].listRepetions[singer]/totalArtist[singer][3]*100) 

        x.bar(count, height,width=0.1, color=color,align='center',tick_label= item)
        count +=0.1

LinkList = [ "https://www.letras.mus.br/titas/", "https://www.letras.mus.br/cazuza/", "https://www.letras.mus.br/emicida/", "https://www.letras.mus.br/mallu-magalhaes/"]
AllArtistUniqueWords = []
AllAuthor = []
AllTotalArtist = []
TotalMusics = [0,0,0,0]
### totalMusic = [Number of Artists, Number of Unique Words, Number of Songs, Number of Words ]
color = ["yellow", "blue", "red", "green"]
allAjustValue = []
countArtist = 0
AllListUniqueWords = []
totalDicts= {}
for artistPage in LinkList:
    countArtist += 1
    totalListOfuniqueWord = []
    totalArtist =[0,0,0]
    singerPage = request1SingerPage(artistPage)
    ListOfMusicSinger = findLinksSingerPage(singerPage)   
    MusicContent = request1MusicPage(ListOfMusicSinger[0])
    Singer = requestAuthor(MusicContent)
    nSongs = 0
    ajustValue = []
    for link in ListOfMusicSinger:
        MusicContent = request1MusicPage(link)
        Music = requestMusic(MusicContent)
        if  Music[0] :
            nSongs += 1
        Music = Music[1]
        dictMusic = TreatmentMusic(Music)
        listOfUniqueWord = dictMusic[0]
        dictMusic = dictMusic[1]
        for item in listOfUniqueWord:
            totalListOfuniqueWord.append(item)
            dictMusic[item].sumSong(nSongs)
            totalDicts[item] = dictMusic[item]
    totalWords = len(totalListOfuniqueWord)
    totalListOfuniqueWord = set(totalListOfuniqueWord)
    totalListOfuniqueWord = list(totalListOfuniqueWord)
    for item in totalListOfuniqueWord:
        totalDicts[item].appendSong(nSongs)
        totalDicts[item].sumArt(countArtist)
        AllArtistUniqueWords.append(item)
        if totalDicts[item].valid == 1 and totalDicts[item].arrayArt[countArtist-1] == 1:
            ajustValue.append(totalDicts[item].listRepetions[countArtist-1])
            totalArtist = [totalArtist[0] + 1, nSongs, totalWords]
            ### totalArtist = [Number of Unique Words, Number of Songs, Number of Words ]
    print(totalArtist)
    AllArtistUniqueWords = set(AllArtistUniqueWords)
    AllArtistUniqueWords = list(AllArtistUniqueWords) 
    ajustValue = sorted(ajustValue)
    ajustValue = ajustValue[-25]
    AllTotalArtist.append(totalArtist)
    AllAuthor.append(Singer)
    AllListUniqueWords.append(totalListOfuniqueWord)
    allAjustValue.append(ajustValue)
    TotalMusics = [countArtist, len(AllArtistUniqueWords), TotalMusics[2] + nSongs, TotalMusics[3] + totalArtist[2]]
        ### totalMusic = [Number of Artists, Number of Unique Words, Number of Songs, Number of Words ]
    
    print(TotalMusics)
for item in forbiddenWordsPT:
    if item in totalDicts:
        totalDicts[item].desvalidate()

for item in AllArtistUniqueWords:
    totalDicts[item].sumArt(countArtist)
    totalDicts[item].print()

plotArtistGraphBar(totalDicts, AllListUniqueWords, TotalMusics[0],AllTotalArtist,color)

# for NArtist in range(0,TotalMusics[0]):
#     plotArtistGraphBubble(SumAllDicts, AllDicts, AllListUniqueWords, NArtist,TotalMusics[0], allAjustValue,AllTotalArtist, color)
plt.title("Léxico:Palavras Cantadas de %s, %s, %s e %s" %(AllAuthor[0],AllAuthor[1],AllAuthor[2],AllAuthor[3]))
plt.savefig('Palavras cantadas.jpeg', bbox_inches='tight', format='jpeg', dpi=1200)
plt.clf()
     
 

### python GraficoDeMUsicas.py version 0.5

