from maya import cmds, mel
import os
def switch2Vray():
	### load vray plugin
	cmds.loadPlugin('vrayformaya', quiet = True)
	cmds.pluginInfo('vrayformaya', edit = True, autoload = True)
	### change render drop down
	### change render drop down
	cmds.lockNode('defaultRenderGlobals', lock=False )
	cmds.setAttr("defaultRenderGlobals.currentRenderer", lock = False)	
	cmds.setAttr("defaultRenderGlobals.currentRenderer", 'vray', type = "string")
	mel.eval('unifiedRenderGlobalsWindow;')
	mel.eval('unifiedRenderGlobalsWindow;')
	mel.eval('fillSelectedTabForCurrentRenderer;')
	### change to vray shader
	shader = cmds.ls(type = ['blinn','phong','lambert'], l = True)
	removeShader = ['lambert1']
	for VPSHD in shader:
		if VPSHD.endswith('VPSHD'):
			removeShader.append(VPSHD)	
	for x in removeShader:
		shader.remove(x)
	cmds.select(shader)
	try:
		mel.eval('source "S:/LeonLoong/Scripts/LittleScript/maya2VRay.mel"')
	except:
		mel.eval('maya2VRay()')   	 
	### select vray shader, change shader attr
	vrayshader = cmds.ls(type = ['VRayMtl'], l = True)  
	for x in(vrayshader):
	    cmds.setAttr(x+'.reflectionGlossiness', 1)
	    cmds.setAttr(x+'.bumpMult', 1)
	    cmds.setAttr(x+'.diffuseColorAmount', 1)
	cmds.warning('V-Ray Switched')
		
def  LoadKAZPresets():
	### render sett
    mel.eval('loadNodePresets "KAZ_W";')
    mel.eval('vrayAddRenderElement rawGiChannel;')
    mel.eval('vrayAddRenderElement rawLightChannel;')
    mel.eval('vrayAddRenderElement rawReflectionChannel;')
    mel.eval('vrayAddRenderElement sampleRateChannel;')
    cmds.warning('KAZ_W Preset Loaded')	

def changeTextureAttribute():
	### texture input gamma  and texture filter
	texture_File = cmds.ls(type = ['file'], l = True)
	for x in (texture_File):
	     cmds.vray(x, "addAttributesFromGroup", x, 'vray_file_gamma', 1)
	     cmds.vray(x, "addAttributesFromGroup", x, 'vray_texture_filter', 1)
	### change bump to linear sRGB
	changeFile = []
	files = cmds.ls(type = 'file')
	lists = cmds.listConnections(files, plugs = True, source = False)
	for x in lists:
		if x.endswith('bumpMap'):
			bumpFile = cmds.listConnections(x)
			for y in bumpFile:
				changeFile.append(y)	
	
	bump_Node =cmds.ls(type ="bump2d")
	for x in (bump_Node):
		files = cmds.listConnections((x+".bumpValue"), s = True, d= False)
		for y in (files):
			changeFile.append(y)	
	for z in changeFile:
		cmds.setAttr(z+".colorProfile", 2)
	cmds.warning('Texture Input Gamma and Texture Filter')

def vraySky():
	mel.eval('vrayCreateVRaySky;')
	mel.eval('disconnectAttr VRaySky1.outColor vraySettings.cam_envtexBg;')
	mel.eval('disconnectAttr VRaySky1.outColor vraySettings.cam_envtexRefract;')
	
def createCamera():
	### camera
	cmds.camera(displayFilmGate = False, displayResolution = True, overscan = 1.3, filmFit = 'Fill')
	cmds.vray('addAttributesFromGroup', 'camera1|cameraShape1', 'vray_cameraPhysical', 1)
	cmds.setAttr("cameraShape1.vrayCameraPhysicalOn", 1)
	cmds.setAttr("cameraShape1.vrayCameraPhysicalFNumber", 2.8)
	cmds.setAttr("cameraShape1.vrayCameraPhysicalShutterSpeed", 100)
	cmds.setAttr('camera1.translate', 61.73, 37.172, 51.209, type = 'double3')
	cmds.setAttr('camera1.rotate', -14.4, 50, 0, type = 'double3')
	cmds.rename('camera1' , 'RENDER')
	mel.eval('lookThroughModelPanel RENDER modelPanel4;')

