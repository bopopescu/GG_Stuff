##############################################################################
# 
#
## CML
#
##
## @author : EFRIZAL HARDIMAN
## @contact : efrizal.hardiman@gmail.com
##############################################################################

import init

import os
import sys
import nuke
import nukescripts
import re
from glob import glob
from datetime import time
from datetime import date
from datetime import datetime

def dirCallbacks():
    callbacks = 'try:\n\treload(superModule)\nexcept:\n\timport superModule\nsuperModule.createOutDirs()'
    if nuke.toNode('WritePNG'):
        nuke.toNode('WritePNG').knob('beforeRender').setValue(callbacks)

def constantRange():
    for each in nuke.allNodes('Constant'):
        each['first'].setValue(1)
        each['last'].setValue(1000)

# CREATE FOLDER IF NOT EXISTS
def createOutDirs():
	trgDir = os.path.dirname( nuke.filename( nuke.thisNode() ) )
	if not os.path.isdir( trgDir ):
		os.makedirs( trgDir )

# ADDING TIME CODE
def addingTimeCode():
    try:
        writeMov = nuke.toNode('WriteMov')
        conn1 = writeMov.input(0).name()
        node1 = writeMov.input(0)
        
        if writeMov:
            if conn1.startswith('AddTimeCode'):
                pass
            elif not conn1.startswith('AddTimeCode'):
                times = nuke.createNode('AddTimeCode')
                times.setInput(0, node1)
                writeMov.setInput(0, times)
                times.setXpos(writeMov.xpos())
                times.setYpos(writeMov.ypos()-35) 
    except:
        pass
		

# GET FRAME RANGES FROM ALL READ NODES
def getAllFrameRanges():
    for each in nuke.allNodes('Read'):
        file = each['file'].evaluate()
        try:
            basename = os.path.basename(file)
            dirname = os.path.dirname(file)
            listAll = os.listdir(dirname)
            listAll.sort()
            # ''' EXCLUDE ALL EXTENSION .DB AND CREATE NEW LIST '''
            newlist = sorted( [ x for x in listAll if not x.endswith('.db')])
            firstList = newlist[0]
            lastList = newlist[-1]
            list1 = firstList.split('.')
            firstFrame = int( list1[-2] )
            each['first'].setValue(firstFrame)
            each['origfirst'].setValue(firstFrame)
            list2 = lastList.split('.')
            lastFrame = int( list2[-2] )
            each['last'].setValue(lastFrame)
            each['origlast'].setValue(lastFrame)
            # ''' SET ALL READ NODES '''
            each['on_error'].setValue('nearest frame')
        except:
            print each['name'].value() + ' has no valid folder or empty'
                
# CHANGE PADDING NAME TO '####'
def changePaddingName():
    for i in nuke.allNodes('Read'):
        try:
            # '''GET VALUE FROM ALL READ NODES'''
            getReadValue = i.knob('file').getValue()
            # '''GET DIRECTORY NAME OF ALL READ NODES'''
            dirname = os.path.dirname(getReadValue)
            # '''GET FILE NAME OF ALL READ NODES'''
            basename = os.path.basename(getReadValue)
            # '''GET EXTENSION FILE FROM FILE NAME'''
            splitExt = os.path.splitext(basename)[-1]
            # '''GET NAME FILE'''
            splitName = os.path.splitext(basename)[0]
            # '''GET PADDING NAME'''
            splitPadding = splitName.split('.')[-1]
            # '''GET NAME'''
            splitPaddingName = splitName.split('.')[0]
            # '''SET NEW PADDING FORMAT'''
            namePadding = '####'
            if len(splitPadding) == 4:
                # '''REPLACE OLD PADDING TO NEW PADDING'''
                newPadding = str.replace(basename, splitPadding, namePadding)
                # '''JOIN DIRECTORY NAME AND NEW FILE NAME'''
                newPath = os.path.join(dirname, newPadding).replace('\\','/')
                # '''THEN REPLACE NEW FILE NAME WITH NEW PADDING NAME'''
                newReadValue = i.knob('file').setValue(newPath)
        except:
            print each['name'].value() + ' cannot change the padding name because it has no valid folder or empty'
			
