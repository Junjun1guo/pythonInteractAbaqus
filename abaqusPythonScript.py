import os
import shutil
##########################################################################
########################---参数设置---####################################
thick=0.03 #弯曲板厚度(m)
upperPlateThick=0.1 #上下固定板厚度
height=1.5 #板高度(m)
width=1.5 #板宽度(m)
tapHeight=0.1 #不变宽度高度（m)
middleHeight=0.3 #中间段高度(m)
middleWidth=0.6 #中间段宽度(m)
numPlate=5 #板个数(m)
distance=0.2 #板间隔距离
numStep=1 #荷载步数
stepDisp=0.6 #每个荷载步位移增量
seedSize=0.03 #网格尺寸
maxInc=0.05 #每个荷载步增量大小
##########################################################################
########################---清除历史结果---#################################
import fnmatch
listName=os.listdir(os.getcwd())
for fileName in listName:
    try:
        if fnmatch.fnmatch(fileName,'Job-pushOver.*'):
            os.remove(fileName)
    except:
        os.system('taskkill /f /t /im '+"Job-pushOver.023")
##########################################################################
########################---abaqus脚本文件---##############################

fileName="runAbaqus.py"
os.remove(fileName)
f= open(fileName, "a+")
#######################################
#########---导入必要的模块---#########

f.write( "#############################\n")
f.write( "from abaqus import *\n")
f.write( "from abaqusConstants import *\n")
f.write( "from caeModules import *\n")
f.write( "from odbAccess import *\n")
f.write( "import regionToolset\n")
# """
######################################
#########---初始化---#################
f.write( "#############################\n")
f.write( "session.viewports[\"Viewport: 1\"].setValues(displayedObject=None)\n")
######################################
#########---建立模型---################
f.write( "#############################\n")
f.write( "mdb.models.changeKey(fromName=\"Model-1\",toName=\"steelPlate Frame\")\n")
f.write( "plateModel=mdb.models[\"steelPlate Frame\"]\n")
######################################
#########---生成部件---################
f.write( "#############################\n")
f.write( "bendPlateSketch_1=plateModel.ConstrainedSketch(name=\"bendPlateSketch_1\",sheetSize=2)\n")
xyCoords1=[(-0.5*width,tapHeight),(-0.5*width,0),(0.5*width,0),(0.5*width,tapHeight),
           (0.5*middleWidth,0.5*height-0.5*middleHeight),(0.5*middleWidth,0.5*height+0.5*middleHeight),
           (0.5*width,height-tapHeight),(0.5*width,height),(-0.5*width,height),
           (-0.5*width,height-tapHeight),(-0.5*middleWidth,0.5*height+0.5*middleHeight),
           (-0.5*middleWidth,0.5*height-0.5*middleHeight),(-0.5*width,tapHeight)]
for j1 in range(len(xyCoords1)-1):
    f.write("bendPlateSketch_1.Line(point1="+str(xyCoords1[j1])+",point2="+str(xyCoords1[j1+1])+")\n")

f.write( "bendPlatePart_1=plateModel.Part(name=\"bendPlatePart_1\",dimensionality=THREE_D,type=DEFORMABLE_BODY)\n")
f.write( "bendPlatePart_1.BaseShell(sketch=bendPlateSketch_1)\n")
for i1 in range(numPlate-1):
    f.write("bendPlatePart_"+str(i1+2)+"=plateModel.Part(name=\"bendPlatePart_"+
            str(i1+2)+"\",objectToCopy=bendPlatePart_1)\n")
