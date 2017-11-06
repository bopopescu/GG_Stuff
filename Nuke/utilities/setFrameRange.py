##############################################################################
# 
#
## The Kazoops
#
##
## @author : EFRIZAL HARDIMAN
## @contact : efrizal.hardiman@gmail.com
##############################################################################

import nuke

def setFrameRange():
	ret = nuke.getFramesAndViews('Set Frame Range', '101-1000')
	getFrame = ret[0]
	convertFrame = nuke.FrameRange(getFrame)

	nuke.root().knob('first_frame').setValue(convertFrame.first())
	nuke.root().knob('last_frame').setValue(convertFrame.last())
	for i in nuke.selectedNodes():
		if i.Class() == 'Read':
			i.knob('first').setValue(convertFrame.first())
			i.knob('last').setValue(convertFrame.last())
			i.knob('origfirst').setValue(convertFrame.first())
			i.knob('origlast').setValue(convertFrame.last())

def main():
    setFrameRange()