def changeNodes():
	newNodePath = nuke.toNode('CMLPath').knob('ShotOutput').evaluate()
	nodeExpression = '[value CMLPath.ShotOutput]'
	if newNodePath:
		for i in nuke.allNodes('Read'):
			try:
				oldPattern = i.knob('file').getValue().replace('/','\\')
				dirname = os.path.dirname(oldPattern).split('\\')[-1]
				basename = os.path.basename(oldPattern)
				suffixPath = os.path.join(dirname, basename)
				relievePath = os.path.relpath(oldPattern, newNodePath)
			except:
				print "the path already correct"
			try:
				if relievePath == suffixPath:
					joinPath = os.path.join(nodeExpression, relievePath).replace('\\','/')
					newReadValue = i.knob('file').setValue(joinPath)
					changePaddingName()
			except:
				changePaddingName()

# SAVE NUKE AS TEMP            
def saveNukeTemp():
    renderPath = nuke.toNode('path')['reconnectRead'].value()
    episode = renderPath.split('/')[3].lower()
    shot = renderPath.split('/')[4].lower()

    nukeName = episode+'_'+shot+'.nk'
    nukePath = 'N:/workspace/compositing/'+episode+'/CompFile'

    fullSaveTemp = os.path.join(nukePath,nukeName).replace('\\','/')
    if nuke.Root()['name'].value() == '':
        nuke.Root()['name'].setValue(fullSaveTemp)
        
#SETUP FOR NUKESCRIPTS GET START AND END FRAME        
def autoSetupNukescripts():
    # SET FIRST AND LAST FRAME BASED ON ACTOR READ NODES
    x = nuke.allNodes('Read')
    firstset = []
    lastset = []
    for each in x:
        # VALIDATE THE FOLDER IF EXIST
        try:
            gen = each['file'].evaluate()
            dir = os.listdir(os.path.dirname(gen))
            if gen.find('Actor') is not -1:
                first =  each['first'].value()
                last =  each['last'].value()
                firstset.append(first)
                lastset.append(last)
        except:
                print each['name'].value() + " doesn't have a valid directory"
    
    # SET THE NUKE FIRST AND LAST FRAME
    nuke.Root().knob('first_frame').setValue(int(min(firstset)))
    nuke.Root().knob('last_frame').setValue(int(max(lastset)))
    nuke.Root().knob('lock_range').setValue(1)\
    
def updateMovNode():
    cNode = nuke.toNode('WriteMov_DNXHR')
    movoutputnode = nuke.toNode('MovOutput')
    if cNode:
        stamp = cNode['Date'].value()
        mTime = os.path.getmtime("W:\Production\Comp_Library\Comp_Tools\CMLWrite_DNXHR.nk")
        nodeStamp = datetime.fromtimestamp(mTime)
        strStamp = str(nodeStamp)
        if stamp < strStamp:
            nuke.delete(cNode)
            nuke.scriptReadFile("W:\Production\Comp_Library\Comp_Tools\CMLWrite_DNXHR.nk")
            cNode = nuke.toNode('WriteMov_DNXHR')
            cNode.setInput(0, movoutputnode)
            cNode.setXpos(movoutputnode.xpos())
            cNode.setYpos(movoutputnode.ypos()+200)
            print 'current node is not latest'
        else:
            print 'current node is the latest'

def onSetup():
	addingTimeCode()
	changePaddingName()
	getAllFrameRanges()
	constantRange()
	autoSetupNukescripts()
    
# CALLBACKS WHEN SAVE THE NUKESCRIPTS  
def onSave():
    saveNukeTemp()
    dirCallbacks()
    getAllFrameRanges()
    changePaddingName()
    setTextFrameName()
    setOutput()
    autoSetupNukescripts()