#Cody McMahon
#2/5/16
#TCSS 480 ASSIGNMENT 5

#about "test file"
#
#I'm really not sure what i should have done for the test file my program should never crash,
#crawl into any sites a normal mozilla browser could, skip broken links, and add all words it
#finds to the dictionary and not crash if the link has none. But i don't know how to know if 
#I am gathering every possible link and not gather any that I shouldn't.

#imports
#from wordcloud import WordCloud (if only)
from urllib.request import Request, urlopen
from tkinter import *
import urllib.error
import re
import operator



#"constants"
FILENAME = "urls.txt"
TIMES_TO_PROCESS = 100

#the node class that holds the urls
class Node:
    #used to see how many nodes already exist
    nodeNum = 0
    maxNodeToProcess = TIMES_TO_PROCESS
    
    def __init__(this,s):
        #fields
        this.url = s
        this.words = []
        this.kids = []
        
        #tells whether or not this is a url that should be processed
        if Node.nodeNum < Node.maxNodeToProcess:
            this.process = 1
        else:
            this.process = 0
        Node.nodeNum += 1

    #adds a word to the node
    def addWord(this,s):
        this.words.append(s)
    #adds children to the node
    def addKid(this,n):
        this.kids.append(n)

#used to not list duplicate children
def addKid(url, node):
    for kid in url.kids:
        if kid.url in node.url:
            return            
    url.addKid(node)

#checks the specific url
def searchurl(urlQueue, url):
    #print statement to show that the file is actually running
    print("|", sep = "", end = "")
    #pretend to be using firefox so websites dont block me for thinking im a web crawler
    req = Request(url.url, headers={'User-Agent': 'Mozilla/5.0'})
    #if the url blows up leave the function and get the next one
    try:
        instream = urlopen(req)
    except :
        return
    
    for line in instream:
        #current regular expression to find the full link
        data = re.findall(r"<a\shref\s?=\s?\"http[^>]*?>[\w\s]*?</a>",str(line))
        #different regular expressions i tried
        #1- "<a href ?= ?\"http[^>]*>[\w\s]*</a>"
        #2- "<a\shref\s?=\s?\"https?://[^\"]*\">[\w\s]*</a>"
        #3- s?://[\d\w\s./%-]*\">[]*</a>
        #example link to look at <a href = "http://www.domain.com/folder1/folder1a/pagename.html" en>Some text</a>
        #for text in data:
        if data != []:
            for string in data:
                #parses the link part
                s = re.findall("https?://[^\"]*", string)[0]
                #print ("link is", s)
                node = getNode(urlQueue, s)
                addKid(url, node)
                #parses the words part
                words = re.findall("\">([\w\s]*)</a>",string)
                #skips rid of "Nones"
                if words is None:
                    continue
                #skips empty lists
                if words is []:
                    continue
                #splits the string into small words
                word = re.findall("\w*",str(words))
                #itterate through words
                for w in word:
                    #dont include empty strings into dictionary
                    if w in '':
                        continue
                    #only adds the word to dictionary if it gets this far
                    node.addWord(w.lower())

    
#checks if the child node needs to be created or can be pulled from the main queue
def getNode(urlQueue, url):
    for node in urlQueue:
        if node.url in url:
            return node
    newNode = Node(url)
    urlQueue.append(newNode)
    return newNode

#takes all the words out of the nodes and puts them into a master dictionary and sorts the dictionary so it can be displayed
def doWordThings(urlQueue):
    dic = {}
    file = open("CODY_MCMAHONS_CSV_FILE.csv", "w")
    print("Page, Links",file = file)
    #look at all urls that have been proccessed and their kids and print them to a csv file
    for i in range(0,TIMES_TO_PROCESS):
        print(urlQueue[i].url,end= " , ",file = file)
        for kid in urlQueue[i].kids:
            print(kid.url, end = " | ",file = file)
        print(file = file)
        
        if urlQueue[i] is urlQueue[-1]:
            break
    #look at ALL urls and the words attactched to them
    for url in urlQueue:
        for word in url.words:
            if word in dic:
                dic[word] = dic[word]+1
            else:
                dic[word] = 1
    newDic = sorted(dic.items(), key=operator.itemgetter(1))
    return newDic

#display the dictionary in console and in GUI format
def displayDictionary(dic):
    window = Tk()
    window.title("wordcloud")
    wordcloudtext = ""
    for i in reversed(range(-15,0)):
        print(dic[i])
        #words for the word map
        Label(text=dic[i][0],height = 1 ,width = (16 + i) * 3, font = font.Font(family="Helvetica", size=2*(16+i))).pack()
    
    #program basically ends on the loop for the gui
    window.mainloop()
    



#where the program starts
def main():
    urlQueue = []
    file = open(FILENAME, 'r')
    for line in file:
        data = str(line)
        #does a regular expression so these have the exact same syntax as the others
        s = re.findall("https?://[^\s]*", data)[0]
        getNode(urlQueue, s)#these nodes have no parents
    print("scowering the web for links[",sep = "", end = "")
    for url in urlQueue:
        #print(url.url)
        if url.process:
            searchurl(urlQueue, url)
        else:
            break
    print("]done")
    dic = doWordThings(urlQueue)
    displayDictionary(dic)


if __name__ == "__main__":
    main()
    
