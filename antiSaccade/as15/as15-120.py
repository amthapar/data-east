from psychopy import core, visual, sound, event
import numpy as np
import localLib


win=visual.Window(units="pix",
                  size=(256,256), 
                  color=[0,0,0],
                  fullscr = True,
                  allowGUI=False)
fps=round(win.getActualFrameRate())
win.close()


if fps!=120:
    print()
    print("WARNING....  Frame Rate is not 120")
    input("Enter to Continue, control-c to quit.  ") 

[fptr,sub]=localLib.startExp(expName="as15-120",runMode=True,fps=fps)
win=visual.Window(units="pix",
                  size=(256,256), 
                  color=[0,0,0],
                  fullscr = True,
                  allowGUI=False)

mouse = event.Mouse(visible=False)
timer = core.Clock()
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)

def fix():
    hline=visual.Line(win,units="pix",lineColor=[1,1,1],lineWidth=3)
    hline.start=[-10,0]
    hline.end=[+10,0]
    vline=visual.Line(win,units="pix",lineColor=[1,1,1],lineWidth=3)
    vline.start=[0,-10]
    vline.end=[0,+10]
    return([vline,hline])


def cue(ori,rad):
    cuePos=[rad*np.cos(ori),rad*np.sin(ori)]
    line1=visual.Line(win,units="pix",lineColor=[1,1,1],lineWidth=5,
                      start=[x*.65 for x in cuePos],
                      end=[x*.85 for x in cuePos])
    line2=visual.Line(win,units="pix",lineColor=[1,1,1],lineWidth=5,
                      start=[x*1.15 for x in cuePos],
                      end=[x*1.35 for x in cuePos])
    return([line1,line2])

def runFrames(frame,frameTimes,timerStart=4):
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

def getResp(abortKey='9'):
    keys=event.getKeys(keyList=['x','m',abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=('x','m',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    resp = int(resp=='m')
    return([resp,rt])

def feedback(resp,isLarge):
    if (resp==isLarge):
        correct1.play()
        correct2.play()
    else:
        error.play()
    return(resp==isLarge)

def trial(oriTarg,oriCue,isLet,crit,rad=300,letLev=['X','M'],contrast=.25):
    pos=[rad*np.cos(oriTarg),rad*np.sin(oriTarg)]
    frameTimes60=[30,30,18,1,crit,3,3,3,1]
    frameTimes75=[37,37,22,1,crit,3,3,3,1]
    frameTimes120=[60,60,36,2,crit,6,6,6,1]

    frame=[]
    frame.append(visual.BufferImageStim(win,stim=fix()))
    frame.append(visual.BufferImageStim(win))
    frame.append(visual.BufferImageStim(win,stim=cue(ori=oriCue,rad=rad)))
    frame.append(visual.BufferImageStim(win))
    targ=visual.TextStim(win,text=letLev[isLet],pos=pos,color=[contrast,contrast,contrast])
    frame.append(visual.BufferImageStim(win,stim=[targ]))
    mask=visual.TextStim(win,text='#',pos=pos,color=[1,1,1])
    frame.append(visual.BufferImageStim(win,stim=[mask]))
    mask=visual.TextStim(win,text='@',pos=pos,color=[1,1,1])
    frame.append(visual.BufferImageStim(win,stim=[mask]))
    mask=visual.TextStim(win,text='%',pos=pos,color=[1,1,1])
    frame.append(visual.BufferImageStim(win,stim=[mask]))
    frame.append(visual.BufferImageStim(win))    
    runFrames(frame,frameTimes120)
    [resp,rt]=getResp()
    feedback(resp,isLet)
    visual.ImageStim(win).draw()
    win.flip()
    core.wait(.5)
    return([resp,round(rt,3),resp==isLet])

def getReady(blkType):
    text=["Valid Cue","Opposite Cue"]
    visual.TextStim(win,text[blkType],pos=(0,30)).draw()
    visual.TextStim(win,"Place your fingers on 'x' and 'm'",pos=(0,-10)).draw()
    visual.TextStim(win,"Press 'x' or 'm' to begin",pos=(0,-30)).draw()
    win.flip()
    event.waitKeys(keyList=('x','m'))
    visual.TextStim(win,'').draw()
    win.flip()
    core.wait(1)






def block(sub,blk,blkType,crit,numTrials=50):
    getReady(blkType)
    correctInRow=0;
    isLet=np.random.randint(2,size=numTrials)
    oriTarg=np.random.uniform(low=0,high=2*np.pi,size=numTrials)
    if (blkType==0):
        oriCue=oriTarg
    else:
        oriCue=[(x+np.pi)%(2*np.pi) for x in oriTarg]
    for t in range(numTrials):
        [resp,rt,correct]=trial(oriTarg[t],oriCue[t],isLet[t],crit)
        out=[sub,blk,blkType,t,crit,isLet[t],round(oriTarg[t],2),round(oriCue[t],2),resp,rt,correct]
        print(*out,sep=", ",file=fptr)
        if crit<6:
            inc=1
        else:
            inc=2
        if not correct:
            crit=crit+inc
            correctInRow=0
        elif correctInRow==1:
            crit=crit-inc
            correctInRow=0
        else:
            correctInRow=1
        if crit==0:
            crit=1
        win.flip()
    if blk<7:
        visual.TextStim(win,'Take A Break').draw()
        visual.TextStim(win,"Press Any Key When Ready",pos=(0,-30)).draw()
        win.flip()
        event.waitKeys()
        core.wait(.5)
    return(crit)


blkType=[0,1,1,0,0,1,1,0]

startCrit=[30,40,13,7]
crit=[0,0]
numTrials=[10,10,50,50,50,50,50,50]
#numTrials=[2,2,2,2,2,2,2,2]
for b in range(len(blkType)):
    if b==len(blkType)-1:
        visual.TextStim(win,'LAST BLOCK!!!').draw()
        visual.TextStim(win,"Hang in there, Almost Done, Try Your Best",pos=(0,-30)).draw()
        visual.TextStim(win,"Press Any Key When Ready",pos=(0,-60)).draw()
        win.flip()
        event.waitKeys()
        core.wait(.5)        
    bt=blkType[b]
    if (b<4):
        useCrit=startCrit[b]
    else:
        useCrit=crit[bt]
    crit[bt]=block(sub,b,bt,crit=useCrit,numTrials=numTrials[b])    
win.close()
core.quit()
