# -*- coding: utf-8 -*-
# @File : 234.py
# @Date :  2020-09-02 18:14
# @Email :  {guojj@tongji.edu.cn/guojj01@gmail.com}
# @Author : guojj


###导入必要的模块
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import numpy as np
import os



class abaqusODBProcess(object):
    """基于python的Abaqus前后处理程序."""

    def __init__(self,odbPath):
        self._odb = openOdb(path=odbPath) #打开结果数据库

    @property
    def steps(self):
        """返回模型荷载步,编号规则stepName_number,number 从1到N"""
        totalSteps=self._odb.steps.keys()
        stepName=totalSteps[0].split('_')[0]
        numStep=len(totalSteps)
        return stepName,numStep

    @property
    def instance(self):
        """返回装配件实例"""
        print(self._odb.rootAssembly.instances.keys())

        return self._odb.rootAssembly.instances.keys()[1]

    @property
    def nodes(self):
        """返回模型节点列表，[[number1,x1,y1,z1],...]"""
        nodes = self._odb.rootAssembly.instances[self.instance].nodes
        nodeList=[[each.label]+list(each.coordinates) for each in nodes]
        return nodeList

    @property
    def elements(self):
        """返回模型单元列表,[[eleNum1,node1i,node1j,...],...]"""
        elements = self._odb.rootAssembly.instances[self.instance].elements
        eleList=[[each.label]+list(each.connectivity) for each in elements]
        return eleList

    def rfNodeResponse(self,nodedSetName,component):
        """
        返回参考点响应列表[[rx0,ry0,rz0],...]
        :param nodedSetName: 节点集名称
        :param component:分量名称,如‘U’，‘RF’等
        """
        endSet=self._odb.rootAssembly.nodeSets[nodedSetName]
        returnList = []
        stepName,numSteps=self.steps
        print(numSteps)
        for i1 in range(numSteps):
            flag = True
            j1 = 0
            while (flag):
                try:
                    frame = self._odb.steps[stepName+"_" + str(i1 + 1)].frames[j1]
                    j1 = j1 + 1
                    displacement = frame.fieldOutputs[component]
                    centerDisplacement = displacement.getSubset(region=endSet)
                    fieldValues = centerDisplacement.values
                    for v in fieldValues:
                        returnList.append(v.data)
                except:
                    flag = False
        return returnList

    def nodeDisp(self):
        """返回节点位移,dispXList,dispYList,dispZList"""
        stepName, numSteps = self.steps
        returnDict = {}
        for i1 in range(numSteps):
            flag = True
            j1 = 0
            while (flag):
                try:
                    frame = self._odb.steps[stepName +"_"+ str(i1 + 1)].frames[j1]
                    j1 = j1 + 1
                    displacement = frame.fieldOutputs['U'].values
                    for each in displacement:
                        if not returnDict.has_key(each.nodeLabel):
                            returnDict[each.nodeLabel] = []
                            returnDict[each.nodeLabel].append(each.data)
                        else:
                            returnDict[each.nodeLabel].append(each.data)
                except:
                    flag = False
        changeValue = [returnDict[1][i1 * 2] for i1 in range(len(returnDict[1]) / 2)]
        returnDict[1] = changeValue
        dispXList=[]
        dispYList=[]
        dispZList=[]
        for i1 in range(len(returnDict)):
            tempValueX=[each[0] for each in returnDict[i1+1]]
            tempValueY = [each[1] for each in returnDict[i1 + 1]]
            tempValueZ = [each[2] for each in returnDict[i1 + 1]]
            dispXList.append([i1+1]+tempValueX)
            dispYList.append([i1 + 1] + tempValueY)
            dispZList.append([i1 + 1] + tempValueZ)
        return dispXList,dispYList,dispZList

    def intPointResponse(self,responseType):
        """
        提取积分点响应
        responseType:响应类型
        """
        stepName, numSteps = self.steps
        returnDict = {}
        if responseType=='mises':
            for i1 in range(numSteps):
                flag = True
                j1 = 0
                while (flag):
                    try:
                        frame = self._odb.steps[stepName+"_" + str(i1 + 1)].frames[j1]
                        j1 = j1 + 1
                        displacement = frame.fieldOutputs['S'].values
                        for each in displacement:
                            if not returnDict.has_key(each.elementLabel):
                                returnDict[each.elementLabel] = []
                                returnDict[each.elementLabel].append(each.mises)
                            else:
                                returnDict[each.elementLabel].append(each.mises)
                    except:
                        flag = False
        elif responseType=='PEEQ':
            for i1 in range(numSteps):
                flag = True
                j1 = 0
                while (flag):
                    try:
                        frame = self._odb.steps[stepName+"_" + str(i1 + 1)].frames[j1]
                        j1 = j1 + 1
                        displacement = frame.fieldOutputs['PEEQ'].values
                        for each in displacement:
                            if not returnDict.has_key(each.elementLabel):
                                returnDict[each.elementLabel] = []
                                returnDict[each.elementLabel].append(each.data)
                            else:
                                returnDict[each.elementLabel].append(each.data)
                    except:
                        flag = False
        else:
            raise NameError("Please enter correct name:'mises' or'PEEQ'")
        num = len(returnDict)
        returnList = []
        for i2 in range(num):
            numj = len(returnDict[i2 + 1]) / 2
            tempj = [returnDict[i2 + 1][2 * each] for each in range(numj)]
            returnList.append(([i2 + 1] + tempj))
        return returnList
################################################################################
if __name__ == '__main__':
    odbPath = 'E:/abaqusModel/pythonProgramAbaqus/Job-pushOver.odb'
    instance=abaqusODBProcess(odbPath)
    ##节点及单元信息
    nodes=instance.nodes
    np.savetxt("postResults/nodes.txt",nodes,fmt='%d %.8f %.8f %.8f')
    elements=instance.elements
    np.savetxt("postResults/elements.txt", elements, fmt='%d')
    ##加载点力与位移时程
    nodedSetName = 'ASSEMBLY_CONSTRAINT-UPPERPLATE_REFERENCE_POINT'
    compDisp = 'U'
    comReactionForce = 'RF'
    rfDisp=instance.rfNodeResponse(nodedSetName,compDisp)
    np.savetxt('postResults/refDisp.txt',rfDisp,fmt='%f')
    rfForce = instance.rfNodeResponse(nodedSetName, comReactionForce)
    np.savetxt('postResults/refLoad.txt', rfForce, fmt='%f')
    ##节点位移时程
    dispXList, dispYList, dispZList = instance.nodeDisp()
    np.savetxt("postResults/dispX.txt",dispXList,fmt='%f')
    np.savetxt("postResults/dispY.txt",dispYList,fmt='%f')
    np.savetxt("postResults/dispZ.txt",dispZList,fmt='%f')
    ##单元积分点Mises应力
    responseType='mises'
    misesStress=instance.intPointResponse(responseType)
    np.savetxt("postResults/misesStress.txt", misesStress, fmt="%f")
    ##单元积分点等效塑性应变
    responseType1 = 'PEEQ'
    plasticStrain = instance.intPointResponse(responseType1)
    np.savetxt("postResults/PEEQ.txt", plasticStrain, fmt="%f")

