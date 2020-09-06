# prePostFEA
A general pre and post process framework for finite element analysis, such as ABAQUS, OpenSees et al.

![GitHub](https://img.shields.io/github/license/Junjun1guo/prePostFEA?color=red&logoColor=blue)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Junjun1guo/prePostFEA)
![GitHub top language](https://img.shields.io/github/languages/top/Junjun1guo/prePostFEA)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Junjun1guo/prepostFEA/numpy)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Junjun1guo/prepostFEA/pyvista)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Junjun1guo/prepostFEA/records)
![GitHub repo size](https://img.shields.io/github/repo-size/Junjun1guo/prePostFEA?color=GREEN)
![GitHub stars](https://img.shields.io/github/stars/Junjun1guo/prePostFEA)
![GitHub last commit](https://img.shields.io/github/last-commit/Junjun1guo/prePostFEA)

<img src="https://github.com/Junjun1guo/prePostFEA/blob/master/misesStress.gif" width="480" height="350" /><img src="https://github.com/Junjun1guo/prePostFEA/blob/master/dispForce.gif" width="480" height="350" />

## Usage 
1. __Generate finite element model__. If use commercial software,such as ABAQUS, you can write python script to establish FEM(referring abaqusPythonScript.py). If use open source software, such as OpenSees, you can also write python script to generate the input file(referring abaqusPythonScript.py). In additon, for two or three dimensional problems, [pygmsh](https://github.com/nschloe/pygmsh) can be used to mesh the model.
and process the output database (abaqusODBProcess.py and saveDataToSqlite.py), then using 
 
