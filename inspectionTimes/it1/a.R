mycol=c("red","darkgreen")
mypch=c(17,19)
mycex=c(1,1.3)

dat <- read.csv('it1Sub4.dat',head=F)
colnames(dat) <-c('sub','blk','trl','targN','targS',
                  'isWord','isNeg','dur','bright','nes',
                  'resp','rt','acc')
acc= as.integer(as.factor(dat$acc))

if (length(unique(dat$sub>1))) print("Error: More Than One Subject Detected")


tot=1:length(dat$sub)
plot(tot,dat$dur,col=mycol[acc],pch=mypch[dat$isNeg+1],cex=mycex[dat$isWord+1],typ='b')

########

numBlocks=max(dat$blk)+1
numTrialsPerBlock=tot/numBlocks

tapply(acc-1,dat$blk,mean)
tapply(dat$dur,dat$blk,mean)

