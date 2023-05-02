##################################
# Importing  #####################
##################################

from psychopy import core, visual, sound, event
import random as rd
import decimal
import sys
import numpy as np  
import os
import copy as cp
import localLib


##############################
# Setup  #####################
##############################

target_val = [-.2,-.2,-.2]

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

run_mode = False
if run_mode == False:
    nt_inst_t = 5
    nt_rest_tasks = 5
    nt_train = 2
else:
    nt_inst_t = 50
    nt_rest_tasks = 32
    nt_train = 10
[fptr,sub]=localLib.startExp(expName="sb2",runMode=run_mode,fps=fps)


    
    
    
########################################
# GLOBAL SETTINGS  #####################
########################################

scale=400

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)
mouse = event.Mouse(visible=False)
timer = core.Clock()
seed = rd.randrange(1e6)
rng = rd.Random(seed)

correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)

header=['sub','task','condition','correct','rt','resp','block','accuracy','trial','round','2fast']


########################################
# Functions  #####################
########################################


### Logestics:

def runFrames(frame,frameTimes,timerStart=3):
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


def getResp(truth, abortKey='9'):
    keys=event.getKeys(keyList=['x','m',abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=('x','m',abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    if truth == True:
        acc = int(resp=='m')
    else:
        acc = int(resp=="x")
    return([resp,rt,acc])

def feedback(resp,correctResp):
    if (resp==correctResp):
        correct1.play()
        core.wait(.1)
        correct2.play()
    else:
        error.play()
    return(resp==correctResp)



### Conjuction Search:


def conjunct(truth, size, set_size, st, ins = False):
    if size == set_size[1]:
        x = np.arange(-120,121,60)
        y = np.arange(-120,121,60)
    else:
        x = np.arange(-90,90,60)
        y = np.arange(-90,90,60)

    xx, yy = np.meshgrid(x,y)
    grid = np.stack((xx,yy), axis = -1)
    grid_flat = [i2 for i in grid for i2 in i]
    grid_select = rd.sample(grid_flat, size)
    jitter = np.random.uniform(low=-20, high=20, size=(len(grid_select),2))
    grid_jitter = grid_select + jitter
    stims = []
    for pos in range(size):
        x,y = grid_jitter[pos]
        text_stim = visual.TextStim(
            win = win,
            text = st,
            pos = (x, y),
            color = 'white',
            height = 20
        )
        stims.append(text_stim)
    if truth == True:
        pick = rd.sample(range(size), 1)
        x,y = grid_jitter[pick[0]]
        text_stim = visual.TextStim(
            win = win,
            text = st,
            pos = (x, y),
            color = 'white',
            height = 20,
            flipHoriz = True
        )
        stims[pick[0]] = text_stim
        if ins == True:
            text_stim2 = visual.TextStim(
                win = win,
                text = st,
                pos = (x, y),
                color = 'red',
                height = 20,
                flipHoriz = True
            )
            stims[pick[0]] = text_stim2
    return(stims)


def conjunctTrial(size, truth, set_size, st):
    x = visual.TextStim(
        win = win,
        text = "Press 'X' if you do not see a backward letter",
        pos = (-400,-475),
        color = "white"
    )
    m = visual.TextStim(
        win = win,
        text = "Press 'M' if you do see a backward letter",
        pos = (400,-475),
        color = "white"
    )
    frameTimes=[30,30,1]  #at 60hz
    stims = conjunct(truth, size, set_size, st)
    frame=[]
    tstim = [visual.TextStim(win,"+"), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    tstim = [visual.TextStim(win,""), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    tstim = stims+[x,m]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    runFrames(frame,frameTimes, timerStart=2)
    [resp,rt,ac]=getResp(truth = truth)
    acc=feedback(ac,1)
    if rt < .2:
        warn()
        tooFast = 1
    else:
        tooFast = 0

    return(resp,rt,acc,tooFast)



def runConjunct(trial_size, set_size = [2,18], method = 1, train = False, rnd=1):
    st = "N" if train == False else "N"
    truth = []
    size = []
    if method == 1:
        for i in range(trial_size):
            truth.append(i%2)
            size.append(set_size[i%2])
    if method == 2:
        for i in range(trial_size):
            x = rd.choices([0,1], k = 2)
            truth.append(x[0]%2)
            size.append(set_size[x[1]%2])
    rd.shuffle(truth)
    rd.shuffle(size)
    for i in range(trial_size):
        [resp,rt,acc,tooFast] = conjunctTrial(size[i],truth[i],set_size,st)

        cond = 0 if size[i] == set_size[0]  else 1
        resp2 = 1 if resp == "m" else 0
        out=[sub,2,cond,truth[i],round(rt,2),resp2,int(train),int(acc),i+1,rnd,tooFast]
        print(*out,sep=", ",file=fptr)
        fptr.flush()

### Mental Rotation:

def curveLine(ang, dir=0):
    if ang == 180: center1 = (100, 0)
    else: 
        center1 = (0, 0)
        center2 = (-250, 100)
    radius = 100
    start_angle = 0
    end_angle =  ang
    num_points = 10000
    angles = [np.deg2rad(angle) for angle in np.linspace(start_angle, end_angle, num_points)]

    x_coords1 = center1[0] + radius * np.cos(angles)
    y_coords1 = center1[1] + radius * np.sin(angles)
    x_coords2 = center2[0] + radius * np.cos(angles)
    y_coords2 = center2[1] + radius * np.sin(angles)
    if dir == 3:
        coords1 = [(-x,y) for x,y in zip(x_coords1, y_coords1)]
        coords2 = [(-x-450,y) for x,y in zip(x_coords2, y_coords2)]
        txt = f'Rotate {ang}\u00B0 counter clockwise!'
    else:
        coords1 = [(x,y) for x,y in zip(x_coords1, y_coords1)]
        coords2 = [(x,y) for x,y in zip(x_coords2, y_coords2)]
        txt = f'Rotate {ang}\u00B0 clockwise!'

    if ang != 0:
        # if ang == 180:
            # coords = np.flip(coords, axis=1)
            # [x,y] = coords[-1]
            # pointer1_vert1 = [(x,y), (x+10,y+12)]
            # pointer1_vert2 = [(x,y), (x+10,y-10)]
        [x,y] = coords1[0]
        f_pointer1_vert1 = [(x,y), (x+10,y+10)]
        f_pointer1_vert2 = [(x,y), (x-12,y+10)] 
        [x,y] = coords2[0]
        s_pointer1_vert1 = [(x,y), (x+10,y+10)]
        s_pointer1_vert2 = [(x,y), (x-12,y+10)] 


        f_wedge = visual.ShapeStim(
            win=win, 
            lineColor='white', 
            vertices=coords1,
            closeShape=False)
        f_line1 = visual.ShapeStim(
            win = win, 
            lineColor="white",
            vertices=f_pointer1_vert1
        )
        f_line2 = visual.ShapeStim(
            win = win, 
            lineColor="white",
            vertices=f_pointer1_vert2
        )
        f_text_stim = visual.TextStim(
            win = win,
            text = txt,
            pos = (center1[0],center1[1]+150),
            color = 'white'
        )
        s_wedge = visual.ShapeStim(
            win=win, 
            lineColor='white', 
            vertices=coords2,
            closeShape=False)
        s_line1 = visual.ShapeStim(
            win = win, 
            lineColor="white",
            vertices=s_pointer1_vert1
        )
        s_line2 = visual.ShapeStim(
            win = win, 
            lineColor="white",
            vertices=s_pointer1_vert2
        )
        s_text_stim = visual.TextStim(
            win = win,
            text = txt,
            pos = (center2[0],center2[1]+150),
            color = 'white'
        )
        [flash_x, flash_y, flash_width, flash_height] = [0,-40, 160, 20]
        body = visual.Rect(
            win = win, 
            units = "pix",
            width = flash_width,
            height = flash_height, 
            lineColor = [0, 0, 0],
            pos = [flash_x, flash_y],
            fillColor = "white"
	    )
        head_verts = [(flash_x+flash_width/2, flash_y-flash_height/2-10), (flash_x+flash_width/2, flash_y+flash_height/2+10), (flash_x+flash_width/2+flash_height, flash_y)]
        head = visual.ShapeStim(
            win, 
            fillColor='white',
            vertices=head_verts, 
            lineColor='white')

    

        f_stim = [f_wedge,f_line1,f_line2,f_text_stim]
        s_stim = [s_wedge,s_line1,s_line2,s_text_stim, body, head]
        return(f_stim, s_stim)
    else:
        f_text_stim = visual.TextStim(
            win = win,
            text = f'Do not rotate!',
            pos = (0,150),
            color = 'white'
        )
        s_text_stim = visual.TextStim(
            win = win,
            text = f'Match?',
            pos = (0,150),
            color = 'white'
        )
        return(f_text_stim,s_text_stim)


def rotMat(orig_mat, rotation, flip = False):
    rot_mat = orig_mat
    for r in range(rotation):
        rot_mat = np.rot90(rot_mat)
    if flip == True:
        ax = rd.choice([0,1])
        if rotation == 2: 
            rot_mat = np.flip(rot_mat, axis = ax)
        else:
            rot_mat = np.flip(rot_mat, axis = ax)
    return rot_mat 			


def presMat(orig_mat, rot_mat, ins = False):
    rect = visual.Rect(
        win = win, 
        units = "pix",
        width = 60,
        height = 60, 
        lineColor = [0, 0, 0]
    )
    stims = []
    if ins == True:
        y = -100 		
        for row in range(3):
            x1 = -60
            for col in range(3):
                trect = cp.copy(rect)
                if orig_mat[row,col] == 1:
                    trect.fillColor = [1,-1,-1]
                else:
                    trect.fillColor = [-1,-1,1]
                trect.pos = [x1,y]
                stims.append(trect)
                x1+=60
            y+=60
        return(stims)
    y = -100 		
    for row in range(3):
        x1 = -300
        x2 = 200
        for col in range(3):
            trect = cp.copy(rect)
            if orig_mat[row,col] == 1:
                trect.fillColor = [1,-1,-1]
            else:
                trect.fillColor = [-1,-1,1]
            trect.pos = [x1,y]
            stims.append(trect)
            trect2 = cp.copy(rect)
            x1+=60
            if rot_mat[row,col] == 1:
                trect2.fillColor = [1,-1,-1]
            else:
                trect2.fillColor = [-1,-1,1]
            trect2.pos = [x2,y]
            stims.append(trect2)
            x2+=60
        y+=60
    return(stims)

def menRotTrial(stims, truth, curve, match = False):
    x = visual.TextStim(
        win = win,
        text = "Press 'X' for not a match",
        pos = (-400,-475),
        color = "white"
    )
    m = visual.TextStim(
        win = win,
        text = "Press 'M' for match",
        pos = (400,-475),
        color = "white"
    )


    frameTimes=[30,30,60,60,1]  #at 60hz
    frame=[]
    #frame.append(visual.BufferImageStim(win, stim = stims))
    tstim = [visual.TextStim(win,"+"), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    tstim = [visual.TextStim(win,""), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    if match == True:
        tstim = [curve, x, m]
        frame.append(visual.BufferImageStim(win,stim=tstim))
    else:
        curve.append(x)
        curve.append(m)
        frame.append(visual.BufferImageStim(win,stim=curve))
    tstim = [visual.TextStim(win,""), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    stims.append(x)
    stims.append(m)
    frame.append(visual.BufferImageStim(win,stim=stims))
    runFrames(frame,frameTimes, timerStart=4)
    [resp,rt,ac]=getResp(truth = truth)
    acc=feedback(ac,1)
    
    if rt < .2:
        warn()
        tooFast = 1
    else:
        tooFast = 0

    return(resp, rt, acc, tooFast)



def runMenRot(trial_size, method = 1, rotations = [0,1,3], train = False, rnd=1):
    mats = []
    '''
    if train == True:
        mats.append(np.array([[1,0,0],[1,0,0],[0,0,0]]))
        mats.append(np.array([[0,0,0],[0,1,0],[0,1,1]]))
        mats.append(np.array([[1,1,0],[0,1,1],[0,0,0]]))
        mats.append(np.array([[1,0,0],[0,0,0],[0,1,0]]))
        mats.append(np.array([[1,0,0],[0,0,0],[0,1,1]]))
        mats.append(np.array([[0,1,0],[1,0,1],[0,0,0]]))
    else:
        mats.append(np.array([[0,0,0],[1,1,0],[1,0,1]]))
        mats.append(np.array([[0,0,1],[1,0,0],[1,0,1]]))
        mats.append(np.array([[0,1,0],[1,0,1],[1,0,0]]))
        mats.append(np.array([[0,1,0],[1,0,0],[1,0,1]]))
        mats.append(np.array([[1,0,0],[0,0,0],[0,1,1]]))
        mats.append(np.array([[0,1,0],[1,0,1],[0,0,0]]))
    '''
    mats.append(np.array([[1,0,0],[1,0,0],[0,0,0]]))
    mats.append(np.array([[0,0,0],[0,1,0],[0,1,1]]))
    mats.append(np.array([[1,1,0],[0,1,1],[0,0,0]]))
    mats.append(np.array([[1,0,0],[0,0,0],[0,1,0]]))
    mats.append(np.array([[1,0,0],[0,0,0],[0,1,1]]))
    mats.append(np.array([[0,1,0],[1,0,1],[0,0,0]]))

    for i in range(len(mats)):
        temp_mat = np.flip(mats[i], axis = 1)
        mats.append(temp_mat)
    order = []
    stim_grid = []
    for i in range(len(mats)): 
        stim_grid.append([i,rotations[0]])
        stim_grid.append([i,rotations[1]])
        stim_grid.append([i,rotations[2]])
    if method == 1:
        for i in range(trial_size):
            order.append(i%2)
    if method == 2:
        for i in range(trial_size):
            x = rd.choices([0,1], k = 2)
            order.append(x[0])

    rd.shuffle(stim_grid)
    rd.shuffle(order)
    for t in range(trial_size):
        x = stim_grid[t][1]
        if order[t] == 1:
            tmat_t = mats[stim_grid[t][0]]
            tmat_q = rotMat(tmat_t,x)
        else:
            tmat_t = rd.choice(mats)
            tmat_q = rotMat(tmat_t,x,flip=True)
        tstims = presMat(tmat_t, tmat_q)    
        if x != 0: 
            [f_curve, s_curve] = curveLine(90, dir = x)
            stims = tstims + s_curve
            [resp,rt,acc,tooFast] = menRotTrial(stims, order[t], f_curve)
            # elif x == 2:
                # [wedge90,line1,line2,txt] = curveLine(180, loc_cent = False)
                # curve = curveLine(180)
        else: 
            [f_curve, s_curve] = curveLine(0)
            tstims.append(s_curve)
            [resp,rt,acc,tooFast] = menRotTrial(tstims, order[t], f_curve, match = True)


        if x == 0:
            cond = 0
        else:
            cond = 1 if x == 1 else -1 
        resp2 = 1 if resp == "m" else 0
        out=[sub,1,cond,order[t],round(rt,4),resp2,int(train),int(acc),t+1,rnd,tooFast]
        print(*out,sep=", ",file=fptr)
        fptr.flush()




### Memory span:
def runMemSpan(trial_size, target_size=[2,5], method = 1, train = False, rnd=1):
    target = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    # if train == True: 
    #     target = []
    #    for i in range(10): target.append(str(i))
    order = []
    size = []
    if method == 1:
        for i in range(trial_size):
            order.append(i%2)
            size.append(target_size[i%2])
    if method == 2:
        for i in range(trial_size):
            x = rd.choices([0,1], k = 2)
            order.append(x[0]%2)
            size.append(target_size[x[1]%2])
    rd.shuffle(order)
    rd.shuffle(size)
    for t in range(trial_size):
        letters = target
        q = rd.sample(letters, k = size[t])
        if order[t] == True:
            s = rd.choice(q)
            truth = True
        else:
            wrong_s = []
            for i in range(len(letters)):
                if letters[i] not in q: 
                    wrong_s.append(letters[i])
            s = rd.choice(wrong_s)
            truth = False
        q = " ".join(q)
        q_stim = visual.TextStim(
            win = win,
            text = q.upper(),
            pos = (0,0),
            color = [.9,.9,0]
        )
        s_stim = visual.TextStim(
            win = win,
            text = s.upper(),
            pos = (0,0),
            color = 'white'
        )
        # s_stim.size = q_stim.size = 5
        [resp,rt,acc,tooFast] = memSpanTrial(truth, q_stim, s_stim)

        cond = 0 if size[t] == target_size[0] else 1 
        resp2 = 1 if resp == "m" else 0
        out=[sub,3,cond,order[t],round(rt,4),resp2,int(train),int(acc),t+1,rnd, tooFast]
        print(*out,sep=", ",file=fptr)
        fptr.flush()



def mask():
    mask1 = visual.TextStim(
        win = win,
        text = "@",
        pos = (0,0),
        color = "white"
    )
    mask2 = visual.TextStim(
        win = win,
        text = "#",
        pos = (0,0),
        color = "white"
    )
    return(mask1, mask2)

def memSpanTrial(truth, q, s):
    x = visual.TextStim(
        win = win,
        text = "Press 'X' if the white letter was part of the yellow letter",
        pos = (-400,-475),
        color = "white"
    )
    m = visual.TextStim(
        win = win,
        text = "Press 'M' if the white letter was part of the yellow letter",
        pos = (400,-475),
        color = "white"
    )
    frameTimes=[60,30,60,1]  #at 60hz
    frame=[]
    tstim = [visual.TextStim(win,"+"), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    frame.append(visual.BufferImageStim(win,stim=[q, m, x]))
    tstim = [visual.TextStim(win,""), m, x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    frame.append(visual.BufferImageStim(win,stim=[s, m, x]))

    # frame.append(mask1)
    # frame.append(mask2)

    runFrames(frame,frameTimes,timerStart=3)
    [resp,rt,ac]=getResp(truth = truth)
    acc=feedback(ac,1)
    if rt < .2:
        warn()
        tooFast = 1
    else:
        tooFast = 0
    return(resp,rt,acc,tooFast)


### Inspection time:




def getRespInsTime(s, abortKey='9'):
    letters = ["a","s","d","f","g","h","j","k","l",abortKey]
    keys=event.getKeys(keyList=letters,timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=letters,timeStamped=timer)
    resp=keys[0][0]
    resp=resp.upper()
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    return([resp,rt])



def insTimeTrial(t, q, s):
    x = visual.TextStim(
        win = win,
        text = "Enter the letter you just saw \nFrom 'A' to 'L' on your keyboard",
        pos = (0,-475),
        color = "white"
    )

    frameTimes=[30,30,t,3,3,1]  #at 60hz
    frame=[]
    [mask1,mask2] = mask()
    tstim = [visual.TextStim(win,"+"), x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    tstim = [visual.TextStim(win,""), x]
    frame.append(visual.BufferImageStim(win,stim=tstim))
    frame.append(visual.BufferImageStim(win,stim=[q,x]))
    frame.append(visual.BufferImageStim(win,stim=[mask1,x]))
    frame.append(visual.BufferImageStim(win,stim=[mask2,x]))
    frame.append(visual.BufferImageStim(win,stim=[visual.TextStim(win,""),x]))

    runFrames(frame,frameTimes, timerStart=2)
    [resp,rt]=getRespInsTime(s)
    resp2 = int(resp==s)
    acc=feedback(resp2,1)
    return(resp,rt,acc)




def runInsTime(trial_size, rnd = 1):
    letters = ["A","S","D","F","G","H","J","K","L"]
    counter = 0
    if rnd == 1:
        t = 8
    else:
        t = 4
    for i in range(trial_size):
        x = rd.choice(letters)
        x.upper()
        q_stim = visual.TextStim(
            win = win,
            text = x,
            pos = (0,0),
            color = target_val
        )
        if i < 4:
            [resp,rt,acc] = insTimeTrial(20, q_stim, x)
        else:
            [resp,rt,acc] = insTimeTrial(t, q_stim, x)
            if acc == False:
                t += 1
                counter = 0
            else:
                counter += acc
                if counter == 2:
                    if t > 1: 
                        t -= 1
                    counter = 0
        out=[sub,0,t,x,round(rt,2),resp,"NA",int(acc),i+1,rnd,"NA"]
        print(*out,sep=", ",file=fptr)
        fptr.flush()
### Buffer:

def getRespBuffer(abortKey='9'):
    keys=event.getKeys(keyList=["x",abortKey],timeStamped=timer)
    if len(keys)==0:
        keys=event.waitKeys(keyList=("x",abortKey),timeStamped=timer)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    return("confirmed")


def warn():
    frameTimes=[60,60,60,60,60,1]  #at 60hz
    head_verts = [(-80, -50), (80, -50), (0,50)]
    tri = visual.ShapeStim(
        win, 
        fillColor='red',
        vertices=head_verts, 
        lineColor='white')
    txt = visual.TextStim(
        win = win,
        text = "!",
        pos = (-2.5,0),
        color = 'white',
        height = 100
    )
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.BufferImageStim(win,stim=[tri, txt]))
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Too fast!"))
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Pay attention! \n press 'X' to continue..."))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()


def expBuffer(exp, round = 1):
    frameTimes=[60,1]  #at 60hz
    frame=[]
    txt1= visual.TextStim(
        win = win,
        text = "Well done on so far!",
        pos = (0,150),
        color = [0,1,0]
    )
    txt0= visual.TextStim(
        win = win,
        text = "Press 'X' to continue...",
        pos = (0,-150),
        color = [0,1,0]
    )

    frame.append(visual.TextStim(win,""))
    frame.append(visual.BufferImageStim(win,stim=[txt0, txt1]))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
    txt0= visual.TextStim(
        win = win,
        text = "Press 'X' to begin...",
        pos = (0,-150),
        color = [0,1,0]
    )

    frame=[]
    if round == 2:
        if exp == 0:
            txt = "In the upcoming task, your objective again is to recognize the displayed letter and input it using the keyboard."
        if exp == 1:
            txt = "In the upcoming task, your objective again is to determine whether the presented grids are identical or distinct. Press 'M' for a match and 'X' for a difference."
        if exp == 2:
            txt = "In the upcoming task, your objective again is to determine if a backward letter is present among the forward-facing letters. Press 'M' if you find one and 'X' if none exists."
        if exp == 3:
            txt = "In the upcoming task, your objective again is to determine  whether the second displayed letter was part of the initial set of letters. Press 'M' if it was and 'X' if it wasn't."

        txt2= visual.TextStim(
            win = win,
            text = txt,
            pos = (0,150),
            color = [0,1,0]
        )
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=[txt0, txt2]))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()
        frameTimes=[60,1]  #at 60hz
        frame=[]



def trainBuffer(exp):
    frame=[]
    txt0= visual.TextStim(
        win = win,
        text = "Press 'X' to continue...",
        pos = (0,-250),
        color = [0,1,0]
    )
    if exp != 0:
        frameTimes=[30,1]  #at 60hz
        txt1= visual.TextStim(
            win = win,
            text = "Well done so far!",
            pos = (0,0),
            color = [0,1,0]
        )
        txt00= visual.TextStim(
            win = win,
            text = "Press 'X' to continue to the next task...",
            pos = (0,-150),
            color = [0,1,0]
        )
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=[txt1, txt00]))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()
        frame = []

    if exp == 1:
        frameTimes=[30,1]  #at 60hz
        mat = np.array([[1,0,0],[1,0,0],[0,0,0]])
        mat_same = rotMat(mat,0)
        mat_wrong = rotMat(mat, 1, flip = True)
        mat_rot = rotMat(mat,1)
        stim_og = presMat(mat, mat, ins = True)
        stim_same = presMat(mat, mat_same)    
        stims_wrong = presMat(mat, mat_wrong)    
        stims_rot = presMat(mat, mat_rot)
        txt1= visual.TextStim(
            win = win,
            text = "In this task, you will be presented with grids, similar to the example below:",
            pos = (0,150),
            color = [0,1,0]
        )
        stims = [txt0] + [txt1] + stim_og 
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt2 =visual.TextStim(
            win = win,
            text = "Occasionally, the grids represent the same object.",
            pos = (0,150),
            color = [0,1,0]
        )
        stims = [txt0] + [txt2] + stim_same 
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt3 =visual.TextStim(
            win = win,
            text = "Sometimes one grid may be a rotated version of the other.",
            pos = (0,350),
            color = [0,1,0]
        )
        [f_curve, s_curve] = curveLine(90, dir = 1)
        stims = [txt0] + [txt3] + stims_rot + s_curve 
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt4 =visual.TextStim(
            win = win,
            text = "In some instances, the grids display distinct objects.",
            pos = (0,100),
            color = [0,1,0]
        )
        stims = [txt0] + [txt4] + stims_wrong
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()
        
        frame=[]
        frame.append(visual.TextStim(win,""))
        txt5 =visual.TextStim(
            win = win,
            text = "Your task is to determine if the grids represent the same object or not. If they do, press 'M' for match. If not, press 'X' for mismatch.",
            pos = (0,100),
            color = [0,1,0]
        )
        frame.append(visual.BufferImageStim(win,stim=[txt0,txt5]))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()
    if exp == 2:
        frameTimes=[30,1]  #at 60hz
        stim1 = conjunct(0, 10, [10,10], "N")
        stim2 = conjunct(1, 10, [10,10], "N", ins = True)
        mat = np.array([[1,0,0],[1,0,0],[0,0,0]])
        txt1= visual.TextStim(
            win = win,
            text = "In this task, you will be presented with a series of letters, similar to the example below:",
            pos = (0,250),
            color = [0,1,0]
        )
        stims = [txt0] + [txt1] + stim1 
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt2 =visual.TextStim(
            win = win,
            text = "Occasionally, all the letters displayed are forwardfacing.",
            pos = (0,250),
            color = [0,1,0]
        )
        stims = [txt0] + [txt2] + stim1 
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt3 =visual.TextStim(
            win = win,
            text = "Other times, one of the letters may be facing backward.",
            pos = (0,250),
            color = [0,1,0]
        )
        stims = [txt0] + [txt3] + stim2
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        frame.append(visual.TextStim(win,""))
        txt5 =visual.TextStim(
            win = win,
            text = "Your task is to determine if a backward letter is present. If you find one, press 'M' for yes. If not, press 'X' for no.",
            pos = (0,100),
            color = [0,1,0]
        )
        frame.append(visual.BufferImageStim(win,stim=[txt0,txt5]))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

    if exp == 3:
        frameTimes=[30,1]  #at 60hz
        q_stim_5 = visual.TextStim(
            win = win,
            text = "MHPJR",
            pos = (0,0),
            color = [.9,.9,0]
        )
        q_stim_1 = visual.TextStim(
            win = win,
            text = "B",
            pos = (0,0),
            color = [.9,.9,0]
        )
        sr_stim = visual.TextStim(
            win = win,
            text = "P",
            pos = (0,0),
            color = 'white'
        )
        sw_stim = visual.TextStim(
            win = win,
            text = "V",
            pos = (0,0),
            color = 'white'
        )
        sr_stim2 = visual.TextStim(
            win = win,
            text = "B",
            pos = (0,0),
            color = 'white'
        )
        sw_stim2 = visual.TextStim(
            win = win,
            text = "W",
            pos = (0,0),
            color = 'white'
        )
        txt1= visual.TextStim(
            win = win,
            text = "In this task, you will be presented with a collection of letters, similar to the example below:",
            pos = (0,150),
            color = [0,1,0]
        )
        stims = [txt0] + [txt1] + [q_stim_5] 
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt2 =visual.TextStim(
            win = win,
            text = "Following this, you will be shown a single letter. \nYour task is to determine if this letter was also present in the previous collection.",
            pos = (0,150),
            color = [0,1,0]
        )
        stims = [txt0] + [txt2] + [sr_stim2] 
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt3 =visual.TextStim(
            win = win,
            text = "If the letter was present in the previous collection, press 'M'.",
            pos = (0,150),
            color = [0,1,0]
        )
        stims = [txt0] + [txt3] + [sr_stim]
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        txt4 =visual.TextStim(
            win = win,
            text = "If the letter was not present in the previous collection, press 'X'.",
            pos = (0,150),
            color = [0,1,0]
        )
        stims = [txt0] + [txt4] + [sw_stim]
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        frame.append(visual.TextStim(win,""))
        txt5 =visual.TextStim(
            win = win,
            text = "Occasionally, the collection may consist of just one letter being displayed.",
            pos = (0,150),
            color = [0,1,0]
        )

        stims = [txt0] + [txt5] + [q_stim_1]
        
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame = []
        frame.append(visual.TextStim(win,""))
        txt6 =visual.TextStim(
            win = win,
            text = "Likewise, when the subsequent letter is displayed, press 'M' if it matches the previous letter and 'X' if it doesn't.",
            pos = (0,150),
            color = [0,1,0]
        )

        frame.append(visual.BufferImageStim(win,stim=[txt0,txt6,sw_stim2]))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

    if exp == 0:
        frameTimes=[30,1]  #at 60hz
        txt1= visual.TextStim(
            win = win,
            text = "In this task, you will initially see a single letter, which will be masked subsequently.",
            pos = (0,150),
            color = [0,1,0]
        )
        txt9= visual.TextStim(
            win = win,
            text = "Your task is to recognize the letter and press the corresponding key on your keyboard.",
            pos = (0,0),
            color = [0,1,0]
        )
        txt10= visual.TextStim(
            win = win,
            text = "Press 'X' to see an example...",
            pos = (0,0),
            color = [0,1,0]
        )
        stims = [txt0] + [txt1] + [txt9]
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame = []
        frame.append(visual.TextStim(win,""))
        frame.append(txt10)
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()

        frame=[]
        frameTimes=[30,30,30,6,6,1]
        q_stim = visual.TextStim(
            win = win,
            text = "K",
            pos = (0,0),
            color = target_val
        )
        [mask1,mask2] = mask()
        frame.append(visual.TextStim(win,"+", color = "white"))
        frame.append(visual.TextStim(win,""))
        frame.append(q_stim)
        frame.append(mask1)
        frame.append(mask2)
        txt11= visual.TextStim(
            win = win,
            text = "Now, input the letter you observed on the screen.",
            pos = (0,150),
            color = [0,1,0]
        )
        frame.append(txt11)
        runFrames(frame,frameTimes, timerStart=2)
        [resp,rt]=getRespInsTime(0)
        frame=[]
        frameTimes=[30,1]
        letters = ["A","S","D","F","G","H","J","K","L"]
        q = " ".join(letters)
        txt15=visual.TextStim(
            win = win,
            text = "The duration for which the letter is displayed will decrease as you perform better.",
            pos = (0,200),
            color = [0,1,0]
        )
        txt16=visual.TextStim(
            win = win,
            text = "Only letters from the second row of the keyboard will be displayed. That is:",
            pos = (0,100),
            color = [0,1,0]
        )
        txt17=visual.TextStim(
            win = win,
            text = letters,
            pos = (0,-50),
            color = [.5,.5,0]
        )
        stims = [txt15] + [txt0] + [txt16] + [txt17]
        frame.append(visual.TextStim(win,""))
        frame.append(visual.BufferImageStim(win,stim=stims))
        runFrames(frame,frameTimes, timerStart=0)
        getRespBuffer()


    frame=[]
    frame.append(visual.TextStim(win,""))
    txt6 =visual.TextStim(
        win = win,
        text = "If you have any questions, feel free to ask. \nPress 'X' to start the task.",
        pos = (0,100),
        color = [0,1,0]
    )
    frame.append(txt6)
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()

'''
def intialBuffer():
    frameTimes=[30,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,"Welcome! \nPress press 'X' when ready..."))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
    txt = "Welcome to the Inspection Time Task. \nIn this task, a letter will be presented to you, followed by a mask. \nYour objective is to identify the letter that was presented. \nPlease enter the corresponding letter on the keyboard. \nIf you have any questions, please don't hesitate to ask the RA. \nPress 'X' to begin the task. "
    frameTimes=[60,1]  #at 60hz
    frame=[]
    frame.append(visual.TextStim(win,""))
    frame.append(visual.TextStim(win,txt))
    runFrames(frame,frameTimes, timerStart=0)
    getRespBuffer()
'''



header=['sub','task','condition','correct','rt','resp','block','accuracy','trial','round','2fast']
print(*header,sep=", ",file=fptr)
header=['sub','task','condition','correct','rt','resp','block','accuracy','trial','round','2fast']

fptr.flush()



runMemSpan(10, target_size=[1,5], method = 1, train = False, rnd = 2)





hz=round(win.getActualFrameRate())
size=win.size
win.close()
if useDB:
	stopExp(sessionID,hz,size[0],size[1],seed,dbConf)

core.quit()

