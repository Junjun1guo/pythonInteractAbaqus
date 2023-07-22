#-*-coding: UTF-8-*-
#####Units: Length-m, Force-kN, mass-ton, Stress-kpa(10e-3MPa), g=9.81m/s2
#####Units: Length-mm, Force-N, mass-ton, Stress-Mpa, g=9810mm/s2 pho=ton/mm3
#########################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com/guojj01@gmail.com
#  Environemet: Successfully executed in python 3.8
#  Date: 2021-09-19
#########################################################################
########################---导入必要模块---#################################
import os
import shutil
import numpy as np
from abaqus import *
from abaqusConstants import *#导入abaqus常量
from symbolicConstants import *#导入abaqus符号常量
from caeModules import *#导入CAE各模块
from odbAccess import *#odb操作模块
import regionToolset#集合选择
###########---1---基于abaqus环境进行计算----#################################
numStep=10 #荷载步数
maxInc=0.05 #每个荷载步增量大小,总量为1
stepDisp=20 #每个荷载步位移大小(mm)
PlateSeedSize=5 #钢板网格尺寸(mm)
RodSeedSize=5 #连接杆网格尺寸(mm)
trianglePlateTopWidth=100 #钢板顶边宽度(mm)
trianglePlateBottomWidth=500#梯形钢板底部宽度(mm)
trianglePlateHeight=600#梯形钢板高度(mm)
rodRaidus=20#连接杆半径(mm)
fy=406.307  #钢材屈服强度(Mpa)
fu=723.320  #钢材极限强度(Mpa)
E=1.91E+05 #钢材弹性模量(Mpa)
epsilon=0.103  #最大强度对应的应变
shellThinkness=15 ##三角钢板厚度(mm)
slotHeight=100 #滑槽内部高度(mm)
slotThickness=20#滑槽厚度(mm)
slotDepth=200 #滑槽深度(mm)
#########################################################################
########################---清除历史结果---#################################
import fnmatch #用于文件名称匹配
listName=os.listdir(os.getcwd())#获取当前文件夹路文件目录
for fileName in listName:
    try:
        if fnmatch.fnmatch(fileName,'Job-pushOver.*'):
            os.remove(fileName)#清除历史abaqus数据
    except:
        os.system('taskkill /f /t /im '+"Job-pushOver.023")#杀死进程中abaqus任务
##########################################################################
###########################---初始化模型---#################################
session.viewports["Viewport: 1"].setValues(displayedObject=None)#视图设置
mdb.models.changeKey(fromName="Model-1",toName="selfCenteringSteelDamper")#修改模型名称
steelDamperModel=mdb.models["selfCenteringSteelDamper"]#模型变量
#########################################################################
###########################---生成部件---##################################
####---三角钢板---
trianglePlateSketch_1=steelDamperModel.ConstrainedSketch(name="trianglePlateSketch_1",sheetSize=2000)#设置草图绘制
trianglePlateSketch_1.Line(point1=(0,0),point2=(trianglePlateBottomWidth, 0))
upperCoord=(trianglePlateBottomWidth-trianglePlateTopWidth)*0.5
trianglePlateSketch_1.Line(point1=(trianglePlateBottomWidth, 0),point2=(trianglePlateBottomWidth-upperCoord,trianglePlateHeight))
trianglePlateSketch_1.Line(point1=(trianglePlateBottomWidth-upperCoord,trianglePlateHeight),point2=(upperCoord,trianglePlateHeight))
trianglePlateSketch_1.Line(point1=(upperCoord,trianglePlateHeight),point2=(0, 0))
trianglePlatePart_1=steelDamperModel.Part(name="trianglePlatePart_1",dimensionality=THREE_D,type=DEFORMABLE_BODY)#生成部件
trianglePlatePart_1.BaseShell(sketch=trianglePlateSketch_1)#生成部件壳体
####---连接杆---
connectingRodSketch=steelDamperModel.ConstrainedSketch(name="connectingRodSketch",sheetSize=2000)#设置草图绘制
connectingRodSketch.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0,rodRaidus))
connectingRodPart=steelDamperModel.Part(name="connectingRodPart",dimensionality=THREE_D,type=DEFORMABLE_BODY)
connectingRodPart.BaseSolidExtrude(sketch=connectingRodSketch, depth=trianglePlateTopWidth)
####---滑槽---
connectingSlotSketch=steelDamperModel.ConstrainedSketch(name="connectingSlotSketch",sheetSize=2000)#设置草图绘制
connectingSlotSketch.Line(point1=(0,0),point2=(slotThickness, 0))
connectingSlotSketch.Line(point1=(slotThickness, 0),point2=(slotThickness, slotHeight))
connectingSlotSketch.Line(point1=(slotThickness, slotHeight),point2=(slotThickness+rodRaidus*2, slotHeight))
connectingSlotSketch.Line(point1=(slotThickness+rodRaidus*2, slotHeight),point2=(slotThickness+rodRaidus*2,0))
connectingSlotSketch.Line(point1=(slotThickness+rodRaidus*2,0),point2=(slotThickness*2+rodRaidus*2, 0))
connectingSlotSketch.Line(point1=(slotThickness*2+rodRaidus*2, 0),point2=(slotThickness*2+rodRaidus*2,slotHeight+slotThickness))
connectingSlotSketch.Line(point1=(slotThickness*2+rodRaidus*2,slotHeight+slotThickness),
                          point2=(0,slotHeight+slotThickness))
