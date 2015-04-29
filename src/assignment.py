import xml.sax
import re
import nltk
from nltk.stem import PorterStemmer
import os
import sys
import collections
postinglist={}
stop=[]
path=os.getcwd()
f1=open(path+'/stoplist.txt','r') 
for i in f1:
    if i!='\n':
        stop.append(i)
stoplist1=[]
for i in stop:
    i=i[:-1]
    stoplist1.append(i)
stoplist={}
for i in stoplist1:
    stoplist[i]=1
fc=0
def merge(file1,file2,out_file):
    print (file1,file2)
    with open(file1,'r+') as f1, open(file2,'r+') as f2:
        sources = [f1,f2]
        with open(out_file, "wb") as dest:
            l1 = f1.readline()
            l2 = f2.readline()
            s1 = l1.split()
            s2 = l2.split()
            while(1):
                try:
                    aa=s1[0][0]
                except:
                    return
                try:
                    aa=s2[0][0]
                except:
                    return
                if(s1[0] < s2[0]):
                    dest.write(bytes(l1,'utf8'))
                    try:
                        l1 = f1.readline()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.readline()
                                dest.write(bytes(t2,'utf8'))
                            except:
                                break
                        break
                elif(s1[0] > s2[0]):
                    dest.write(bytes(l2,'utf8'))
                    try:
                        l2 = f2.readline()
                        s2 = l2.split()
                    except:
                        while(1):
                            try:
                                t1 = f1.readline()
                                dest.write(bytes(t1,'utf8'))
                            except:
                                break
                        break
                else:
                    line = s1[0] +':' + s1[1] +'|'+ s2[1]
            #if(s1[0] == '0.0'):
            #    print line
                    dest.write(bytes(line + '\n','utf8'))
                    try:
                        l1 = f1.readline()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.readline()
                                dest.write(bytes(t2,'utf8'))
                            except:
                                break
                        break
                    try:
                        l2 = f2.readline()
                        s2 = l2.split()
                    except:
                        dest.write(bytes(l1,'utf8'))
                        while(1):
                            try:
                                t1 = f1.readline()
                                dest.write(bytes(t1,'utf8'))
                            except:
                                break
                        break

