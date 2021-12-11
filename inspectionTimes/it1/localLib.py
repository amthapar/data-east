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


def getBlockTrial(b,bT,trialsPerBlock,pos,neg,oP,oN):
    t=range(trialsPerBlock*b,trialsPerBlock*(b+1))
    if bT==0:
        a=pos.iloc[oP[t]]
    else:
        a=neg.iloc[oN[t]]
    return(a)




def loadV1StairCases(trialsPerBlock,numBlock):
    dat=pd.read_csv("./allV1.txt")
    pos=dat.loc[dat['valence']==0]
    neg=dat.loc[dat['valence']==1]
    oP=np.random.choice(range(pos.shape[0]),pos.shape[0],replace=False)
    oN=np.random.choice(range(neg.shape[0]),neg.shape[0],replace=False)
    blockType=[0,1]*divmod(numBlock,2)[0]
    return([getBlockTrial(b,blockType[b],trialsPerBlock,pos,neg,oP,oN) 
            for b in range(numBlock)])


