from psychopy import core, visual, event
import numpy as np
import localLib



win=visual.Window(units="pix",
                  size=(256,256), 
                  color=[0,0,0],
                  fullscr = True,
                  allowGUI=False)
fps=round(win.getActualFrameRate())
win.close()

if fps!=60:
    print()
    print("WARNING....  Frame Rate is not 60hz.")
    input("Enter to Continue, control-c to quit.  ") 

[fptr,sub]=localLib.startExp(expName="aStroop3",runMode=False,fps=fps)
win=visual.Window(units="pix",
                  size=(256,256), 
                  color=[-1,-1,-1],
                  fullscr = True,
                  allowGUI=False)

mouse = event.Mouse(visible=False)
timer = core.Clock()


abortKey='q'
center=[0,-300]
ang=[val*np.pi/180 for val in [150,110,70,30]]
pos=[[600*np.cos(w)+center[0],600*np.sin(w)+center[1]]  for w in ang]
boxLabel=['One','Two','Three','Four']
cueSet=['1','2','3','4']
targetSet=['A','S','D','F','G','H','J','K','L']
responseSet=['a','s','d','f','g','h','j','k','l']
responseSet.append(abortKey)
contrast=.25
nLoc=len(ang)

headTarg=["targ"+x for x in boxLabel]
header=['sub','blk','trl','cong','cueWord','cueColor',*headTarg,'soa','resp','rt','correct']


def fix():
    outer=[]
    for i in range(nLoc):
        outer.append(visual.Rect(win,units='pix',
                                 fillColor=[-1,-1,-1],
                                 lineColor=[1,1,1],
                                 lineWidth=2,
                                 width=100,
                                 height=100,
                                 pos=pos[i]))
        outer.append(visual.TextStim(win,boxLabel[i],
                                     pos=[pos[i][0],pos[i][1]+70],
                                     height=24))
    outer.append(visual.Rect(win,units="pix",
                             fillColor=[-1,-1,-1],
                             lineColor=[1,1,1],
                             lineWidth=2,
                             width=150,
                             height=70,
                             pos=center))
    return(outer)

def runFrames(frame,frameTimes,timerStart=1):
    event.clearEvents()
    currentFrame=0
    cumTimes=np.cumsum(frameTimes)    
    for refresh in range(max(cumTimes)):
        if refresh in cumTimes:
            currentFrame=currentFrame+1
            if currentFrame==timerStart:
                timer.reset()
        frame[currentFrame].draw()
        win.flip()        

def getResp():
    keys=event.getKeys(keyList=responseSet,timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=(responseSet),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    return([resp,rt])

def feedback(resp,correctResp):
    if (resp.lower()==correctResp.lower()):
        visual.ImageStim(win,"correct.png").draw()
    else:
        visual.ImageStim(win,"error.png").draw()
    win.flip
    return(resp.lower()==correctResp.lower())

def trial(cue,number,targets,crit):
    frameTimes=[75,12,crit,3,3,30]
    frame=[]
    display=fix()
    frame.append(visual.BufferImageStim(win,stim=display))
    display.append(visual.TextStim(win,cue,height=32,pos=center))
    frame.append(visual.BufferImageStim(win,stim=display))
    targDisplay=fix()
    #targDisplay.append(visual.TextStim(win,cueWord,color=colVal[cueCol],
                                       #height=32,pos=center))
    for i in range(nLoc):
        targDisplay.append(visual.TextStim(win,targets[i],pos=pos[i]))
    frame.append(visual.BufferImageStim(win,stim=targDisplay))
    maskDisplay1=fix()
    maskDisplay2=fix()
    for i in range(nLoc):
        maskDisplay1.append(visual.TextStim(win,'@',pos=pos[i]))
        maskDisplay2.append(visual.TextStim(win,'#',pos=pos[i]))
    frame.append(visual.BufferImageStim(win,stim=maskDisplay1))
    frame.append(visual.BufferImageStim(win,stim=maskDisplay2))
    frame.append(visual.BufferImageStim(win,stim=fix()))                            
    runFrames(frame,frameTimes)     
    [resp,rt]=getResp()
    correct=feedback(resp,targets[number])
    visual.ImageStim(win).draw()
    win.flip()
    core.wait(.5)
    return([resp,round(rt,3),correct])
 
def getReady():
    visual.TextStim(win,"Get Ready, Responses are A to L",pos=(0,-10)).draw()
    visual.TextStim(win,"Press 'G' to begin",pos=(0,-30)).draw()
    win.flip()
    event.waitKeys(keyList=('g'))
    visual.TextStim(win,'').draw()
    win.flip()
    core.wait(1)

def block(blk,crit,numTrials=100,inc=1):
    getReady()
    correctInRow=[0,0];
    last=nLoc+1
    for t in range(numTrials):
        isCongruent=np.random.randint(2)
        flag=True
        while (flag):
            number=np.random.randint(nLoc)
            flag= (number==last)
        last=number
        if (isCongruent):
            cue=cueSet[number]*(number+1)
        else:
            flag=True
            while (flag):
                alt=np.random.randint(nLoc)
                cue=cueSet[alt]*(number+1)
                flag = (number==alt)
        targets=np.random.choice(targetSet,nLoc,replace=False)
        [resp,rt,correct]=trial(cue,number,targets,crit[isCongruent])    
        out=[sub,blk,t,isCongruent==1,cue,number,*targets,
             crit[isCongruent],resp,rt,correct]
        print(*out,sep=", ",file=fptr)
        if not correct:
            crit[isCongruent]=crit[isCongruent]+inc
            correctInRow[isCongruent]=0
        elif correctInRow[isCongruent]==1:
            crit[isCongruent]=crit[isCongruent]-inc
            correctInRow[isCongruent]=0
        else:
            correctInRow[isCongruent]=1
        if crit[isCongruent]==0:
            crit[isCongruent]=1
    return(crit)


print(*header,sep=", ",file=fptr)
fptr.flush()
blk=0
crit=block(blk,crit=[60,60],numTrials=0,inc=5)
while (blk<4):
    blk=blk+1
    crit=block(blk,crit,numTrials=100,inc=1)

win.close()
core.quit()