def createLight():
    ### light
	cmds.file("Q:/Production/Tech/KAZ_Maya/_Lighting/Lv1ExtLight.ma", i = True, type = "mayaAscii",mergeNamespacesOnClash = False, rpr = "Lv1ExtLight", options = "v=0;", pr = True)
	cmds.file("Q:/Production/Tech/KAZ_Maya/_Lighting/ExtDomeLight.ma", i = True, type = "mayaAscii",mergeNamespacesOnClash = False, rpr = "ExtDomeLight", options = "v=0;", pr = True)
	cmds.delete('VRayLightDome1')
	cmds.setAttr("LIGHTRIG.translateZ", -24.784)
	cmds.setAttr("LIGHTRIG.rotateY", -42.252)
	cmds.setAttr("VRayLightDome.translateZ",  -6.389015)
	mel.eval('setAttr "VRaySunShape1.intensityMult" 0.03;')
	mel.eval('setAttr "VRaySunShape1.turbidity" 2.5;')
	mel.eval('setAttr "VRaySunShape1.sizeMultiplier" 1;')
	mel.eval('setAttr "VRaySunShape1.skyModel" 3;')


def addSubdiv():
    ### add subdiv
    grpGRP = cmds.ls(sl=True)
    if grpGRP == []:
        cmds.warning('Please Select Group')
    else:
        mel.eval('vray objectProperties add_single VRayDisplacement')
        mel.eval('vray addAttributesFromGroup vrayDisplacement vray_opensubdiv 1;')
        mel.eval('setAttr "vrayDisplacement.vrayOsdSubdivDepth" 2;')
        cmds.rename('vrayDisplacement', 'OpenSubdiv_2')
        
def saveMayaSHDFile():
    scenePath = cmds.file(query=True,sceneName=True).split("KAZ")[0]+'Shader'
    if not os.path.exists(scenePath):   
        os.makedirs(scenePath)
    sceneName = cmds.file(query=True,sceneName=True).split("/")[-1].rpartition(".")[0].split("_PRD")[0]
    cmds.file(rename = ("%s/%s"%(scenePath , sceneName)))
    cmds.file(save = True, f=True) 
	
def saveImageFile():
	if cmds.window('Double_Click_Your_Name', exists = True):
		cmds.deleteUI('Double_Click_Your_Name')
	cmds.window('Double_Click_Your_Name')
	cmds.paneLayout()
	global name
	name = cmds.textScrollList( append = ['Ankan', 'ED', 'Leon', 'Mega'])
	cmds.textScrollList(name, e=True, dcc = doubleClickAction)
	cmds.showWindow('Double_Click_Your_Name')

def doubleClickAction():
	nameSelect = cmds.textScrollList(name, query =True, selectItem = True)[0]
	print nameSelect
	epNumber = cmds.file(query=True,sceneName=True).split('/')[5]
	epName = cmds.file(query=True,sceneName=True).split("/")[-1].rpartition(".")[0].split("KAZ_P_")[-1]
	cmds.vray("vfbControl", "-saveimage", "S:/Eduard/From %s/%s_Props_%s.png"%(nameSelect , epNumber , epName))
	cmds.warning('Image File Saved in S:/Eduard/From %s/%s_Props_%s.png'%(nameSelect , epNumber , epName))
	
def cleanFile():
	deleteObject = ['RENDER', 'LIGHTRIG', 'VRayLightDome', 'vrayRE_Raw_GI*', 'vrayRE_Raw_Light*', 'vrayRE_Raw_Reflection*', 'vrayRE_Sample_Rate*', 'EPC_3k_File', 'VRayPlaceEnvTex1'] 
	mel.eval('vrayDeleteSky;')
	for each in deleteObject:
		if cmds.objExists(each):
			cmds.delete(each)	
	shapesInSel = cmds.ls(type = 'mesh')
	shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
	shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)
	for i in shaders:
		try:
			materialInfoNode = cmds.ls(cmds.listConnections(i), typ='materialInfo')[-1]
			cmds.connectAttr('%s.message' % i, '%s.texture' % materialInfoNode, nextAvailable=True)
		except:
			pass
	mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
	cmds.warning('File Cleaned')
	
def saveMayaPDRFile():
    None