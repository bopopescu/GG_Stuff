prj=str(sys.argv[1])
nuke.scriptOpen(prj)
print "="*len(prj)
print prj
print "="*len(prj)
first_frame = int(nuke.Root().knob('first_frame').value())
last_frame = int(nuke.Root().knob('last_frame').value())
for i in nuke.allNodes():
    if i.Class()=="Write":
        if i['name'].getValue()=='WriteMov_DNXHR':
            nuke.execute(i, first_frame, last_frame)
nuke.scriptClose()