connectingSlotSketch.Line(point1=(0,slotHeight+slotThickness),point2=(0,0))
slotPart=steelDamperModel.Part(name="slotPart",dimensionality=THREE_D,type=DEFORMABLE_BODY)#生成部件
slotPart.BaseSolidExtrude(sketch=connectingSlotSketch, depth=slotDepth)
#########################################################################
###########################---材料定义---##################################
####---弹性材料---
elasticMaterial=steelDamperModel.Material(name="elasticMaterial")#线弹性材料名称定义
elasticMaterial.Elastic(table=((E, 0.3), ))#线弹性材料定义
####---弹塑性材料---
elasPlasticMaterial=steelDamperModel.Material(name="elasPlasticMaterial")#弹塑性材料名称定义
elasPlasticMaterial.Elastic(table=((E,0.3),))#弹塑性材料弹性部分定义
stressStrainTable=((fy,0),(fu,epsilon),(fu+1,1))#塑性应力应变关系表格
elasPlasticMaterial.Plastic(table=stressStrainTable)#弹塑性材料塑性部分定义
#########################################################################
###########################---创建截面---##################################
###---三角钢板弹塑性截面---
bendPlateSection=steelDamperModel.HomogeneousShellSection(name="bendPlateSection",
    material="elasPlasticMaterial",thickness=shellThinkness)#建立各向同性壳截面
###---连接杆弹性截面---
solidSection=steelDamperModel.HomogeneousSolidSection(name='solidSection', material='elasticMaterial')
#########################################################################
###########################---截面指定---##################################
###---三角钢板截面指定---
trianglePart= steelDamperModel.parts['trianglePlatePart_1']
bendPlateFace=(trianglePart.faces,)#选取三角板所有的面
trianglePart.SectionAssignment(region=bendPlateFace, sectionName='bendPlateSection')#截面指定
###---连接杆截面指定---
rod_region=(connectingRodPart.cells,)
connectingRodPart.SectionAssignment(region=rod_region, sectionName='solidSection')#连接杆截面指定
###---滑槽截面指定---
slot_region=(slotPart.cells,)
slotPart.SectionAssignment(region=slot_region, sectionName='solidSection')#滑槽截面指定
#########################################################################
###########################---装配件---###################################
###---三角钢板装配件---
rootAssembly=steelDamperModel.rootAssembly#根装配件
#生成三角形钢板装配件实例
trianglePlateInstance_1=rootAssembly.Instance(name="trianglePlateInstance_1",part=trianglePlatePart_1,dependent=ON)
#生成连接杆装配件实例
connectingRod_instance=rootAssembly.Instance(name="connectingRod_instance",part=connectingRodPart,dependent=ON)
#连接杆与钢板装配实例
###移动连接杆到钢板顶部
fixedPoint=trianglePlateInstance_1.vertices[0]
movablePoint=connectingRod_instance.InterestingPoint(edge=connectingRod_instance.edges[0], rule=MIDDLE)
rootAssembly.CoincidentPoint(fixedPoint=fixedPoint, movablePoint=movablePoint)
###转动连接杆
rootAssembly.rotate(instanceList=('connectingRod_instance', ),
    axisPoint=((trianglePlateBottomWidth-trianglePlateTopWidth)*0.5,0,0.0), axisDirection=(0.0,1, 0.0), angle=90.0)
###沿X轴平行移动连接杆
connectingRod_instance.ConvertConstraints()#将连接杆实例转换为绝对位置
rootAssembly.translate(instanceList=('connectingRod_instance', ), vector=(trianglePlateTopWidth, 0.0,0.0))
####对连接杆与钢板进行布尔并运算
trianglePlateRod_instance=rootAssembly.InstanceFromBooleanMerge(name='trianglePlateRod_instance', instances=(trianglePlateInstance_1,
    connectingRod_instance,),keepIntersections=OFF, originalInstances=SUPPRESS,domain=GEOMETRY)