####################
f.write( "bottomPlateSketch=plateModel.ConstrainedSketch(name=\"bottomPlate\",sheetSize=2)\n")
xyCoords1=[(-0.5*width,0),(0.5*width,0)]
extrudeValue=distance*(numPlate+1)
f.write("bottomPlateSketch.Line(point1="+str(xyCoords1[0])+",point2="+str(xyCoords1[1])+")\n")
f.write( "bottomPlatePart=plateModel.Part(name=\"bottomPlatePart\",dimensionality=THREE_D,type=DEFORMABLE_BODY)\n")
f.write( "bottomPlatePart.BaseShellExtrude(sketch=bottomPlateSketch, depth="+str(extrudeValue)+")\n")
f.write("upperPlatePart=plateModel.Part(name=\"upperPlatePart\",objectToCopy=bottomPlatePart)\n")
######################################
# """
#########---定义材料---################
f.write( "#############################\n")
f.write( "elasPlasticMaterial=plateModel.Material(name=\"elasPlasticMaterial\")\n")
f.write( "elasPlasticMaterial.Elastic(table=((210000000,0.3),))\n")
stressStrainTable=((345000,0),(471000,0.15),(480000,1))
f.write( "elasPlasticMaterial.Plastic(table="+str(stressStrainTable)+")\n")
#####################################
#########---创建截面---###############
f.write( "#############################\n")
f.write( "bendPlateSection=plateModel.HomogeneousShellSection(name=\"bendPlateSection\","
         "material=\"elasPlasticMaterial\",thickness="+str(thick)+")\n")
f.write( "fixPlateSection=plateModel.HomogeneousShellSection(name=\"fixPlateSection\","
         "material=\"elasPlasticMaterial\",thickness="+str(upperPlateThick)+")\n")
#####################################
#########---截面指定---###############
f.write( "#############################\n")
for i2 in range(numPlate):
    f.write("bendPlateFace_"+str(i2+1)+"=(bendPlatePart_"+str(i2+1)+".faces,)\n")
    f.write("bendPlatePart_"+str(i2+1)+".SectionAssignment(region=bendPlateFace_"+str(i2+1)+","
            "sectionName=\"bendPlateSection\")\n")
f.write("bottomPlateFaces=(bottomPlatePart.faces,)\n")
f.write("bottomPlatePart.SectionAssignment(region=bottomPlateFaces,sectionName=\"fixPlateSection\")\n")
f.write("upperPlateFaces=(upperPlatePart.faces,)\n")
f.write("upperPlatePart.SectionAssignment(region=upperPlateFaces,sectionName=\"fixPlateSection\")\n")
######################################
#########---装配部件---###############
f.write( "#############################\n")
f.write("rootAssembly=plateModel.rootAssembly\n")
for i3 in range(numPlate):
    f.write("bendInstance_"+str(i3+1)+"=rootAssembly.Instance(name=\"bendPlateAssembly_"+str(i3+1)+"\","
            "part=bendPlatePart_"+str(i3+1)+",dependent=ON)\n")
f.write("bottomInstance=rootAssembly.Instance(name=\"bottomPlateAssembly\",part=bottomPlatePart,dependent=ON)\n")
f.write("upperInstance=rootAssembly.Instance(name=\"upperPlateAssembly\",part=upperPlatePart,dependent=ON)\n")
for i4 in range(numPlate):
    f.write("rootAssembly.translate(instanceList=('bendPlateAssembly_"+str(i4+1)+"', ),"
        " vector=(0.0, 0.0,"+str(distance*(i4+1))+"))\n")
f.write("rootAssembly.translate(instanceList=('upperPlateAssembly', ), vector=(0.0,"+str(height)+",0.0))\n")

f.write("assemblyPart=rootAssembly.InstanceFromBooleanMerge(name='assemblyPart', instances=(")
for i5 in range(numPlate):
    f.write("bendInstance_"+str(i5+1)+",")
f.write("\nbottomInstance,upperInstance,),originalInstances=SUPPRESS,domain=GEOMETRY)\n")
######################################
#########---荷载步设置---##############
f.write( "#############################\n")
aa="pushOver_"+str(1)
f.write("plateModel.StaticStep(name=\""+aa+"\",previous='Initial', initialInc="+str(maxInc)+","
        " maxInc="+str(maxInc)+",nlgeom=ON)\n")
