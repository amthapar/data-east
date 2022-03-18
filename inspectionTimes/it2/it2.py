from psychopy import core, visual, sound, event
import numpy as np
import sys
import decimal

from localLib import *

expName="it2"
runMode=False
trialsPerBlock=50
numBlock=9
[fptr,sub]=startExp(expName,runMode)

trialInfo=loadV2(trialsPerBlock,numBlock)



win=visual.Window(units="pix",
                  size=(128,32), 
                  color=[0,0,0], 
                  fullscr = True,
                  allowGUI=False)

mouse = event.Mouse(visible=False)
timer = core.Clock()
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)
abortKey='q'
   


def runTrial(trl,pres):
    isR=trl[1]
    b=pres[1]
    dur=[30,30,pres[0],1]
    cumDur=np.cumsum(dur)
    stim=[]
    stim.append(visual.TextStim(win,'+'))
    stim.append(visual.TextStim(win,''))
    stim.append(visual.TextStim(win,trl[0],color=[b,b,b]))
    stim.append(visual.NoiseStim(win,units='pix',
                                 noiseType='Uniform',
                                 size=[128,32],
                                 noiseElementSize=pres[2]))
    scene=0   
    for fp in range(max(cumDur)):
        if fp in cumDur:
            scene=scene+1
        stim[scene].draw()
        win.flip()
    timer.reset()
    keys=event.waitKeys(keyList=('r','u',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    respBool = (resp=='r')
    if (respBool==isR):
        correct1.play()
        correct2.play()
    else:
        error.play()
    stim[1].draw()
    win.flip()
    core.wait(1)
#    rt = decimal.Decimal(rt).quantize(decimal.Decimal('1e-3'))        
    return([int(respBool),round(rt,3),respBool==isR])


def getReady():
    visual.TextStim(win,"r= has r    +    u= no r",pos=(0,10)).draw()
    visual.TextStim(win,"Place your fingers on 'r' and 'u'",pos=(0,-10)).draw()
    visual.TextStim(win,"Press 'r' or 'u' to begin",pos=(0,-30)).draw()
    win.flip()
    event.waitKeys(keyList=('r','u'))
    visual.TextStim(win,'').draw()
    win.flip()
    core.wait(1)  

def takeBreak(block):
    visual.TextStim(win,"Good Job",pos=(0,30)).draw()
    blockText=f"You have completed {block+1} of {numBlock+1} blocks."
    visual.TextStim(win,blockText,pos=(0,10)).draw()
    visual.TextStim(win,"Take A Break",pos=(0,-10)).draw()
    visual.TextStim(win,"Press Any Key When Ready To Resume",pos=(0,-30)).draw()
    win.flip()
    event.waitKeys()
    core.wait(1)
    
def runBlock(block):
    pres=[4,.15,8]  #initial duration, contrast, mask size
    if block==0:
        pres[0]=7
    correctInRow=0
    getReady()
    for trialNum in range(block*trialsPerBlock,(block+1)*trialsPerBlock):
        trl=trialInfo.iloc[trialNum]
        resp=runTrial(trl,pres)
        out=[sub,block,trialNum]+trl.values.tolist()+pres+resp
        print(*out,sep=", ",file=fptr)
        if not resp[2]:
            pres[0]=pres[0]+1
            correctInRow=0
        elif correctInRow==1:
            pres[0]=pres[0]-1
            correctInRow=0
            if pres[0]<1:
                pres[0]=1
        else:
            correctInRow=1
    if block<numBlock-1:
        takeBreak(block)
                
def endMatter():
    visual.TextStim(win,"GREAT JOB",pos=(0,10)).draw()
    visual.TextStim(win,"You Are Done",pos=(0,-10)).draw()
    visual.TextStim(win,"Press Any Key to Exit",pos=(0,-30)).draw()
    win.flip()
    event.waitKeys()
    core.wait(1)
         
for b in range(numBlock+1):
    runBlock(b)
endMatter()            
fptr.close()
win.close()
core.quit()