###滑槽装配件实例
slot_instance=rootAssembly.Instance(name="slot_instance",part=slotPart,dependent=ON)
fixedPoint=trianglePlateRod_instance.vertices[2]
movablePoint=slot_instance.InterestingPoint(edge=slot_instance.edges[2],rule=MIDDLE)
rootAssembly.CoincidentPoint(fixedPoint=fixedPoint,movablePoint=movablePoint)
rootAssembly.rotate(instanceList=('slot_instance',),axisPoint=(0,0,0),axisDirection=(0,1,0),angle=90)
slot_instance.ConvertConstraints()
rootAssembly.translate(instanceList=('slot_instance',),vector=((trianglePlateBottomWidth-slotDepth)*0.5,0,0))
rootAssembly.translate(instanceList=('slot_instance',),vector=(0,trianglePlateHeight+2*rodRaidus+slotThickness+5,0))
#########################################################################
###########################---荷载步设置---################################
####---创建荷载步---
steelDamperModel.StaticStep(name='pushOver_1', previous='Initial', initialInc=maxInc, maxInc=maxInc, nlgeom=ON)
for i1 in range(numStep-1):
    previousName = "pushOver_" + str(i1 + 1)
    currentName = "pushOver_" + str(i1 + 2)
    steelDamperModel.StaticStep(name=currentName,previous=previousName, initialInc=maxInc, maxInc=maxInc,nlgeom=ON)
#########################################################################
###########################---场变量输出设置---#############################
#场变量输入名称修改
steelDamperModel.fieldOutputRequests.changeKey(fromName='F-Output-1',toName='Selected Field Outputs')
#########################################################################
###########################---耦合设置---##################################
###---参考点与顶部线耦合设置---
refPointCoord=(trianglePlateBottomWidth*0.5,trianglePlateHeight+2*rodRaidus+5+slotThickness,0)#参考点坐标
refPointid=rootAssembly.ReferencePoint(refPointCoord).id#建立参考点
#建立参考点集合
refPointRegion=rootAssembly.Set(referencePoints=(rootAssembly.referencePoints[refPointid],), name='refPointSet')
slotUpFace = slot_instance.faces.findAt((refPointCoord,),)#通过边上一点选择边
region_slotUpFace=regionToolset.Region(faces=slotUpFace)#集合域
steelDamperModel.Coupling(name='coupling_refAndTopFace',controlPoint=refPointRegion,surface=region_slotUpFace,
                          couplingType=KINEMATIC,influenceRadius=WHOLE_SURFACE)#建立控制点与边之间分布耦合
#接触面设置
leftSlotNode=(trianglePlateBottomWidth*0.5,trianglePlateHeight,rodRaidus)
leftSlotSurface=slot_instance.faces.findAt((leftSlotNode,))#通过面上一点选取面
rootAssembly.Surface(side1Faces=leftSlotSurface,name="leftSlotSurfaceInstance")
region_leftSlotSurface=rootAssembly.surfaces['leftSlotSurfaceInstance']
####################
rightSlotNode=(trianglePlateBottomWidth*0.5,trianglePlateHeight,-rodRaidus)
rightSlotSurface=slot_instance.faces.findAt((rightSlotNode,))#通过面上一点选取面
rootAssembly.Surface(side1Faces=rightSlotSurface,name="rightSlotSurfaceInstance")
region_rightSlotSurface=rootAssembly.surfaces['rightSlotSurfaceInstance']
####################
rodSurfaceNode=(trianglePlateBottomWidth*0.5,trianglePlateHeight+2*rodRaidus,0)
rodSurface=trianglePlateRod_instance.faces.findAt((rodSurfaceNode,))
rootAssembly.Surface(side1Faces=rodSurface,name="rodSurfaceInstance")
region_rodSurface=rootAssembly.surfaces['rodSurfaceInstance']
# ###法向耦合约束设置
frictionless_interaction=steelDamperModel.ContactProperty('Frictionless')
frictionless_interaction.TangentialBehavior(formulation=FRICTIONLESS)
steelDamperModel.SurfaceToSurfaceContactStd(name='leftNormalInter',createStepName='Initial', master=region_leftSlotSurface,
    slave=region_rodSurface, sliding=FINITE, interactionProperty='Frictionless')
steelDamperModel.SurfaceToSurfaceContactStd(name='rightNormalInter',createStepName='Initial', master=region_rightSlotSurface,
    slave=region_rodSurface, sliding=FINITE, interactionProperty='Frictionless')
#########################################################################
###########################---边界条件设置---##############################
###---约束边界条件---
bottomPointCoord=(trianglePlateBottomWidth*0.5,0,0)#底边上一点
plateBottomEdge = trianglePlateRod_instance.edges.findAt((bottomPointCoord,),)#通过边上一点选择边
region_bottomEdge=regionToolset.Region(edges=plateBottomEdge)#集合域
steelDamperModel.DisplacementBC(name='initBC', createStepName='Initial',region=region_bottomEdge,
                                u1=SET, u2=SET, u3=SET, ur1=SET,ur2=SET, ur3=SET)#底边固接
