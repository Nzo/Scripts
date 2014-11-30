import maya.cmds as cmds
import maya.mel as mel

def autoPaintTargetShape():
# Thanks to kelsolaar for his help
    assert len(cmds.ls(sl=True)) == 2, 'Please select exactly two objects!'
    blendshape_node = cmds.blendShape(weight=(0, 1))
    mel.eval('artSetToolAndSelectAttr "artAttrCtx" ("blendShape.{0}.weightMap")'.format(blendshape_node))
    mel.eval('artAttrCtx -e -value 0 `currentCtx`')
    mel.eval('artAttrPaintOperation artAttrCtx Replace')
    mel.eval('artAttrCtx -e -clear `currentCtx`')
    mel.eval('artAttrCtx -e -value 1 `currentCtx`')
    

def extractUnlockShapes():
	base = cmds.ls(selection=True,tr=True)
	shapeName = cmds.ls(selection=True,dag=True,s=True,ni=True)
	blendName = cmds.listConnections(shapeName, d=False, s=True,type="blendShape")
	targetName = cmds.blendShape(blendName, q=True,t=True)
	for i in targetName:
	    if (cmds.getAttr(blendName[0]+'.'+i,lock=True)):
	        print (i + " lock")
	    else:
	        cmds.select(base ,replace=True)
	        cmds.setAttr(blendName[0]+'.'+i, 1)
	        dupShape = cmds.duplicate(rr=True)
	        cmds.rename( dupShape, i)
	        cmds.setAttr(blendName[0]+'.'+i, 0)

def applyDeltaToSelections():
	mySel= cmds.ls(sl=True)
	base= cmds.ls(selection=True, tail=2)
	blendName = cmds.blendShape()
	listLength = len(mySel)-2
	cmds.setAttr(blendName[0]+'.'+base[0], 1)
	for x in range(0,listLength):
	    i = mySel[x]
	    cmds.select(base[1] ,replace=True)
	    cmds.setAttr(blendName[0]+'.'+i, 1)
	    dupShape = cmds.duplicate(rr=True)
	    blendShapeTmp = cmds.blendShape( dupShape[0], i, weight=(0,1))
	    cmds.setAttr(blendName[0]+'.'+i, 0)
	    cmds.delete(dupShape[0])
	    cmds.select(i,replace=True)
	    cmds.delete(ch=True)
	cmds.setAttr(blendName[0]+'.'+base[0], 0)
	cmds.delete(blendName)
