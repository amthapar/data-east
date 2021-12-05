from psychopy import core, visual, sound, event
import numpy as np
import sys
import decimal

from localLib import *

expName="it1"
runMode=False
[fptr,sub]=startExp(expName,runMode)

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
abortKey='q'

targ=np.loadtxt("allV1.txt",dtype='str',usecols=0)
targType=np.loadtxt("allV1.txt",dtype='int',usecols=1)
targNum=len(targ)
o=np.random.choice(range(targNum),targNum)




def trial(targ,targDur,word,b,nes):
    dur=[30,30,targDur,1]
    cumDur=np.cumsum(dur)
    stim=[]
    stim.append(visual.TextStim(win,'+'))
    stim.append(visual.TextStim(win,''))
    stim.append(visual.TextStim(win,targ,color=[b,b,b]))
    stim.append(visual.NoiseStim(win,units='pix',
                                 noiseType='Uniform',
                                 size=[256,256],
                                 noiseElementSize=nes))
    scene=0   
    for fp in range(max(cumDur)):
        if fp in cumDur:
            scene=scene+1
        stim[scene].draw()
        win.flip()
    timer.reset()
    keys=event.waitKeys(keyList=('v','n',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        win.close()
        core.quit()   
    respBool = (resp=='v')
    if (respBool==word):
        correct1.play()
        correct2.play()
    else:
        error.play()
    core.wait(.5)
    rt = decimal.Decimal(rt).quantize(decimal.Decimal('1e-3'))        
    return(respBool,rt)



for n in range(30):
    critDur=6
    b=.35
    nes=8
    [respBool,rt]=trial(targ[o[n]],critDur,targType[o[n]]>0,b=b,nes=nes)
    print(sub,n,o[n],targ[o[n]],targType[o[n]],critDur,b,nes,respBool,rt,file=fptr)


win.close()
core.quit()



