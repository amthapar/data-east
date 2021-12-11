library(stringr)
a <- read.csv('wordsV1.csv',head=T)
neg=str_trim(a[1:324,1])
write.table(file='negV1.txt',neg,
            row.names = F,
            quote=F,
            col.names =F)
pos=str_trim(a[1:322,2])
write.table(file='posV1.txt',pos,
            row.names = F,
            quote=F,
            col.names =F)

allW=c(pos,neg)
nonword=allW
wordLen=nchar(allW)
letF=table(unlist(strsplit(allW,"")))
letP=letF/sum(letF)

for (i in 1:length(allW)){
  nonLets=sample(x=letters,
                 size=wordLen[i],
                 replace=T,
                 prob=letP)
  nonword[i]=paste(nonLets,collapse='')}

write.table(file='nonV1.txt',nonword,
            row.names = F,
            quote=F,
            col.names =F)

nP=length(pos)
nN=length(neg)
nNW=length(nonword)

type=rep(0:1,c(nNW,nP+nN))
valence=rep(c(0,1,0,1),c(nNW/2,nNW/2,nP,nN))
all=c(nonword,pos,neg)
itemNum=(1:length(all))-1
out=cbind(itemNum,all,type,valence)
colnames(out)=c("itemNum","item","type","valence")
write.table(file='allV1.txt',out,
            row.names = F,
            quote=F,
            col.names =T,
            sep=',')

