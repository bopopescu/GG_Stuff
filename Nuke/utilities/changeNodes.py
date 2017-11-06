##############################################################################
# 
#
## SONIC BOOM 2
#
#
##############################################################################

import re
import nuke
import os


def changePaddingName():
    for i in nuke.allNodes('Read'):
        namePadding = '####'
        getReadValue = i.knob('file').getValue()
        dirname = os.path.dirname(getReadValue)
        basename = os.path.basename(getReadValue)
        oldPadding = basename.split('.')[-2]
        splitExt = os.path.splitext(basename)[1]
        splitName = os.path.splitext(basename)[0]
        newPadding = str.replace(basename, oldPadding, namePadding)
        newPath = os.path.join(dirname, newPadding).replace('\\','/')
        newReadValue = i.knob('file').setValue(newPath)

def changeNodes():
    newNodePath = nuke.toNode('SonicBoom').knob('RenderLocation').evaluate()
    nodeExpression = '[value SonicBoom.RenderLocation]'
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
            
def main():
    changeNodes()
    
if __name__ == '__main__':
    main()