dat=read.csv('aStroop2MSub0')
clean=dat[dat$blk>0,]
tapply(clean$soa,list(clean$cong,clean$blk),mean)*1000/60
