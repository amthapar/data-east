from psychopy import core, visual, sound, event
import numpy as np
import localLib

[fptr,sub]=localLib.startExp(expName="as10",runMode=True)
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
    hline=visual.Line(win,units="pix",lineColor=[1,1,1])
    hline.start=[-10,0]
    hline.end=[+10,0]
    vline=visual.Line(win,units="pix",lineColor=[1,1,1])
    vline.start=[0,-10]
    vline.end=[0,+10]
    return([vline,hline])

    return(circ)

def cue(ori,rad):
    cuePos=[rad*np.cos(ori),rad*np.sin(ori)]
    line1=visual.Line(win,units="pix",lineColor=[1,1,1],lineWidth=5,
                      start=[x*.8 for x in cuePos],
                      end=[x*.9 for x in cuePos])
    line2=visual.Line(win,units="pix",lineColor=[1,1,1],lineWidth=5,
                      start=[x*1.1 for x in cuePos],
                      end=[x*1.2 for x in cuePos])
    return([line1,line2])

def plaid(ori,rad,sf):
    targPos=[rad*np.cos(ori),rad*np.sin(ori)]    
    grate1 = visual.GratingStim(win, tex='sqr', size=64,contrast=.2,
                                ori=45,mask='circle',pos=targPos,sf=sf)    
    grate2 = visual.GratingStim(win, tex='sqr', size=64,contrast=.2,
                                ori=135,mask='circle',blendmode="add",
                                pos=targPos,sf=sf)
    return([grate1,grate2])


    
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
    keys=event.getKeys(keyList=['v','n',abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=('v','n',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    resp = int(resp=='n')
    return([resp,rt])

def feedback(resp,isLarge):
    if (resp==isLarge):
        correct1.play()
        correct2.play()
    else:
        error.play()
    return(resp==isLarge)

def trial(oriTarg,oriCue,isLarge,crit,rad=300,sfLevels=[.12,.03],maskSamples=4):
    frameTimes=[30,30,3,3,crit]+[1]*maskSamples+[1]
    frame=[]
    frame.append(visual.BufferImageStim(win,stim=fix()))
    frame.append(visual.BufferImageStim(win))
    frame.append(visual.BufferImageStim(win,stim=cue(ori=oriCue,rad=rad)))
    frame.append(visual.BufferImageStim(win))
    frame.append(visual.BufferImageStim(win,stim=plaid(ori=oriTarg,rad=rad,
                                        sf=sfLevels[isLarge])))
    noise=visual.NoiseStim(win,units='pix',noiseType='Uniform',size=64,
                           noiseElementSize=8,mask="circle")
    noise.pos=[rad*np.cos(oriTarg),rad*np.sin(oriTarg)]
    for i in range(maskSamples):
        noise.updateNoise()
        frame.append(visual.BufferImageStim(win,stim=[noise]))
    frame.append(visual.BufferImageStim(win))    
    runFrames(frame,frameTimes)
    [resp,rt]=getResp()
    feedback(resp,isLarge)
    visual.ImageStim(win).draw()
    win.flip()
    core.wait(1)
    return([resp,round(rt,3),resp==isLarge])

def getReady(blkType):
    text=["Valid Cue","Opposite Cue"]
    visual.TextStim(win,text[blkType],pos=(0,30)).draw()
    visual.TextStim(win,"v=Small Plaid    +    n=Large Plaid",pos=(0,10)).draw()
    visual.TextStim(win,"Place your fingers on 'v' and 'n'",pos=(0,-10)).draw()
    visual.TextStim(win,"Press 'v' or 'n' to begin",pos=(0,-30)).draw()
    win.flip()
    event.waitKeys(keyList=('v','n'))
    visual.TextStim(win,'').draw()
    win.flip()
    core.wait(1)

def block(sub,blk,blkType,crit,numTrials=50):
    getReady(blkType)
    correctInRow=0;
    isLarge=np.random.randint(2,size=numTrials)
    oriTarg=np.random.uniform(low=0,high=2*np.pi,size=numTrials)
    if (blkType==0):
        oriCue=oriTarg
    else:
        oriCue=[(x+np.pi)%(2*np.pi) for x in oriTarg]
    for t in range(numTrials):
        [resp,rt,correct]=trial(oriTarg[t],oriCue[t],isLarge[t],crit)
        out=[sub,blk,blkType,t,crit,isLarge[t],round(oriTarg[t],2),round(oriCue[t],2),resp,rt,correct]
        print(*out,sep=", ",file=fptr)
        if not correct:
            crit=crit+1
            correctInRow=0
        elif correctInRow==1:
            crit=crit-1
            correctInRow=0
        else:
            correctInRow=1
        if crit==0:
            crit=1


blkType=[0,1,0,1,1,0]
startCrit=[20,20,4,4,4,4]
numTrials=[6,6,50,50,50,50]
for b in range(len(blkType)):
    block(sub,b,blkType[b],crit=startCrit[b],numTrials=numTrials[b])    
win.close()
core.quit()