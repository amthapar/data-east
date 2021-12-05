import os

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
	


