# -*- coding: utf-8 -*-
# @File : 234.py
# @Date :  2020-09-02 18:14
# @Email :  {guojj@tongji.edu.cn/guojj01@gmail.com}
# @Author : guojj


###导入必要的模块
import numpy as np
import pyvista as pv
import pygmsh
import ctypes
import os
import shutil
import time
import pyqtgraph as pg
import array
from numba import jit
import meshio
import re
import json
from saveDataToSqlite import SaveData

class prePostPlot(object):
    """模型及结果显示类"""
    def __init__(self,dbPath):
        self.saveInstance = SaveData(dbPath)

    def prePlot(self):
        """前处理模型展示"""
        nodes=self.saveInstance.getAllNode()
        elements=self.saveInstance.getAllEle()
        nodesProcess=prePostPlot.strToListConvert(nodes,'coords','float')
        elementsProcess=prePostPlot.strToListConvert(elements,'connectivity','int')
        prePostPlot.staticPlot(nodesProcess,elementsProcess)

    def postPlot(self,comp,colorValue,saveName,sleepValue):
        """后处理结果绘制"""
        nodes = self.saveInstance.getAllNode()
        elements = self.saveInstance.getAllEle()
        nodesProcess = prePostPlot.strToListConvert(nodes, 'coords', 'float')
        elementsProcess = prePostPlot.strToListConvert(elements, 'connectivity', 'int')
        if comp=="mises":
            response=self.saveInstance.getAllMises()
            responsePorcess = prePostPlot.strToListConvert(response, 'mises', 'float')
        elif comp=="PEEQ":
            response = self.saveInstance.getAllPEEQ()
            responsePorcess = prePostPlot.strToListConvert(response, 'PEEQ', 'float')
        nodeDisp=self.saveInstance.getAllDisp()
        dispXProcess=prePostPlot.strToListConvert(nodeDisp, 'dispX', 'float')
        dispYProcess=prePostPlot.strToListConvert(nodeDisp, 'dispY', 'float')
        dispZProcess = prePostPlot.strToListConvert(nodeDisp, 'dispZ', 'float')
        prePostPlot.dynamicPlot(nodesProcess,elementsProcess,dispXProcess,dispYProcess
                                ,dispZProcess,responsePorcess,colorValue,saveName,sleepValue)

    @staticmethod
    def dynamicPlot(nodes,elements,dispX,dispY,dispZ,varValue,colorValue,saveName,sleepValue):
        """"""
        ##绘图窗口设置
        user32 = ctypes.windll.user32
        screensizex, screensizey = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        plotter = pv.Plotter(shape=(1,1), border=True, window_size=[int(screensizex), int(screensizey)])
        plotter.set_background(color="white")
        ##数据格式处理
        vertices=np.array(nodes)
        elementProcess = [[len(each)] + list(map(lambda item: item - 1, each)) for each in elements]
        faces = np.hstack(elementProcess)
        surf = pv.PolyData(vertices, faces)
        scales = np.array([varValue[j1][0] for j1 in range(len(varValue))])
        ##动态图绘制
        plotter.add_mesh(surf, show_edges=False, scalars=scales, edge_color="blue", interpolate_before_map=True,
                         cmap="jet", clim=[0, colorValue], show_scalar_bar=True)
        plotter.show(interactive=False, auto_close=False)
        plotter.add_axes()
        plotter.camera_position = (2, 2, -2)
        plotter.open_gif(saveName+'.gif')
        for i1 in range(len(varValue[0]) - 1):
            scaless = np.array([varValue[j1][i1] for j1 in range(len(varValue))])
            pts = np.array([[dispX[j1][i1] + vertices[j1][0], dispY[j1][i1] + vertices[j1][1], \
                             dispZ[j1][i1] + vertices[j1][2]] for j1 in range(len(dispX))])
            plotter.update_scalars(scaless)
            plotter.update_coordinates(pts)
            plotter.write_frame()
            time.sleep(sleepValue)
        plotter.close()

    @staticmethod
    def staticPlot(nodes,elements,showNodes=False,showEle=False):
        """
        静态图形绘制
        """
        vertices=np.array(nodes)
        elementProcess=[[len(each)]+list(map(lambda item:item-1,each)) for each in elements]
        faces=np.hstack(elementProcess)
        surf = pv.PolyData(vertices, faces)
        ##绘图窗口设置
        user32 = ctypes.windll.user32
        screensizex, screensizey = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        plotter = pv.Plotter(shape=(1,1), border=True, window_size=[int(1 * screensizex),
                            int(1 * screensizey)])
        plotter.set_background(color="white")
        ##坐标轴绘制
        arrowX=pv.Arrow(start=(0,0,0),direction=(1,0,0),tip_length=0.3,tip_radius=0.1,
                        shaft_radius=0.05,scale=0.1)
        arrowY=pv.Arrow(start=(0,0,0),direction=(0,1,0),tip_length=0.3,tip_radius=0.1,
                        shaft_radius=0.05,scale=0.1)
        arrowZ=pv.Arrow(start=(0,0,0),direction=(0,0,1),tip_length=0.3,tip_radius=0.1,
                        shaft_radius=0.05,scale=0.1)
        plotter.add_mesh(arrowX, color="red", show_edges=False)
        plotter.add_mesh(arrowY, color="green", show_edges=False)
        plotter.add_mesh(arrowZ, color="blue", show_edges=False)
        ##图形绘制
        plotter.add_mesh(surf, show_edges=True, edge_color="blue",style='surface')
        if showNodes==True:
            labelRange = [(i1 + 1) for i1 in range(len(vertices))]
            plotter.add_point_labels(vertices,labelRange, bold=False, point_size=0,
                font_size=16,text_color="red",font_family="times",show_points=False,shape=None,tolerance=1.0)
        if showEle==True:
            pass
        plotter.show(interactive=True, auto_close=False)

    @staticmethod
    def strToListConvert(strList,keys,types):
        """
        pass
        将字符化列表转为数字列表，'[1,2,3]'to [1,2,3]
        其中strList为字典列表，keys为键值，types为转换目标类型
        """
        temp1=[each[keys][1:-1].split() for each in strList]
        returnList=[list(map(float,each)) for each in temp1]
        if types=='float':
            finalList=returnList
        elif types=='int':
            finalList=[list(map(eval(types),each)) for each in returnList]
        else:
            print("types must be float or int!")
        return finalList

    @staticmethod
    def intervalValue(maxValue,numbers):
        """
        返回间隔线间隔大小
        maxValue-最大值
        numbers-分割线个数
        """
        b = len(str(int(maxValue)))
        if b==1 and int(maxValue)==0:
            interval = round(maxValue /numbers, 2)
            i3=2
            while(interval==0):
                interval=round(maxValue /numbers, i3+1)
                i3=i3+1

        elif b==1 and int(maxValue)!=0:
            interval = int(maxValue /numbers)
        else:
            loc = maxValue / 10 ** (b - 1)
            interval = int(loc) * 0.2 * 10 ** (b - 1)
        return interval

    def dispForcePlot(self,saveName,timeSleep,disp=None,force=None):
        """滞回曲线绘制"""
        if disp==None and force==None:
            dispForce= self.saveInstance.getRefResponse()
            dispX= np.array(prePostPlot.strToListConvert(dispForce, 'refDisp', 'float'))[:,2]
            forceY = np.array(prePostPlot.strToListConvert(dispForce, 'refLoad', 'float'))[:, 2]
        else:
            dispX=disp
            forceY=force
        ###绘图窗口设置

        user32 = ctypes.windll.user32
        screensizex, screensizey = 0.9*user32.GetSystemMetrics(0), 0.9*user32.GetSystemMetrics(1)
        plotter = pv.Plotter(shape=(1, 1), border=True, window_size=[int(screensizex), int(screensizey)])
        plotter.set_background(color="white")
        ###数据格式处理
        maxDisp=1.1*max(np.abs(dispX))
        maxForce = max(np.abs(forceY))
        screenRatio=user32.GetSystemMetrics(0)/float(user32.GetSystemMetrics(1))
        ratio=screenRatio*maxForce/float(maxDisp)
        ###坐标轴绘制
        plotter.camera_position = [(0, 0, 5 * maxForce), (0, 0, 0), (0, 1, 0)]
        lineX= np.array([[-1.2*ratio*maxDisp,0, 0], [1.2*ratio*maxDisp,0, 0]])
        arrayXUp= np.array([[1.15*ratio*maxDisp,0.02*maxForce, 0], [1.2*ratio*maxDisp,0, 0]])
        arrayXDown = np.array([[1.15 * ratio * maxDisp, -0.02 * maxForce, 0], [1.2 * ratio * maxDisp, 0, 0]])
        lineY = np.array([[0, -1.2*maxForce, 0], [0, 1.2*maxForce, 0]])
        arrayYLeft = np.array([[-0.02*maxForce, 1.12*maxForce, 0], [0, 1.2*maxForce, 0]])
        arrayYRight = np.array([[0.02 * maxForce, 1.12 * maxForce, 0], [0, 1.2 * maxForce, 0]])
        plotter.add_lines(lineX, color="k", width=2)
        plotter.add_lines(lineY, color="k", width=2)
        plotter.add_lines(arrayXUp, color="k", width=2)
        plotter.add_lines(arrayXDown, color="k", width=2)
        plotter.add_lines(arrayYLeft, color="k", width=2)
        plotter.add_lines(arrayYRight, color="k", width=2)
        ###坐标标签绘制
        plotter.add_point_labels(np.array([1.8*maxForce,-0.1*maxForce,0]),labels=["disp. (m)"],
                                 text_color="red",font_size=20,font_family='times',fill_shape=False,
                                 shape=None)
        plotter.add_point_labels(np.array([-0.4*maxForce, 1.12* maxForce, 0]), labels=["force (kN)"],
                                 text_color="red", font_size=20, font_family='times', fill_shape=False,
                                 shape=None)
        ###间隔大小
        intervalX=prePostPlot.intervalValue(maxDisp,5)
        intervalY = prePostPlot.intervalValue(maxForce, 5)
        ###分割线绘制
        bottomLine=np.array([[-1*ratio*maxDisp,-1.1*maxForce, 0], [1*ratio*maxDisp,-1.1*maxForce, 0]])
        upLine = np.array([[-1 * ratio * maxDisp, 1.1 * maxForce, 0], [1 * ratio * maxDisp, 1.1 * maxForce, 0]])
        leftLine = np.array([[-1 * ratio * maxDisp, -1.1 * maxForce, 0], [-1 * ratio * maxDisp, 1.1 *maxForce, 0]])
        rightLine = np.array([[1 * ratio * maxDisp, -1.1 * maxForce, 0], [1 * ratio * maxDisp, 1.1 * maxForce, 0]])
        plotter.add_lines(bottomLine, color="k", width=1)
        plotter.add_lines(upLine, color="k", width=1)
        plotter.add_lines(leftLine, color="k", width=1)
        plotter.add_lines(rightLine, color="k", width=1)

        indexX=0
        while((indexX*intervalX)<(maxDisp-intervalX)):
            indexX=indexX+1
            posVertical = np.array([[ratio*intervalX*indexX, -1.1 * maxForce, 0],
                                    [ratio*intervalX*indexX, 1.1 * maxForce, 0]])
            negVertical = np.array([[-ratio*intervalX * indexX, -1.1 * maxForce, 0],
                                    [-ratio*intervalX * indexX, 1.1 * maxForce, 0]])
            plotter.add_lines(posVertical, color="grey", width=0.1)
            plotter.add_lines(negVertical, color="grey", width=0.1)
            textPos=ratio*intervalX*(indexX-1)
            plotter.add_point_labels(np.array([textPos+0.8*intervalX*ratio, -1.2 * maxForce, 0]),
                                     labels=[str(intervalX*indexX)], text_color="k", font_size=15,
                                     font_family='times', fill_shape=False, shape=None)
            plotter.add_point_labels(np.array([-textPos -1.2 * intervalX * ratio, -1.2 * maxForce, 0]),
                                     labels=[str(-intervalX * indexX)], text_color="k", font_size=15,
                                     font_family='times', fill_shape=False, shape=None)
        plotter.add_point_labels(np.array([maxForce*0.01, -1.2 * maxForce, 0]),
                                 labels=[str(0)], text_color="k", font_size=15,
                                 font_family='times', fill_shape=False, shape=None)

        indexY = 0
        while ((indexY * intervalY) < (maxForce-intervalY)):
            indexY = indexY + 1
            posHorizontal = np.array([[-1 * ratio * maxDisp, indexY*intervalY, 0],
                                      [1 * ratio * maxDisp, indexY*intervalY, 0]])
            negHorizontal = np.array([[-1 * ratio * maxDisp, -indexY * intervalY, 0],
                                      [1 * ratio * maxDisp, -indexY * intervalY, 0]])
            plotter.add_lines(posHorizontal, color="grey", width=0.1)
            plotter.add_lines(negHorizontal, color="grey", width=0.1)
            textPos =  intervalY * (indexY - 1)
            plotter.add_point_labels(np.array([-1.15 * ratio * maxDisp, textPos+0.9*intervalY, 0]),
                                     labels=[str(intervalY*indexY)],text_color="k", font_size=15,
                                     font_family='times', fill_shape=False,shape=None)
            plotter.add_point_labels(np.array([-1.15 * ratio * maxDisp, -textPos-1.1*intervalY, 0]),
                                     labels=[str(-intervalY * indexY)], text_color="k", font_size=15,
                                     font_family='times', fill_shape=False, shape=None)
        plotter.add_point_labels(np.array([-1.15 * ratio * maxDisp, maxForce*0.01, 0]),
                                 labels=[str(0.0)], text_color="k", font_size=15,
                                 font_family='times', fill_shape=False, shape=None)
        ###动态图绘制
        plotter.show(interactive=False, auto_close=False)
        plotter.open_gif(str(saveName)+'.gif')
        num=len(dispX)-1
        for i1 in range(num):
            lines=np.array([[ratio*dispX[i1],forceY[i1],0], [ratio*dispX[i1+1],forceY[i1+1],0]])
            plotter.add_lines(lines,color="red",width=2)
            plotter.write_frame()
            time.sleep(timeSleep)
################################################################################
if __name__ == '__main__':
    dbPath="postResultDB.db"
    instance=prePostPlot(dbPath)
     instance.prePlot()
    componentMame="mises"
    colorValue=371000
    saveName="plasticStrain"
    timeSleep=0.1
    instance.postPlot(componentMame,colorValue,saveName,timeSleep) #绘制应力及等效塑性应变动态图
    saveName1="dispForce"
    instance.dispForcePlot(saveName1,timeSleep) #绘制加载点力与位移滞回曲线

