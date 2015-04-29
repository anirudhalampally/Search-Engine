import sys,os
f=open('./please/file102.txt','r')
g=open('./sec/secindex.txt','wb')
lines=f.readlines()
pally=lines
h=open('./please/index.txt','wb')
prv=pally[0].split(":")[0]
out=pally[0][:-1]
for i in range(1,len(pally)):
    pally[i]=pally[i].replace('::',':')
    cur=pally[i].split(":")[0]
    if prv==cur:
        out+=pally[i].split(":")[1][:-1]
    else:
        out+='\n'
        h.write(bytes(out,'utf8'))
        out=pally[i][:-1]
    prv=pally[i].split(":")[0]
i=0
h.close()
lines=open('./please/index.txt','r')
lines=lines.readlines()
n = len(lines)
jump=int(n**(1.0/3.0))
jump=int(n/jump)
print (jump)
line=0
while True:
    if line>n:
        break
    name='./sec/'+str(i)+'.txt'
    i+=1
    f=open(name,'wb')
    k=line
    st=''
    name=lines[k].split(":")[0]+'|'+str(i)+'|'
    try:
        name+=lines[k+jump-1].split(":")[0]+'\n'
    except:
        name+=lines[n-1].split(":")[0]+'\n'
    g.write(bytes(name,'utf8'))
    k=0
    while k<jump and k+line<n:
        st+=lines[k+line]
        k+=1
    f.write(bytes(st,'utf8'))
    line+=jump

