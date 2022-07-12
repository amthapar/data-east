from psychopy import core, visual, sound, event
import numpy as np
import localLib


#win=visual.Window(units="pix",
#                  size=(256,256), 
#                  color=[0,0,0],
#                  fullscr = True,
#                  allowGUI=False)
#fps=round(win.getActualFrameRate())
#win.close()


#if fps!=75:
#    print()
#    print("WARNING....  Frame Rate is not 75")
#    input("Enter to Continue, control-c to quit.  ") 

[fptr,sub]=localLib.startExp(expName="adaptStroop",runMode=False,fps=60)
win=visual.Window(units="pix",
                  size=(256,256), 
                  color=[-1,-1,-1],
                  fullscr = True,
                  allowGUI=False)

mouse = event.Mouse(visible=False)
timer = core.Clock()
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)


pos = [[-500,300],[500,300],[-500,-300],[500,-300]]
colName=['Red','Green','Yellow','Blue']
colVal=[[1,0,0],[0,1,0],[1,1,-1],[-1,-1,1]]
targLevel=['X','M']
contrast=.25


def fix():
    outer=[]
    for i in range(4):
        outer.append(visual.Rect(win,units='pix',lineColor=[1,1,1],lineWidth=2,
                                 width=100,
                                 height=100,
                                 pos=pos[i]))
        outer.append(visual.TextStim(win,colName[i],pos=[pos[i][0],pos[i][1]+70]))
    outer.append(visual.Rect(win,units="pix",lineColor=[1,1,1],lineWidth=2,
                             width=150,
                             height=70))
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
    isRespM = int(resp=='m')
    return([isRespM,rt])

def feedback(isRespM,isTargM):
    if (isRespM==isTargM):
        correct1.play()
        correct2.play()
    else:
        error.play()
    return(isRespM==isTargM)

def trial(cueWord,cueCol,isTargM,crit):
    frameTimes=[60,3,crit,3,3,1]
    frame=[]
    display=fix()
    frame.append(visual.BufferImageStim(win,stim=display))
    display.append(visual.TextStim(win,colName[cueWord],color=colVal[cueCol],height=32))
    frame.append(visual.BufferImageStim(win,stim=display))
    targDisplay=fix()
    targDisplay.append(visual.TextStim(win,colName[cueWord],color=colVal[cueCol],height=32))
    targChar=['&','&','&','&']
    targChar[cueCol]=targLevel[isTargM]
    for i in range(4):
        targDisplay.append(visual.TextStim(win,targChar[i],pos=pos[i]))
    frame.append(visual.BufferImageStim(win,stim=targDisplay))
    maskDisplay1=fix()
    maskDisplay1.append(visual.TextStim(win,colName[cueWord],color=colVal[cueCol],height=32))
    maskDisplay2=fix()
    maskDisplay2.append(visual.TextStim(win,colName[cueWord],color=colVal[cueCol],height=32))
    for i in range(4):
        maskDisplay1.append(visual.TextStim(win,'$',pos=pos[i]))
        maskDisplay2.append(visual.TextStim(win,'#',pos=pos[i]))
    frame.append(visual.BufferImageStim(win,stim=maskDisplay1))
    frame.append(visual.BufferImageStim(win,stim=maskDisplay2))
    frame.append(visual.BufferImageStim(win,stim=display))                
    runFrames(frame,frameTimes)
    [isRespM,rt]=getResp()
    correct=feedback(isRespM,isTargM)
    visual.ImageStim(win).draw()
    win.flip()
    core.wait(.5)
    return([isRespM,round(rt,3),correct])

def getReady():
    visual.TextStim(win,"Place your fingers on 'x' and 'm'",pos=(0,-10)).draw()
    visual.TextStim(win,"Press 'x' or 'm' to begin",pos=(0,-30)).draw()
    win.flip()
    event.waitKeys(keyList=('x','m'))
    visual.TextStim(win,'').draw()
    win.flip()
    core.wait(1)

def block(blk,crit=[90,60],numTrials=100):
    getReady()
    correctInRow=[0,0];
    for t in range(numTrials):
        isTargM=np.random.randint(2)
        isCongruent=np.random.randint(2)
        cueCol=np.random.randint(4)
        if (isCongruent):
            cueWord=cueCol
        else:
            flag=True
            while (flag):
                cueWord=np.random.randint(4)
                flag = (cueWord==cueCol)
        [resp,rt,correct]=trial(cueWord=cueWord,cueCol=cueCol,isTargM=isTargM,
                                crit=crit[isCongruent])
        out=[sub,blk,t,isCongruent,cueWord,cueCol,isTargM,
             crit[isCongruent],resp,rt,correct]
        print(*out,sep=", ",file=fptr)
        if not correct:
            crit[isCongruent]=crit[isCongruent]+5
            correctInRow[isCongruent]=0
        elif correctInRow[isCongruent]==1:
            crit[isCongruent]=crit[isCongruent]-5
            correctInRow[isCongruent]=0
        else:
            correctInRow[isCongruent]=1
        if crit[isCongruent]==0:
            crit[iCongruent]=1


block(0)
startCrit=[20,20,9,5,5,9,9,5]  # for 75
numTrials=[10,10,50,50,50,50,50,50]
win.close()
core.quit()
