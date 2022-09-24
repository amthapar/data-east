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

[fptr,sub]=localLib.startExp(expName="aFlank1",runMode=False,fps=fps)
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
header=['sub','blk','trl','cong','cue','center','flanker',*headTarg,'soa','resp','rt','correct']



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

def instructTrial(cue,number,targets):
    frameTimes=[75,12,1]
    frame=[]
    display=fix()
    frame.append(visual.BufferImageStim(win,stim=display))
    display.append(visual.TextStim(win,cue,height=32,pos=center))
    frame.append(visual.BufferImageStim(win,stim=display))
    for i in range(nLoc):
        display.append(visual.TextStim(win,targets[i],pos=pos[i]))
    frame.append(visual.BufferImageStim(win,stim=display))    
    runFrames(frame,frameTimes)     
    [resp,rt]=getResp()
    correct=feedback(resp,targets[number])
    visual.ImageStim(win).draw()
    win.flip()
    core.wait(.5)
    return([resp,round(rt,3),correct])

 
def texter(text,keyList=None):
    for i in range(len(text)):
        visual.TextStim(win,text[i],pos=(0,-i*30)).draw()
    win.flip()
    if keyList is None:
        event.waitKeys()
    else:
        event.waitKeys(keyList=keyList)
    visual.TextStim(win,'').draw()
    win.flip()
    core.wait(1)

def block(blk,crit,numTrials=100,inc=1):
    correctInRow=[0,0];
    last=nLoc+1
    for t in range(numTrials):
        isCongruent=np.random.randint(2)
        flag=True
        while (flag):
            center=np.random.randint(nLoc)
            flag= (center==last)
        last=center
        if (isCongruent):
            flanker=center
        else:
            flag=True
            while (flag):
                flanker=np.random.randint(nLoc)
                flag = (center==flanker)
        cue=cueSet[flanker]*2+cueSet[center]+cueSet[flanker]*2
        targets=np.random.choice(targetSet,nLoc,replace=False)
        [resp,rt,correct]=trial(cue,center,targets,crit[isCongruent])    
        out=[sub,blk,t,isCongruent==1,cue,center,flanker,*targets,
             crit[isCongruent],resp,rt,correct]
        print(*out,sep=", ",file=fptr)
        fptr.flush()
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


texter(["Welcome","You Can Ask Questions At Any Time",
        "(press any key to continue)"])
instructTrial("33233",1,['F','K','S','H'])
instructTrial("44444",3,['J','S','A','L'])
instructTrial("11211",1,['G','J','A','H'])
instructTrial("33333",2,['F','L','D','G'])
instructTrial("22122",0,['L','A','S','J'])

texter(["Try It With Flashed Numbers and Letters","Any Questions?",
        "(press any key to continue)"])

trial("33233",1,['F','K','S','H'],120)
trial("44444",3,['J','S','A','L'],120)
trial("22122",0,['G','J','A','H'],120)
trial("11311",2,['F','L','D','G'],90)
trial("11411",3,['L','A','S','J'],90)


texter(["We Are Going To Speed Up The Flashes",
        "You Just Do Your Best",
        "Any Questions?", "(press any key to contine)"])

blk=0
texter(["Get Ready",
        "Responses are A, S, D, F,G , H, J, K, L",
        "Press G to Continue"],"g")
crit=block(blk,crit=[60,60],numTrials=50,inc=5)
blk=1
texter(["That was the first block",
        "As you do better, we make it harder",
        "So, you can't be perfect",
        "Just do your best",
        "Press G to Continue"],"g")

texter(["Get Ready for Block "+str(blk+1)+ " (of 5)",
        "Responses are A, S, D, F,G , H, J, K, L",
        "Press G to Continue"],"g")
crit=block(blk,crit,numTrials=50,inc=2)
while (blk<4):
    blk=blk+1
    texter(["Get Ready for Block "+str(blk+1)+ " (of 5)",
        "Responses are A, S, D, F,G , H, J, K, L",
        "Press G to Continue"],"g")
    crit=block(blk,crit,numTrials=80,inc=1)

fptr.close()
texter(['All Done','Thank You','See Experimenter'],'q')


win.close()
core.quit()
