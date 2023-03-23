# Jeff Rouder, March, 2023
# in consultation with Anjali Thapar
# documentation of data collection needed

fileRoot="sy30bcy"
outFile=paste(fileRoot,"All.csv",sep='')
if (file.exists(outFile)) file.remove(outFile)
fileName=list.files(pattern=fileRoot)

R=length(fileName)
nr=nchar(fileRoot)

# codes as I understand them

# first digit is word frequency, 1=hi, 2=lo, 3=very low
# second digit is repetition, 1=1, 2=2, 3=new word.

# i am going to make repetition logically consistent,
# 0: new, 1: 1-rep, 2: 2-rep


line="sub, freq, repetition, rt, resp"
write(line,file=outFile)
for (r in 1:R){
  out=NULL
  con  <- file(fileName[r], open = "r")
  sub=substr(fileName[r],nr+1,nchar(fileName[r]))
  firstLine <- readLines(con, n = 1, warn = FALSE)
  flag=F
  while (!flag){
    trial<- readLines(con, n = 2, warn = FALSE)
    if (trial[1]!="END"){
      resp=substr(trial[1],1,1)
      rt=as.integer(substr(trial[1],2,7))
      code=trial[2]
      freq=as.integer(substr(trial[2],1,1))
      rep=as.integer(substr(trial[2],2,2))
      rep[rep==3]=0
      line=c(sub,freq,rep,rt,resp)
      out=rbind(out,line)
      }
    if (trial[1]=="END") flag=T
  }
  nc=length(code)
  write.table(out,file=paste(outFile,sep=""),quote=F,
              row.names = F,append=TRUE,sep=", ",col.names=F)
  close(con)
  print(r)
}

