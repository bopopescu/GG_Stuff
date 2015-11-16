### select multiple shader, strip front and back string

from maya import cmds, mel

selected_obj = cmds.ls(sl = True)

for x in(selected_obj):
	cmds.rename(x, elem.strip('Front_'+'_Back'))
