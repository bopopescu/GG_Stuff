#CML

import init

import os
import nuke
import nukescripts
import glob
from datetime import time
from datetime import date
from datetime import datetime

import superModule
import readFromWrite
import reloadAllNodes
import setFrameRange
import nukeOpenDialog

# LOAD ALL PYTHON SCRIPT IN PYTHON FOLDER
pyDir = os.listdir( os.path.join( init.toolsPath,'python' ) )
pythonList = [ x.split ('.')[0] for x in pyDir if x.endswith ( 'py' ) ]
# for u in pythonList:
    # nukemenu = nuke.menu( 'Nodes' ).addMenu( 'CMLPython' ).addCommand( str(u), getattr(__import__ (u), u ) )
    
nuke.menu( 'Nodes' ).addMenu( 'CMLPython' ).addCommand( 'Reload All Nodes', 'reloadAllNodes.reloadAllNodes()', 'F10' )
nuke.menu( 'Nodes' ).addMenu( 'CMLPython' ).addCommand( 'Reconnect to Path', 'superModule.changeNodes()', '' )

# LOAD ALL GIZMOS
gizmodir = os.listdir(os.path.join( init.toolsPath, 'gizmos' ))
gizmolist = [ x.split ( '.' )[0] for x in gizmodir if x.endswith ( 'gizmo' )]
for o in gizmolist:
    toolbar = nuke.menu( 'Nodes' ).addMenu( 'CMLGizmo' ).addCommand(str(o) )
    
    
# ADDING MENU
nuke.menu( 'Nuke' ).addCommand( 'CML/Nuke Custom Panel', 'nukeOpenDialog.main()', 'ctrl+i' )
nuke.menu( 'Nuke' ).addCommand( 'CML/CML Setup', 'superModule.onSetup()', 'F9' )
nuke.menu( 'Nuke' ).addCommand( 'CML/Read From Write', 'readFromWrite.readFromWrite()', 'shift+r' )
nuke.menu( 'Nuke' ).addCommand( 'CML/Set Frame Range', 'setFrameRange.main()', 'shift+f' )
nuke.menu( 'Nuke' ).addCommand( 'CML/Update Mov Writer', 'setFrameRange.updateMovNode()', '' )