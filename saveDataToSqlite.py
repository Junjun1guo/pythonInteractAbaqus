# -*- coding: utf-8 -*-
# @File : 234.py
# @Date :  2020-09-02 18:14
# @Email :  {guojj@tongji.edu.cn/guojj01@gmail.com}
# @Author : guojj


###导入必要的模块
import records
import numpy as np


class SaveData(object):
    """将提取的数据存储到数据库中"""

    def __init__(self,dbPath):
        self._dbPath=dbPath

    @classmethod
    def initDB(self,dbPath):
        """初始化数据库"""
        self.db = records.Database('sqlite:///'+dbPath)
        tableNames=self.db.get_table_names()
        for each in tableNames:
            self.db.query("DROP TABLE IF EXISTS "+each)

    def saveNodes(self,nodes):
        """将节点列表存入数据库,[(tag1,x1,y1,z1),..]"""
        db=records.Database('sqlite:///'+self._dbPath)
        nodesDict=[{'tags':int(each[0]),'coords':str(each[1:])} for each in nodes]
        nodesTable="""
                CREATE TABLE IF NOT EXISTS
                nodes(
                tags INT NOT NULL,
                coords MESSAGE_TEXT NOT NULL);"""
        db.query(nodesTable)
        insertNodes="""
                INSERT INTO
                nodes(tags,coords)
                values (:tags,:coords)
                    """
        db.bulk_query(insertNodes,nodesDict)

    def saveElements(self,elements):
        """将单元列表存入数据库,[(tag1,n1,n2,..),..]"""
        db=records.Database('sqlite:///'+self._dbPath)
        elesDict=[{'tags':int(each[0]),'connectivity':str(each[1:])} for each in elements]
        elesTable="""
                CREATE TABLE IF NOT EXISTS
                elements(
                tags INT NOT NULL,
                connectivity MESSAGE_TEXT NOT NULL);"""
        db.query(elesTable)
        insertEles="""
                INSERT INTO
                elements(tags,connectivity)
                values (:tags,:connectivity)
                    """
        db.bulk_query(insertEles,elesDict)

    def getNode(self,tags):
        """返回特定节点的坐标"""
        db=records.Database('sqlite:///'+self._dbPath)
        conn = db.get_connection()
        try:
            queryValue=conn.query('select * from nodes where tags=='+str(tags)+';')
            returnValue=queryValue.all(as_dict=True)[0]['coords']
            return returnValue
        except :
            print("Please enter correct node tag (integer)!")
            return

    def getAllNode(self):
        """返回所有节点坐标"""
        db=records.Database('sqlite:///'+self._dbPath)
        conn = db.get_connection()
        try:
            queryValue=conn.query('select * from nodes;')
            returnValue=queryValue.all(as_dict=True)
            return returnValue
        except :
            print("table nodes doesn't exitst!")
            return

    def getEle(self,tags):
        """返回特定节点的坐标"""
        db=records.Database('sqlite:///'+self._dbPath)
        conn = db.get_connection()
        try:
            queryValue=conn.query('select * from elements where tags=='+str(tags)+';')
            returnValue=queryValue.all(as_dict=True)[0]['connectivity']
            return returnValue
        except :
            print("Please enter correct element tag (integer)!")
            return

    def getAllEle(self):
        """返回所有单元信息"""
        db=records.Database('sqlite:///'+self._dbPath)
        conn = db.get_connection()
        try:
            queryValue=conn.query('select * from elements;')
            returnValue=queryValue.all(as_dict=True)
            return returnValue
        except :
            print("table elements doesn't exitst!")
            return

    def saveMisesStress(self,mises):
        """将Mises应力列表存储到数据库"""
        db=records.Database('sqlite:///'+self._dbPath)
        elesDict=[{'eleTag':int(each[0]),'mises':str(each[1:])} for each in mises]

        elesTable="""
                CREATE TABLE IF NOT EXISTS
                mises(
                eleTag INT NOT NULL,
                mises MESSAGE_TEXT NOT NULL);"""
        db.query(elesTable)
        insertEles="""
                INSERT INTO
                mises(eleTag,mises)
                values (:eleTag,:mises)
                    """
        db.bulk_query(insertEles,elesDict)

    def getEleMises(self,eletags):
        """返回特定单元的Mises应力"""
        db=records.Database('sqlite:///'+self._dbPath)
        conn = db.get_connection()
        try:
            queryValue=conn.query('select * from mises where eleTag=='+str(eletags)+';')
            returnValue=queryValue.all(as_dict=True)[0]['mises']
            return returnValue
        except :
            print("Please enter correct element tag (integer)!")
            return

    def getAllMises(self):
        """返回所有单元的Mises应力"""
        db = records.Database('sqlite:///' + self._dbPath)
        conn = db.get_connection()
        try:
            queryValue = conn.query('select * from mises;')
            returnValue = queryValue.all(as_dict=True)
            return returnValue
        except:
            print("table mises doesn't exitst!")
            return

    def savePEEQ(self,PEEQ):
        """将等效塑性应变列表存储到数据库"""
        db=records.Database('sqlite:///'+self._dbPath)
        elesDict=[{'eleTag':int(each[0]),'PEEQ':str(each[1:])} for each in PEEQ]

        elesTable="""
                CREATE TABLE IF NOT EXISTS
                peeq(
                eleTag INT NOT NULL,
                PEEQ MESSAGE_TEXT NOT NULL);"""
        db.query(elesTable)
        insertEles="""
                INSERT INTO
                peeq(eleTag,PEEQ)
                values (:eleTag,:PEEQ)
                    """
        db.bulk_query(insertEles,elesDict)

    def getAllPEEQ(self):
        """返回所有单元的等效塑性应变"""
        db = records.Database('sqlite:///' + self._dbPath)
        conn = db.get_connection()
        try:
            queryValue = conn.query('select * from peeq;')
            returnValue = queryValue.all(as_dict=True)
            return returnValue
        except:
            print("table peeq doesn't exitst!")
            return

    def saveNodeDisp(self,dispX,dispY,dispZ):
        """保存节点位移"""
        db=records.Database('sqlite:///'+self._dbPath)
        nodeDispDict=[{'nodeTag':int(x[0]),'dispX':str(x[1:]),'dispY':str(y[1:]),'dispZ':str(z[1:])}
            for x,y,z in zip(dispX,dispY,dispZ)]
        nodeDispTable="""
                CREATE TABLE IF NOT EXISTS
                nodeDisp(
                nodeTag INT NOT NULL,
                dispX MESSAGE_TEXT NOT NULL,
                dispY MESSAGE_TEXT NOT NULL,
                dispZ MESSAGE_TEXT NOT NULL);"""
        db.query(nodeDispTable)
        insertEles="""
                INSERT INTO
                nodeDisp(nodeTag,dispX,dispY,dispZ)
                values (:nodeTag,:dispX,:dispY,:dispZ)
                    """
        db.bulk_query(insertEles,nodeDispDict)

    def getnodeDisp(self,nodeTag):
        """返回特定节点位移"""
        db=records.Database('sqlite:///'+self._dbPath)
        conn = db.get_connection()
        try:
            queryValue=conn.query('select * from nodeDisp where nodeTag=='+str(nodeTag)+';')
            returnValueX=queryValue.all(as_dict=True)[0]['dispX']
            returnValueY = queryValue.all(as_dict=True)[0]['dispY']
            returnValueZ = queryValue.all(as_dict=True)[0]['dispZ']
            return returnValueX,returnValueY,returnValueZ
        except :
            print("Please enter correct node tag (integer)!")
            return

    def getAllDisp(self):
        """返回所有节点位移"""
        db = records.Database('sqlite:///' + self._dbPath)
        conn = db.get_connection()
        try:
            queryValue = conn.query('select * from nodeDisp;')
            returnValue = queryValue.all(as_dict=True)
            return returnValue
        except:
            print("table nodeDisp doesn't exitst!")
            return

    def saveDispForce(self,refDisp,refLoad):
        """保存加载点力与位移时程"""
        db=records.Database('sqlite:///'+self._dbPath)
        loadForceDict=[{'refDisp':str(x),'refLoad':str(y)}
            for x,y in zip(refDisp,refLoad)]
        dispForceTable="""
                CREATE TABLE IF NOT EXISTS
                dispForce(
                refDisp MESSAGE_TEXT NOT NULL,
                refLoad MESSAGE_TEXT NOT NULL);"""
        db.query(dispForceTable)
        insertEles="""
                INSERT INTO
                dispForce(refDisp,refLoad)
                values (:refDisp,:refLoad)
                    """
        db.bulk_query(insertEles,loadForceDict)

    def getRefResponse(self):
        """返回加载点力与位移时程"""
        db = records.Database('sqlite:///' + self._dbPath)
        conn = db.get_connection()
        try:
            queryValue = conn.query('select * from dispForce;')
            returnValue = queryValue.all(as_dict=True)
            return returnValue
        except:
            print("table dispForce doesn't exitst!")
            return



################################################################################
if __name__ == '__main__':
    dbPath="postResultDB.db"
    SaveData.initDB(dbPath)
    saveInstance=SaveData(dbPath)
    nodes=np.loadtxt("postResults/nodes.txt")
    saveInstance.saveNodes(nodes)
    elements=np.loadtxt("postResults/elements.txt")
    saveInstance.saveElements(elements)
    mises=np.loadtxt("postResults/misesStress.txt")
    saveInstance.saveMisesStress(mises)
    PEEQ=np.loadtxt("postResults/PEEQ.txt")
    saveInstance.savePEEQ(PEEQ)
    dispX=np.loadtxt("postResults/dispX.txt")
    dispY= np.loadtxt("postResults/dispY.txt")
    dispZ = np.loadtxt("postResults/dispZ.txt")
    saveInstance.saveNodeDisp(dispX,dispY,dispZ)
    refDisp = np.loadtxt("postResults/refDisp.txt")
    refLoad = np.loadtxt("postResults/refLoad.txt")
    saveInstance.saveDispForce(refDisp,refLoad)




