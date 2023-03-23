# Jeff Rouder, March, 2023
# in consultation with Anjali Thapar
# documentation of data collection needed

fileRoot="dt16bcy"
outFile=paste(fileRoot,"All.csv",sep='')
if (file.exists(outFile)) file.remove(outFile)
fileName=list.files(pattern=fileRoot)

R=length(fileName)
nr=nchar(fileRoot)

# codes are separated by commas in original

# num: number of elements in display
# size: 1 is <50, 2 is >50
# The third code is always 1 and is not used

line="sub, num, size, rt, resp"
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
      code=as.integer(unlist(strsplit(trial[2],",")))
      line=c(sub,code[1:2],rt,resp)
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

