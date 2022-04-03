mycol=c("darkblue","darkred","darkgreen")


dat <- read.csv('it2Sub7.dat',head=F)
colnames(dat) <-c('sub','blk','trl','word',
                  'hasR','val','wordNo',
                  'dur','bright','nes',
                  'resp','rt','acc')
acc= as.integer(as.factor(dat$acc))

if (length(unique(dat$sub>1))) print("Error: More Than One Subject Detected")


tot=1:length(dat$sub)
plot(tot,dat$dur,pch=19,col=mycol[dat$val],cex=1.1,typ='b')

########

fname=system("ls -1 it2S*",intern=T)
dat=NULL
for (i in fname) dat=rbind(dat,read.csv(i,head=F))
colnames(dat) <-c('sub','blk','trl','word',
                  'hasR','val','wordNo',
                  'dur','bright','nes',
                  'resp','rt','acc')
acc= as.integer(as.factor(dat$acc))

datA=dat[dat$blk>0,]
datB=tapply(datA$dur,list(datA$sub,datA$val),mean)
datC=as.data.frame.table(datB)
colnames(datC)=c("sub","val","dur")
summary(aov(dur~val+Error(sub),data=datC))

o=order(datB[,1])
matplot(datB[o,],typ='l',col=mycol,lwd=2,lty=1)
apply(datB,2,mean)

library(BayesFactor)
anovaBF(dur~val*sub,data=datC,whichRandom="sub")