for i6 in range(numStep-1):
    previousName="pushOver_"+str(i6+1)
    currentName="pushOver_"+str(i6+2)
    f.write("plateModel.StaticStep(name=\"" + currentName + "\",previous=\"" + previousName + "\","
            " initialInc="+str(maxInc)+", maxInc="+str(maxInc)+",nlgeom=ON)\n")
######################################
#########---耦合设置--##############
f.write( "#############################\n")
f.write("refPointid=rootAssembly.ReferencePoint(point="+str((0,height,0))+").id\n")
f.write("refPointRegion=rootAssembly.Set(referencePoints=(rootAssembly.referencePoints[refPointid],), name='refPointSet')\n")
points=tuple([((0,height,distance*(i7+0.5)),) for i7 in range(numPlate+1)])
f.write("assemblyTopFaces = assemblyPart.faces.findAt"+str(points)+"\n")
f.write("topFameRegion=regionToolset.Region(faces=assemblyTopFaces)\n")
f.write("plateModel.Coupling(name='Constraint-upperPlate',controlPoint=refPointRegion,"
        "surface=topFameRegion,couplingType=KINEMATIC,influenceRadius=WHOLE_SURFACE)\n")
######################################
#########---边界条件设置--#############
f.write( "#############################\n")
pointsBC=tuple([((0,0,distance*(i7+0.5)),) for i7 in range(numPlate+1)])
f.write("assemblyBottomFaces = assemblyPart.faces.findAt"+str(pointsBC)+"\n")
f.write("bottomFameRegion=regionToolset.Region(faces=assemblyBottomFaces)\n")
f.write("plateModel.DisplacementBC(name='initBC', createStepName='Initial',region=bottomFameRegion,"
        "u1=SET, u2=SET, u3=SET, ur1=SET,ur2=SET, ur3=SET)\n")
#############################################
#########---pushOver荷载设置--################
f.write( "#############################\n")
f.write("plateModel.DisplacementBC(name='pushOver',createStepName='pushOver_1',region=refPointRegion,u3="+str(stepDisp)+")\n")
for i8 in range(numStep-1):
    stepName="pushOver_"+str(i8+2)
    u3=(i8+2)*stepDisp*(-1)**(i8+1)
    f.write("plateModel.boundaryConditions['pushOver'].setValuesInStep(stepName=\""+str(stepName)+"\",u3="+str(u3)+")\n")
#############################################
#########---网格划分设置--####################
f.write( "#############################\n")
######网格尺寸设置
f.write("meshPart=plateModel.parts[\"assemblyPart\"]\n")
f.write("seedEdges=meshPart.edges\n")
f.write("meshPart.seedEdgeBySize(edges=seedEdges,size="+str(seedSize)+")\n")
######划分控制设置
f.write("assemblyFaces=assemblyPart.faces\n")
f.write("assemblyFaces=meshPart.setMeshControls(regions=assemblyFaces,technique=STRUCTURED)\n")
######单元类型设置
f.write("eleType1=mesh.ElemType(elemCode=S4R)\n")
f.write("eleType2=mesh.ElemType(elemCode=S3)\n")
f.write("meshRegion=regionToolset.Region(faces=(assemblyPart.faces),)\n")
f.write("meshPart.setElementType(regions=meshRegion, elemTypes=(eleType1, eleType2))\n")
######网格划分
f.write("meshPart.generateMesh()\n")
#############################################
#########---任务设置--########################
f.write( "#############################\n")
f.write("mdb.Job(name='Job-pushOver', model='steelPlate Frame', multiprocessingMode=DEFAULT, numCpus=4,numDomains=4, numGPUs=1)\n")
f.write( "mdb.jobs['Job-pushOver'].submit(consistencyChecking=OFF)\n")
# """
######################################
f.close()
#######################################
os.system('abaqus CAE script=runAbaqus.py')
# os.system('abaqus CAE noGUI=runAbaqus.py')
############################################
######结果数据库处理
os.system('abaqus CAE noGUI=abaqusODBProcess.py')
###########################################
############################################
######结果后处理

