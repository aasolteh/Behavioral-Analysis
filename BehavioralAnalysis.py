from psychopy import visual, event, gui, core
import numpy as np
import constants as const
import itertools
import random

def calc_stimuli_pos(inner_radius, outer_radius, num_of_points):
    degs_inner = 2*np.pi/num_of_points * np.arange(num_of_points)
    degs_outer = 2*np.pi/num_of_points * np.arange(num_of_points) + np.math.pi/6
    patt_inner = np.array([[np.cos(i), np.sin(i)] for i in degs_inner])
    patt_outer = np.array([[np.cos(i), np.sin(i)] for i in degs_outer])
    inner = inner_radius * patt_inner
    outer = outer_radius * patt_outer
    glob  = np.array([[0, 0]])
    points = np.concatenate((glob, inner, outer))
    return points


def get_state(time_s):
    time_ms = time_s * 1000
    if(time_ms <= const.FIXATION):
        return "fixation"
    elif(time_ms <= const.FIXATION + const.PRESENTATION):
        return "presentation"
    else:
        return "answer"


def wait_for_key(pressedKey):
    waitkeypress = True
    while waitkeypress:
        key = event.getKeys()
        if 'q' in key:
            waitkeypress = False
            pressedKey.append('q')
        elif 'w' in key:
            waitkeypress = False
            pressedKey.append('w')
        elif 'p' in key:
            waitkeypress = False
            pressedKey.append('p')
        elif 'o' in key:
            waitkeypress = False
            pressedKey.append('o')

def wait_for_space():
    waitkeypress = True
    while waitkeypress:
        key = event.getKeys()
        if 'space' in key:
            waitkeypress = False
            return key

def get_input():
    expName = 'behavioralAnalysis'  # from the Builder filename that created this script
    expInfo = {'subjID': '', 'dominantHand': '', 'dominantEye': '', 'subjSex': '', 'subjAge': '', 'subjEducation': ''}
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    expInfo['expName'] = expName
    return expInfo
    
def isclose(a, b, rel_tol=1e-04, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def run_behavioral(numOfBlocks):
    window = visual.Window(size = (1920, 1080), color = (-1, -1, -1), screen = 1)
    redDot = visual.Polygon(window, radius=5, edges=32, fillColor = (255, 0, 0), lineColor = (255, 0, 0), units='pix')

    stimFolder      = "Supplementary Material/"
    leftMessage     = "KbLeft.jpg"
    rightMessage    = "KbRight.jpg"
    distToMonitor   = 55
    pix2cm          = 36.6
    innerDegree     = 4
    outerDegree     = 7
    globDegreeSize  = 2.5
    innerDegreeSize = 4
    outerDegreeSize = 6
    innerRadius     = np.math.tan(innerDegree /180 * np.math.pi) * distToMonitor * pix2cm
    outerRadius     = np.math.tan(outerDegree /180 * np.math.pi) * distToMonitor * pix2cm
    globRadius      = 0
    stimuliNumber   = 13
    stimuli_pool    = calc_stimuli_pos(innerRadius, outerRadius, (stimuliNumber - 1) / 2)
    stimuli_name    = ["0.bmp", "10.bmp", "20.bmp", "30.bmp", "40.bmp", "50.bmp", "60.bmp", "70.bmp", "80.bmp"]
    shuffledStimPool= calc_stimuli_pos(innerRadius, outerRadius, (stimuliNumber - 1) / 2)

    handsOrder = ['l', 'l', 'r', 'r']
    reactionTime = []
    stimulusIndex = []
    usedHand = []
    stimulusPos = []

    subjectInfo   = get_input()
    pressedKey = []
    fp = open('810100376' + subjectInfo['subjID'] + '.csv','w')
    trialClock = core.Clock()
    data = []
    for block in range(numOfBlocks):
        random.shuffle(handsOrder)
        for order in handsOrder:
            if order == 'l':
                instructionStimulus = visual.ImageStim(window, image = stimFolder + leftMessage, pos = [0,0])
            elif order == 'r':
                instructionStimulus = visual.ImageStim(window, image = stimFolder + rightMessage, pos = [0,0])
            instructionStimulus.draw()
            window.flip()
            wait_for_space()
            indexStimuli = 0
            np.random.shuffle(shuffledStimPool)
            random.shuffle(stimuli_name)
            allPermutations = list(itertools.product(shuffledStimPool, stimuli_name))
            random.shuffle(allPermutations)
            while indexStimuli < len(allPermutations): # each trial, made up of 2*numOfPoints stimulis
                usedHand.append(order)
                state = const.FIXATION_STATE
                resetTimer = True
                stimulusIndex.append((allPermutations[indexStimuli])[1])
                stimulusPos.append((np.where(stimuli_pool == (allPermutations[indexStimuli])[0])[0])[1] + 1)
                while state != "answer": # each of stimuli representations
                    if(resetTimer):
                        initTime = trialClock.getTime()
                        resetTimer = False
                    currentTime = trialClock.getTime()
                    state = get_state(currentTime - initTime)
                    if(state == const.FIXATION_STATE):
                        redDot.draw()
                        window.flip()
                    elif(state == const.PRESENTATION_STATE):
                        if isclose((np.linalg.norm((allPermutations[indexStimuli])[0])), innerRadius):
                            stimSize = np.math.tan(innerDegreeSize /180 * np.math.pi) * distToMonitor * pix2cm
                        elif isclose((np.linalg.norm((allPermutations[indexStimuli])[0])), outerRadius):
                            stimSize = np.math.tan(outerDegreeSize /180 * np.math.pi) * distToMonitor * pix2cm
                        elif isclose((np.linalg.norm((allPermutations[indexStimuli])[0])), globRadius):
                            stimSize = np.math.tan(globDegreeSize /180 * np.math.pi) * distToMonitor * pix2cm
                        imageStimulus = visual.ImageStim(window, image = stimFolder + (allPermutations[indexStimuli])[1], pos = [0, 0], size = stimSize, units='pix')
                        imageStimulus.pos = (((allPermutations[indexStimuli])[0])[0], ((allPermutations[indexStimuli])[0])[1])
                        imageStimulus.draw()
                        window.flip()
                        continue
                    elif(state == const.ANSWER_STATE):
                        redDot.draw()
                        window.flip()
                        wait_for_key(pressedKey)
                        reactionTime.append(1000 * trialClock.getTime() - 1000 * initTime - 500)
                        continue
                indexStimuli = indexStimuli + 1
    fp.write('sbj,stm,rt,key,pos,uhnd,hndns,eye,sex,age,edu\n')

    for i in range(len(pressedKey)):
        fp.write('810100376' + subjectInfo['subjID']+','+stimulusIndex[i]+','+str(reactionTime[i])+','+pressedKey[i]+','+str(stimulusPos[i])+','+usedHand[i]+','+subjectInfo['dominantHand']+','+subjectInfo['dominantEye']+','+subjectInfo['subjSex']+','+subjectInfo['subjAge']+','+subjectInfo['subjEducation']+'\n')
    fp.flush()


if __name__ == "__main__":
    numOfBlocks = 4
    run_behavioral(numOfBlocks)