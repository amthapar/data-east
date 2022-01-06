dat=read.csv('testDat')
colnames(dat)=c('sub','blk','blyType','trl','dur','stimType','targetOri','cueOri','resp','rt','acc')
plot(dat$dur[dat$blk==3])
plot(dat$dur[dat$blk==2])