steelDamperModel.DisplacementBC(name='refPointConstraint', createStepName='Initial',region=refPointRegion,
                                u1=SET,u2=SET,u3=UNSET,ur1=SET,ur2=SET,ur3=SET)
#########################################################################
###########################---PushOver荷载设置---##########################
region_pushOver = rootAssembly.sets['refPointSet']#参考点集
# 沿整体坐标系Z做加载100mm，创建pushover位移荷载
steelDamperModel.DisplacementBC(name='pushover', createStepName='pushOver_1', region=region_pushOver, u3=stepDisp)
for i2 in range(numStep-1):
    stepName = "pushOver_" + str(i2 + 2)
    u3 = (i2 + 2) * stepDisp * (-1) ** (i2 + 1)
    steelDamperModel.boundaryConditions['pushover'].setValuesInStep(stepName=stepName, u3=u3)#随后荷载步修改
#########################################################################
###########################---网格划分---##################################
###---钢板部件网格划分---
meshPart=steelDamperModel.parts['trianglePlateRod_instance']#选取需要划分网格的部件(对部件进行网格划分)
plate_findNode1=(0,0,0)
plate_findNode2=(trianglePlateBottomWidth*0.5+1.5*trianglePlateTopWidth,trianglePlateHeight,0)#两对角点需求四条线
plateEdges=trianglePlateRod_instance.edges.findAt((plate_findNode1,),(plate_findNode2,))
meshPart.seedEdgeBySize(edges=plateEdges,size=PlateSeedSize)#指定钢板划分网格最大尺寸mm
plateFaces_findNode=(0,0,0)
plateFace=trianglePlateRod_instance.faces.findAt((plateFaces_findNode,),)
plateFaceRegion=(plateFace,)
eleType1=mesh.ElemType(elemCode=S4R)#单元类型设置
eleType2=mesh.ElemType(elemCode=S3)#单元类型设置
meshPart.setElementType(regions=plateFaceRegion, elemTypes=(eleType1, eleType2))#单元类型指定
###---连接杆网格划分---
rod_findNode=(trianglePlateBottomWidth*0.5,trianglePlateHeight,0)
rodCells=trianglePlateRod_instance.cells.findAt((rod_findNode,),)
rodCellRegion=(rodCells,)
rodEdge_findNode1=((trianglePlateBottomWidth-trianglePlateTopWidth)*0.5,trianglePlateHeight,0)
rodEdge_findNode2=(0.5*trianglePlateBottomWidth+1.5*trianglePlateTopWidth,trianglePlateHeight,0)
rodEdges=trianglePlateRod_instance.edges.findAt((rodEdge_findNode1,),(rodEdge_findNode2,))
meshPart.seedEdgeBySize(edges=rodEdges,size=RodSeedSize)#指定连接杆网格最大尺寸mm
elemType1 = mesh.ElemType(elemCode=C3D8I)
elemType2 = mesh.ElemType(elemCode=C3D6)
elemType3 = mesh.ElemType(elemCode=C3D4)
meshPart.setElementType(regions=rodCellRegion, elemTypes=(eleType1, eleType2,elemType3))#单元类型指定
meshPart.generateMesh()#生成装配件实例网格
###---滑槽网格划分---
meshPart_slot=steelDamperModel.parts['slotPart']#选取需要划分网格的部件(对部件进行网格划分)
slot_findNode=(trianglePlateBottomWidth*0.5,trianglePlateHeight+2*rodRaidus+slotThickness,0)
slotCells=slot_instance.cells.findAt((slot_findNode,),)
slotCellRegion=(slotCells,)
slotEdges=slot_instance.edges
meshPart_slot.seedEdgeBySize(edges=slotEdges,size=RodSeedSize)#指定连接杆网格最大尺寸mm
elemType1 = mesh.ElemType(elemCode=C3D8I)
elemType2 = mesh.ElemType(elemCode=C3D6)
elemType3 = mesh.ElemType(elemCode=C3D4)
meshPart_slot.setElementType(regions=slotCellRegion, elemTypes=(eleType1, eleType2,elemType3))#单元类型指定
meshPart_slot.generateMesh()#生成装配件实例网格
#########################################################################
###########################---任务设置---##################################
# mdb.Job(name='Job-pushOver', model='selfCenteringSteelDamper',multiprocessingMode=DEFAULT,
#         numCpus=12,numDomains=12, numGPUs=1)#任务参数设置
# mdb.jobs['Job-pushOver'].submit(consistencyChecking=OFF)#提交任务



#########################################################################
#########################################################################





