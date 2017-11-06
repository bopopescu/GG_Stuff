import os, nuke

def reloadAllNodes(*args):
    x=nuke.allNodes('Read')
    for y in x: y["reload"].execute()