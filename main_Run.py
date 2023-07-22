#-*-coding: UTF-8-*-
#########################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com/guojj01@gmail.com
#  Environemet: Successfully executed in python 3.8
#  Date: 2021-09-19
#########################################################################
#import necessary modules
import os
import runpy
#########################################################################
############---1---基于abaqus环境进行计算----##########################
# os.system('abaqus CAE noGUI=runAbaqus.py') #active abaqus CAE and run the script
os.system('abaqus CAE script=runAbaqus.py') #active abaqus CAE and run the script
# print("Successfully executed runAbaqus.py module!")
############---2---操作obd文件提取结果----#############################
# os.system('abaqus CAE noGUI=abaqusODBProcess.py')
# os.system('abaqus CAE script=abaqusODBProcess.py')
# print("Successfully executed abaqusODBProcess.py module!")
############---3---将提取的结果存储于数据库中----########################
# runpy.run_path('saveDataToSqlite.py', run_name='__main__')
# print("Successfully executed saveDataToSqlite.py module!")
############---4---基于pyvista显示结果动图----########################
# runpy.run_path('resultsDisplayPyvista.py', run_name='__main__')
# print("Successfully executed resultsDisplayPyvista.py module!")



