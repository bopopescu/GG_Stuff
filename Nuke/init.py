#CML V.01

import os
import nuke
import nukescripts
import sys

# SET TOOLS PATH
global toolsPath
toolsPath = os.path.dirname(__file__)

# RETURN EVERYTHING IN DIRECTORY AND CHECK FOR THE DIRECTORY ONLY
onlyDir = [ f for f in os.listdir( toolsPath ) if os.path.isdir( os.path.join( toolsPath, f ))]
for eachDir in onlyDir:
	#ADD THE DIRECTORY AS PLUGIN
    nuke.pluginAddPath( eachDir )
	
# SET THE ROOT TO USE BOTH BASE AND PROXY FORMATS
# SET ROOT
nuke.addFormat("1280 720 0 0 1280 720 1 CML") 
nuke.knobDefault("Root.format", "CML")
nuke.knobDefault("Root.fps", "25")
#nuke.knobDefault("Root.onScriptLoad", "assetScript.onLoad()")

# SET ROTO
nuke.knobDefault("Roto.output","rgba")

# SET ADDTIMECODE
nuke.knobDefault("AddTimeCode.startcode", "00:00:00:00")
nuke.knobDefault("AddTimeCode.metafps", "false")
nuke.knobDefault("AddTimeCode.useFrame", "true")
nuke.knobDefault("AddTimeCode.fps", "25")
nuke.knobDefault("AddTimeCode.frame", "0")