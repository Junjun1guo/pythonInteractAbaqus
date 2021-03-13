##########################################################################    
Author: Junjun Guo([HomePage](https://github.com/Junjun1guo))    
E-mail: guojj@tongji.edu.cn/guojj_ce@163.com    
Environemet: Successfully excucted in python 3.8    
##########################################################################
______
A general pre and post process framework for finite element analysis, such as ABAQUS, OpenSees et al.

<img width="390" height="300" src="https://github.com/Junjun1guo/pythonInteractAbaqus/edit/blob/master/misesStress.gif"/><img width="390" height="300" src="https://github.com/Junjun1guo/pythonInteractAbaqus/edit/blob/master/dispForce.gif"/>

## Usage 
1. __Generate finite element model__. If use commercial software,such as ABAQUS, you can write python script to establish FEM(referring __abaqusPythonScript.py__). If use open source software, such as OpenSees, you can also write python script to generate the input file(referring __abaqusPythonScript.py__). In additon, for two or three dimensional problems, [pygmsh](https://github.com/nschloe/pygmsh) can be used to mesh the model.       
2. __outPut process__. If use commercial software,such as ABAQUS, you can write python script to read the output database(referring __abaqusODBProcess.py__).If use open source software, such as OpenSees, you can process the output files and save data to [pysqlite](https://github.com/ghaering/pysqlite) database(referring __saveDataToSqlite.py__).    
3. __result display__. [pyvista](https://docs.pyvista.org/) is adopted to generate static and dynamic graphs(referring __prePostProcess.py__).


 
