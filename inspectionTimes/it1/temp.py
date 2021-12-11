import numpy as np
import pandas as pd

dat=pd.read_csv("./allV1.txt")
pos=dat.loc[dat['valence']==0]
neg=dat.loc[dat['valence']==1]
oP=np.random.choice(range(pos.shape[0]),pos.shape[0],replace=False)
oN=np.random.choice(range(neg.shape[0]),neg.shape[0],replace=False)

trialsPerBlock=10
numBlock=4
blockType=[0,1]*divmod(numBlock,2)[0]

def getBlockTrial(b,bT,oP,oN):
    t=range(trialsPerBlock*b,trialsPerBlock*(b+1))
    if bT==0:
        a=pos.iloc[oP[t]]
    else:
        a=neg.iloc[oN[t]]
    return(a)

a=[getBlockTrial(b,blockType[b],oP,oN) for b in range(numBlock)]    



def loadV1ForStaircase():
    targ=np.loadtxt("./allV1.txt",dtype='str',usecols=0)
    targType=np.loadtxt("./allV1.txt",dtype='int',usecols=1)
    targNum=range(len(targ))
    non=[]
    pos=[]
    neg=[]
    for i in range(len(targ)):
        if targType[i]==0:
            non.append(targ[i])
        if targType[i]==1:
            pos.append(targ[i])
        if targType[i]==2:
            neg.append(targ[i])
    tot=len(non)
    half=int(tot/2)
    posneg=[0,1]*half
    np.random.shuffle(posneg)
    posNon=[]
    negNon=[]
    posNonNum=[]
    negNonNum=[]
    for i in range(len(non)):
        if posneg[i]==0:
            posNon.append(non[i])
            posNonNum.append(i)
        if posneg[i]==1:
            negNon.append(non[i])
            negNonNum.append(i)                
    return([pos,posNon,posNonNum,neg,negNon,negNonNum])