def parse(title,text,id):
    text=text.lower()
    text=text.replace('\n',' ').replace('+',' ').replace('-',' ').replace('"',' ').replace('#',' ').replace('%',' ').replace('@',' ').replace('$',' ').replace('!',' ').replace('-',' ').replace("\\"," ").replace('/',' ').replace('+',' ').replace('-',' ')
    text=text.replace('`',' ')
    text=' '.join(text.split())
    h, s, t=text.partition('external links')
    h, s, t=t.partition('Category')
    external=re.findall('\* \[http.*?www\.(.*?)\]',h)
    external=' '.join(external)
    external=external.replace('*',' ').replace('(',' ').replace(')',' ').replace("'",' ').replace('&',' ').replace('-',' ').replace('{{',' ').replace('}}',' ').replace('.',' ').replace('com',' ').replace('org',' ').replace('html',' ').replace('/',' ').replace(',',' ').replace('_',' ').replace(':',' ').replace('=',' ').replace('%',' ').replace('~',' ')
    external=' '.join(external.split())
    try:
        categories=re.findall('\[\[category:(.*?)\]\]',text)
        categories=' '.join(categories)
        categories=categories.replace('*',' ').replace('(',' ').replace(')',' ').replace("'",' ').replace('&',' ').replace('-',' ').replace('{{',' ').replace('}}',' ').replace('.',' ').replace('com',' ').replace('org',' ').replace('html',' ').replace('/',' ').replace(',',' ').replace('_',' ').replace(':',' ').replace('=',' ').replace('%',' ').replace('~',' ').replace('|','')
        text=re.sub('\[\[category:(.*?)\]\]','',text)
    except:
        pass
    text=text.replace('[[',' ').replace(']]',' ').replace('.',' ').replace(',',' ').replace('?',' ').replace('!',' ').replace('%',' ').replace('/',' ').replace('&quot;',' ').replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace(':',' ').replace('reflist','').replace('&',' ')
    text=re.sub('<(.*?)>','',text)
    ref=''
    pupu=''
    pooh=''
    references=''
    try:
        text1=text
        hj,kj,pupu=text1.partition("references")
        if len(pupu)>3:
            pooh=pupu
            pooh=pooh.replace('*',' ').replace('(',' ').replace(')',' ').replace("'",' ').replace('&',' ').replace('-',' ').replace('{{',' ').replace('}}',' ')
            m=re.findall('\|.*?[=](.*?)\|',pooh)
            for i in range(len(m)):
                if len(m)<4:
                    m.remove(i)
            m=' '.join(m)
            if len(m)<3:
                m=pooh
            m=m.replace('|',' ').replace('>',' ').replace('"',' ').replace("'",' ').replace('#',' ').replace('[',' ').replace(']',' ').replace('=',' ').replace(';',' ').replace('-',' ').replace('_',' ').replace('{',' ').replace('}',' ').replace(',',' ').replace('&',' ')
            m=' '.join(m.split())
            ref=m
            references=m
    except:
        pupu=''
        ref=''
        references=''
    head, sep, tail = text.partition("references")
    info, sep, body = head.partition("'''")
    body=body.replace('|',' ').replace('>',' ').replace('"',' ').replace("'",' ').replace('#',' ').replace('[',' ').replace(']',' ').replace('=',' ').replace(';',' ').replace('-',' ').replace('_',' ').replace('{',' ').replace('}',' ').replace(',',' ').replace('(',' ').replace(')',' ').replace('$',' ').replace('*',' ').replace('null&',' ').replace("’",' ').replace('“',' ').replace(':',' ').replace('-',' ')
    body=' '.join(body.split())
    m=re.findall('=(.*?)\|',info)
    m=' '.join(m)
    m=m.replace('|',' ').replace('>',' ').replace('"',' ').replace("'",' ').replace('#',' ').replace('[',' ').replace(']',' ').replace('=',' ').replace(';',' ').replace('-',' ').replace('_',' ').replace('{',' ').replace('}',' ').replace(',',' ').replace('(',' ').replace(')',' ').replace('$',' ').replace('*',' ').replace('&',' ')
    m=' '.join(m.split())
    title=title.replace('|',' ').replace('>',' ').replace('"',' ').replace("'",' ').replace('#',' ').replace('[',' ').replace(']',' ').replace('=',' ').replace(';',' ').replace('-',' ').replace('_',' ').replace('{',' ').replace('}',' ').replace(',',' ').replace('(',' ').replace(')',' ').replace('$',' ').replace('*',' ').replace(':',' ').replace('&',' ')
    title=' '.join(title.split())
    #-------------------------------------------------------------
    infobox=m
    categories=categories
    references=references
    body=body
    title=title
    external=external
    #-------------------------------------------------------------
    title=title.lower()
    title=title.split()
    infobox=infobox.split()
    body=body.split()
    references=references.split()
    categories=categories.split()
    external=external.split()
    title1=[]
    infobox1=[]
    body1=[]
    references1=[]
    categories1=[]
    external1=[]
    stemmer=PorterStemmer()
    for i in title:
        if i in stoplist:
            pass
        else:
            title1.append(stemmer.stem(i))
    for i in infobox:
        if i in stoplist:
            pass
        else:
            infobox1.append(stemmer.stem(i))
    for i in body:
        if i in stoplist:
            pass
        else:
            body1.append(stemmer.stem(i))
    for i in references:
        if i in stoplist:
            pass
        else:
            references1.append(stemmer.stem(i))
    for i in categories:
        if i in stoplist:
            pass
        else:
            categories1.append(stemmer.stem(i))
    for i in external:
        if i in stoplist:
            pass
        else:
            external1.append(stemmer.stem(i))
    title2={}
    for i in title1:
        if i in title2:
            title2[i]+=1
        else:
            title2[i]=1
    infobox2={}
    for i in infobox1:
        if i in infobox2:
            infobox2[i]+=1
        else:
            infobox2[i]=1
    body2={}
    for i in body1:
        if i in body2:
            body2[i]+=1
        else:
            body2[i]=1
    references2={}
    for i in references1:
        if i in references2:
            references2[i]+=1
        else:
            references2[i]=1
    categories2={}
    for i in categories1:
        if i in categories2:
            categories2[i]+=1
        else:
            categories2[i]=1
    external2={}
    for i in external1:
        if i in external2:
            external2[i]+=1
        else:
            external2[i]=1
    posting={}
    for i in title2:
        if i not in posting:
            posting[i]=str(id)+'-'+str('t')+str(title2[i])
        else:
            posting[i]+='|'+str('t')+str(title2[i])
    for i in infobox2:
        if i not in posting:
            posting[i]=str(id)+'-'+'i'+str(infobox2[i])
        else:
            co = 0
            try:
                a=title2[i]
            except:
                co+=1
                pass
            if co >= 1:
                posting[i]+='i'+str(infobox2[i])
            else :
                posting[i]+='|'+'i'+str(infobox2[i])
    for i in body2:
        if i not in posting:
            posting[i]=str(id)+'-'+str('b')+str(body2[i])
        else:
            co = 0
            try:
                a=title2[i]
            except:
                co+=1
                pass
            try :
                a=infobox2[i]
            except:
                co+=1
                pass
            if co >= 1:
                posting[i]+=str('b')+str(body2[i])
            else :
                posting[i]+='|'+str('b')+str(body2[i])
    for i in references2:
        if i not in posting:
            posting[i]=str(id)+'-'+str('r')+str(references2[i])
        else:
            co = 0
            try:
                a=title2[i]
            except:
                co+=1
                pass
            try :
                a=infobox2[i]
            except:
                co+=1
                pass
            try :
                a=body2[i]
            except:
                co+=1
                pass
            if co >= 1:
                posting[i]+=str('r')+str(references2[i])
            else :
                posting[i]+='|'+str('r')+str(references2[i])
    for i in categories2:
        if i not in posting:
            posting[i]=str(id)+'-'+str('c')+str(categories2[i])
        else:
            co = 0
            try:
                a=title2[i]
            except:
                co+=1
                pass
            try :
                a=infobox2[i]
            except:
                co+=1
                pass
            try :
                a=body2[i]
            except:
                co+=1
                pass
            try :
                a=reference2[i]
            except:
                co+=1
                pass
            if co >= 1:
                posting[i]+=str('c')+str(categories2[i])
            else :
                posting[i]+='|'+str('c')+str(categories2[i])
    for i in external2:
        if i not in posting:
            posting[i]=str(id)+'-'+str('e')+str(external2[i])
        else:
            co = 0
            try:
                a=title2[i]
            except:
                co+=1
                pass
            try :
                a=infobox2[i]
            except:
                co+=1
                pass
            try :
                a=body2[i]
            except:
                co+=1
                pass
            try :
                a=reference2[i]
            except:
                co+=1
                pass
            try :
                a=categories2[i]
            except:
                co+=1
                pass
            if co >= 1:
                posting[i]+=str('e')+str(external2[i])
            else :
                posting[i]+='|'+str('e')+str(external2[i])
    for i in posting:
        if i not in postinglist:
            postinglist[i]=posting[i]
        else:
            postinglist[i]+='|'+posting[i]



class ABContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.title=''
        self.id=0
        self.text=''
        self.type=''
        self.fc=0

    def startElement(self, name, attrs):
        if name=='title':
            self.type='title'
            self.id+=1
        elif name=='text':
            self.type='text'
            self.text=''
        else:
            self.type='nn'

    def characters(self, content):
        if self.type=='title':
            self.title=content
            self.text=''
        elif self.type=='text':
            self.text+=content
        else:
            pass

    def endElement(self, name):
        if self.type=='title':
            pass
        elif self.type=='text':
            if self.text!='':
                parse(self.title,self.text,self.id)
            self.text=''
        else:
            pass
        global postinglist
        global fc 
        if(sys.getsizeof(postinglist)>1000000):
            postinglist=collections.OrderedDict(sorted(postinglist.items()))
            name="./please/file"+str(fc)+".txt"
            t=open(name,'w')
            for j in postinglist:
                st=j+": "+postinglist[j]+"\n"
                t.write(st)
            postinglist={}
            fc+=1
        self.type=''





def main(sourceFileName):
    source = open(sourceFileName)
    xml.sax.parse(source, ABContentHandler())
    #for i in postinglist:
    #    print (i,postinglist[i])

if __name__ == "__main__":
    main("evaluate.xml")
    i=0
    if(sys.getsizeof(postinglist)<1000000):
        postinglist=collections.OrderedDict(sorted(postinglist.items()))
        name="./please/file"+str(fc)+".txt"
        t=open(name,'w')
        for j in postinglist:
            st=j+": "+postinglist[j]+"\n"
            t.write(st)
        postinglist={}
        fc+=1

    while(i<fc-1):
        f1="./please/file"+str(i)+".txt"
        f2="./please/file"+str(i+1)+".txt"
        o1="./please/file"+str(fc)+".txt"
        fc+=1
        merge(f1,f2,o1)
        i+=2
