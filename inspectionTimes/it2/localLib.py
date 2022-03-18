import os
import numpy as np
import pandas as pd

def getFileName(expName):
	targString = expName +'Sub'
	path='.'
	with os.scandir(path) as dirs:
		s=0;
		for entry in dirs:
			if targString in entry.name:
				s=s+1
	fname=expName+'Sub'+str(s) + '.dat'
	return(fname,s)
	

def startExp(expName,runMode):
	os.system('clear')
	print("This is expLib [Local Version]\n")
	print("Experiment Start\n\n")
	print("This is " + expName + " in runMode " + str(runMode))
	if runMode:
		[fname,subject]=getFileName(expName)
	else:
		fname="testDat"		
		subject=0
	print("Output FileName is " + fname)
	input("Enter to Continue, control-c to quit.  ") 
	fptr = open(fname, "w")
	return(fptr,subject)


def getBlockTrial(tpb,b,neu,neg,pos,oNu,oNg,oP):
    blockType=divmod(b,3)[0]
    blockRep=divmod(b,3)[1]
    t=range(blockRep*tpb,(blockRep+1)*tpb)
    if blockType==0:
        a=neu.iloc[oNu[t]]
    if blockType==1:
        a=neg.iloc[oNg[t]]
    if blockType==2:
        a=pos.iloc[oP[t]]
    return(a)
    

def loadV2(tpb,nb):
    prac=pd.read_csv("pracV2.csv")
    dat=pd.read_csv("allV2.csv")
    pos=dat.loc[dat['valence']==3]    
    neg=dat.loc[dat['valence']==2] 
    neu=dat.loc[dat['valence']==1]
    oP=np.random.choice(range(pos.shape[0]),pos.shape[0],replace=False)
    oNg=np.random.choice(range(neg.shape[0]),neg.shape[0],replace=False)
    oNu=np.random.choice(range(neu.shape[0]),neu.shape[0],replace=False)
    out=[getBlockTrial(tpb,b,neu,neg,pos,oNu,oNg,oP) for b in range(nb)]
    return(prac.append(out))    


