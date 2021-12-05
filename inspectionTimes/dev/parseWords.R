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

type=rep(0:2,c(nNW,nP,nN))
all=c(nonword,pos,neg)
out=cbind(all,type)
write.table(file='allV1.txt',out,
            row.names = F,
            quote=F,
            col.names =F)