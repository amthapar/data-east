dat=read.csv('aStroop3BSub1')
dat$cong=(dat$cong==" True")
dat$congI=as.integer(dat$cong)

plot(dat$soa*1000/60,pch=dat$congI+21,bg=dat$cong+1,
     xlab="Trial",ylab="SOA in ms")
abline(v=seq(50,350,100),col='lightblue')
