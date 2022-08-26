dat=read.csv('jeffDat')
dat$cong=dat$cong==" True"
dat$congI=as.integer(dat$cong)
png('temp.png')
plot(dat$soa*1000/60,pch=dat$congI+21,bg=dat$cong+1,
     xlab="Trial",ylab="SOA in ms")
abline(v=seq(50,350,100),col='lightblue')
dev.off()
