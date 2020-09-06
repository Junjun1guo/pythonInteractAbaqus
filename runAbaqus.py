#############################
from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbAccess import *
import regionToolset
#############################
session.viewports["Viewport: 1"].setValues(displayedObject=None)
#############################
mdb.models.changeKey(fromName="Model-1",toName="steelPlate Frame")
plateModel=mdb.models["steelPlate Frame"]
#############################
bendPlateSketch_1=plateModel.ConstrainedSketch(name="bendPlateSketch_1",sheetSize=2)
bendPlateSketch_1.Line(point1=(-0.75, 0.1),point2=(-0.75, 0))
bendPlateSketch_1.Line(point1=(-0.75, 0),point2=(0.75, 0))
bendPlateSketch_1.Line(point1=(0.75, 0),point2=(0.75, 0.1))
bendPlateSketch_1.Line(point1=(0.75, 0.1),point2=(0.3, 0.6))
bendPlateSketch_1.Line(point1=(0.3, 0.6),point2=(0.3, 0.9))
bendPlateSketch_1.Line(point1=(0.3, 0.9),point2=(0.75, 1.4))
bendPlateSketch_1.Line(point1=(0.75, 1.4),point2=(0.75, 1.5))
bendPlateSketch_1.Line(point1=(0.75, 1.5),point2=(-0.75, 1.5))
bendPlateSketch_1.Line(point1=(-0.75, 1.5),point2=(-0.75, 1.4))
bendPlateSketch_1.Line(point1=(-0.75, 1.4),point2=(-0.3, 0.9))
bendPlateSketch_1.Line(point1=(-0.3, 0.9),point2=(-0.3, 0.6))
bendPlateSketch_1.Line(point1=(-0.3, 0.6),point2=(-0.75, 0.1))
bendPlatePart_1=plateModel.Part(name="bendPlatePart_1",dimensionality=THREE_D,type=DEFORMABLE_BODY)
bendPlatePart_1.BaseShell(sketch=bendPlateSketch_1)
bendPlatePart_2=plateModel.Part(name="bendPlatePart_2",objectToCopy=bendPlatePart_1)
bendPlatePart_3=plateModel.Part(name="bendPlatePart_3",objectToCopy=bendPlatePart_1)
bendPlatePart_4=plateModel.Part(name="bendPlatePart_4",objectToCopy=bendPlatePart_1)
bendPlatePart_5=plateModel.Part(name="bendPlatePart_5",objectToCopy=bendPlatePart_1)
bottomPlateSketch=plateModel.ConstrainedSketch(name="bottomPlate",sheetSize=2)
bottomPlateSketch.Line(point1=(-0.75, 0),point2=(0.75, 0))
bottomPlatePart=plateModel.Part(name="bottomPlatePart",dimensionality=THREE_D,type=DEFORMABLE_BODY)
bottomPlatePart.BaseShellExtrude(sketch=bottomPlateSketch, depth=1.2000000000000002)
upperPlatePart=plateModel.Part(name="upperPlatePart",objectToCopy=bottomPlatePart)
#############################
elasPlasticMaterial=plateModel.Material(name="elasPlasticMaterial")
elasPlasticMaterial.Elastic(table=((210000000,0.3),))
elasPlasticMaterial.Plastic(table=((345000, 0), (471000, 0.15), (480000, 1)))
#############################
bendPlateSection=plateModel.HomogeneousShellSection(name="bendPlateSection",material="elasPlasticMaterial",thickness=0.03)
fixPlateSection=plateModel.HomogeneousShellSection(name="fixPlateSection",material="elasPlasticMaterial",thickness=0.1)
#############################
bendPlateFace_1=(bendPlatePart_1.faces,)
bendPlatePart_1.SectionAssignment(region=bendPlateFace_1,sectionName="bendPlateSection")
bendPlateFace_2=(bendPlatePart_2.faces,)
bendPlatePart_2.SectionAssignment(region=bendPlateFace_2,sectionName="bendPlateSection")
bendPlateFace_3=(bendPlatePart_3.faces,)
bendPlatePart_3.SectionAssignment(region=bendPlateFace_3,sectionName="bendPlateSection")
bendPlateFace_4=(bendPlatePart_4.faces,)
bendPlatePart_4.SectionAssignment(region=bendPlateFace_4,sectionName="bendPlateSection")
bendPlateFace_5=(bendPlatePart_5.faces,)
bendPlatePart_5.SectionAssignment(region=bendPlateFace_5,sectionName="bendPlateSection")
bottomPlateFaces=(bottomPlatePart.faces,)
bottomPlatePart.SectionAssignment(region=bottomPlateFaces,sectionName="fixPlateSection")
upperPlateFaces=(upperPlatePart.faces,)
upperPlatePart.SectionAssignment(region=upperPlateFaces,sectionName="fixPlateSection")
#############################
rootAssembly=plateModel.rootAssembly
bendInstance_1=rootAssembly.Instance(name="bendPlateAssembly_1",part=bendPlatePart_1,dependent=ON)
bendInstance_2=rootAssembly.Instance(name="bendPlateAssembly_2",part=bendPlatePart_2,dependent=ON)
bendInstance_3=rootAssembly.Instance(name="bendPlateAssembly_3",part=bendPlatePart_3,dependent=ON)
bendInstance_4=rootAssembly.Instance(name="bendPlateAssembly_4",part=bendPlatePart_4,dependent=ON)
bendInstance_5=rootAssembly.Instance(name="bendPlateAssembly_5",part=bendPlatePart_5,dependent=ON)
bottomInstance=rootAssembly.Instance(name="bottomPlateAssembly",part=bottomPlatePart,dependent=ON)
upperInstance=rootAssembly.Instance(name="upperPlateAssembly",part=upperPlatePart,dependent=ON)
rootAssembly.translate(instanceList=('bendPlateAssembly_1', ), vector=(0.0, 0.0,0.2))
rootAssembly.translate(instanceList=('bendPlateAssembly_2', ), vector=(0.0, 0.0,0.4))
rootAssembly.translate(instanceList=('bendPlateAssembly_3', ), vector=(0.0, 0.0,0.6000000000000001))
rootAssembly.translate(instanceList=('bendPlateAssembly_4', ), vector=(0.0, 0.0,0.8))
rootAssembly.translate(instanceList=('bendPlateAssembly_5', ), vector=(0.0, 0.0,1.0))
rootAssembly.translate(instanceList=('upperPlateAssembly', ), vector=(0.0,1.5,0.0))
assemblyPart=rootAssembly.InstanceFromBooleanMerge(name='assemblyPart', instances=(bendInstance_1,bendInstance_2,bendInstance_3,bendInstance_4,bendInstance_5,
bottomInstance,upperInstance,),originalInstances=SUPPRESS,domain=GEOMETRY)
#############################
plateModel.StaticStep(name="pushOver_1",previous='Initial', initialInc=0.05, maxInc=0.05,nlgeom=ON)
#############################
refPointid=rootAssembly.ReferencePoint(point=(0, 1.5, 0)).id
refPointRegion=rootAssembly.Set(referencePoints=(rootAssembly.referencePoints[refPointid],), name='refPointSet')
assemblyTopFaces = assemblyPart.faces.findAt(((0, 1.5, 0.1),), ((0, 1.5, 0.30000000000000004),), ((0, 1.5, 0.5),), ((0, 1.5, 0.7000000000000001),), ((0, 1.5, 0.9),), ((0, 1.5, 1.1),))
topFameRegion=regionToolset.Region(faces=assemblyTopFaces)
plateModel.Coupling(name='Constraint-upperPlate',controlPoint=refPointRegion,surface=topFameRegion,couplingType=KINEMATIC,influenceRadius=WHOLE_SURFACE)
#############################
assemblyBottomFaces = assemblyPart.faces.findAt(((0, 0, 0.1),), ((0, 0, 0.30000000000000004),), ((0, 0, 0.5),), ((0, 0, 0.7000000000000001),), ((0, 0, 0.9),), ((0, 0, 1.1),))
bottomFameRegion=regionToolset.Region(faces=assemblyBottomFaces)
plateModel.DisplacementBC(name='initBC', createStepName='Initial',region=bottomFameRegion,u1=SET, u2=SET, u3=SET, ur1=SET,ur2=SET, ur3=SET)
#############################
plateModel.DisplacementBC(name='pushOver',createStepName='pushOver_1',region=refPointRegion,u3=0.6)
#############################
meshPart=plateModel.parts["assemblyPart"]
seedEdges=meshPart.edges
meshPart.seedEdgeBySize(edges=seedEdges,size=0.03)
assemblyFaces=assemblyPart.faces
assemblyFaces=meshPart.setMeshControls(regions=assemblyFaces,technique=STRUCTURED)
eleType1=mesh.ElemType(elemCode=S4R)
eleType2=mesh.ElemType(elemCode=S3)
meshRegion=regionToolset.Region(faces=(assemblyPart.faces),)
meshPart.setElementType(regions=meshRegion, elemTypes=(eleType1, eleType2))
meshPart.generateMesh()
#############################
mdb.Job(name='Job-pushOver', model='steelPlate Frame', multiprocessingMode=DEFAULT, numCpus=4,numDomains=4, numGPUs=1)
mdb.jobs['Job-pushOver'].submit(consistencyChecking=OFF)
