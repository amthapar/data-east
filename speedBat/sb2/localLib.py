import os

def getFileName(expName,site):
    targString = expName + site +'Sub'
    path='.'
    with os.scandir(path) as dirs:
        s=0;
        for entry in dirs:
            if targString in entry.name:
                s=s+1
    fname=expName+site+'Sub'+str(s)
    return(fname,s)
    


def startExp(expName,runMode,fps=0):
    os.system('clear')
    print("This is expLib [Local Version]\n")
    print("Experiment Start\n\n")
    print("This is " + expName + " in runMode " + str(runMode))
    if runMode:
        print("Enter Site Abbreviation (B=BrynMawr, M=Mississipi State, U=UCI): ")
        site=input()
        [fname,subject]=getFileName(expName,site)
    else:
        fname="testDat"        
        subject=0
    print("Output FileName is " + fname)
    print("Refresh Rate is " + str(fps))
    input("Enter to Continue, control-c to quit.  ") 
    fptr = open(fname, "w")
    fptr.flush()
    return(fptr,subject)