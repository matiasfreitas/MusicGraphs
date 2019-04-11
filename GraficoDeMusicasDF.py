import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter

LinkList = [ "https://www.letras.mus.br/ed-sheeran/"]

def request1MusicPage(link):
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except:
        print ("erro link: " + link)
        return ""
    
def requestMusic(content):
    music = content.find("div", class_="cnt-letra p402_premium")
    if music != None:
        music = content.find("div", class_="cnt-letra p402_premium").get_text
        music = str.lower(str(music))        
        music = music.replace("�", "") 
        music = music.lower()
        music = music.replace("<bound method tag.get_text of <article>", " ")
        music = music.replace("</article>>", " ")
        music = music.replace("<div", " ")
        music = music.replace("</div>", " ")
        music = music.replace("<h1>", " ")
        music = music.replace("<p>", " ")
        music = music.replace("</p>", " ")
        music = music.replace("<br>", " ")
        music = music.replace("<br/>", " ")
        music = music.replace("</br>", " ")
        music = music.replace(">", " ")
        music = music.replace("<", " ")
        music = music.replace("'", " ")
        music = music.replace('"', " ")
        music = music.replace('/', " ")
        music = music.replace("(", " ")
        music = music.replace(")", " ")
        music = music.replace("...", " ")
        music = music.replace("?", " ")
        music = music.replace(",", " ")
        music = music.replace(".", " ")
        music = music.replace("!", " ")
        music = music.replace('“', " ")
        music = music.replace('”', " ")
        music = music.replace("]", " ")
        music = music.replace("[", " ")
        music = music.replace("method", " ")
        music = music.replace("bound", " ")
        music = music.replace("tag", " ")
        music = music.replace("get_text", " ")
        music = music.replace("class=", " ")
        music = music.replace("cnt-letra", " ")
        music = music.replace("p402_premium", " ")
        
        


    else:
        music = ""
    return music

def requestAuthor(content):
    author = str(content.find(class_ ="cnt-head_title").find("h2").get_text)
    author = author.replace('/>', "")
    author = author.replace('/">', "")
    author = author.replace('</a> </h2>>', "")
    author = author.replace('<bound method Tag.get_text of <h2> <a href="/', '')
    author = author.replace('</h1>>', "")
    author = author.split(" ")
    author = author[1:]
    author = ' '.join(author)
    author = author[:-1]
    return author

def requestMusicName(content):
    musicName = str(content.find(class_ ="cnt-head_title").find("h1").get_text)
    musicName = musicName.replace('/>', "")
    musicName = musicName.replace('</a></h1>>', "")
    musicName = musicName.replace('<bound method Tag.get_text of <h1>', "")
    musicName = musicName.replace('</h1>>', "")
    return musicName

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
    listWord = stringMusic.split(" ")
    return Counter(listWord)



AllArtistUniqueWords = []
AllSingers = []
totalDicts= {}
for artistPage in LinkList:
    dfMusicsArtist = pd.DataFrame()
    totalListOfuniqueWord = []
    singerPage = request1SingerPage(artistPage)
    ListOfMusicSinger = findLinksSingerPage(singerPage)   
    MusicContent = request1MusicPage(ListOfMusicSinger[0])
    Singer = requestAuthor(MusicContent)
    Songs = []
    totalDicts = {}
    for link in ListOfMusicSinger:
        dfMusic =  pd.DataFrame()
        MusicContent = request1MusicPage(link)
        Music = requestMusic(MusicContent)
        musicName = requestMusicName(MusicContent)
        counterMusic = TreatmentMusic(Music)
        counterMusic = dict(counterMusic)
        Songs.append(musicName)
        for key in counterMusic:
            if key in totalDicts:
                totalDicts[key][musicName] = counterMusic[key]
            else:
                totalDicts[key] = {musicName:counterMusic[key]}     
    filename = Singer + ".csv"
    dfAllMusics = pd.DataFrame.from_dict(totalDicts)
    dfAllMusics.index.names = ['Songs']
    dfAllMusics.columns.names = ['Words']
    dfAllMusics = dfAllMusics.drop(columns="")
    dfAllMusics = dfAllMusics.fillna(0)
    print(dfAllMusics)
    dfAllMusics.to_csv(filename, encoding='utf_8')
### python GraficoDeMusicasDF.py version 0.9

