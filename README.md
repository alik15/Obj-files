# Obj-files
Aimed at manipulating object files from the command line.

While there are lots of parts of an OBJ file we shall only be dealing with 2 main parts of .obj file


## 1. Vertices
There are 3 different types of vertices

#### V - Geometric Vertices
#### Vt - Texture Vertices  
#### Vn - Vertex Normals

## Functionality
In obj_lib.py you will find 2 classes
One deals with object file and the other with material files
The object file class can load and save multiple object files into a single file
It can also apply rotations in x,y, and z axis to the object and translate it along all 3 directions

Much more detailed information can be found at: <br><br>
obj files: http://paulbourke.net/dataformats/obj/ <br>
material files: http://www.paulbourke.net/dataformats/mtl/ <br>
# Material Files
They are linked to the obj-files and contain detail for textures,etc
The main features in a material file are:


## Functionality
Can combine, rotate, translate letters in .obj file as well as manipulate texture and lighting
An example of an .mtl file:
An example .mtl file

�
newmtl dolph01
Ka 0.4000 0.4000 0.4000
Kd 0.0000 0.2000 1.0000
Ks 0.5000 0.5000 0.5000
illum 2
Ns 60.0000
�
Right now, the class dealing with .mtl files can read and store the various values in a list as strings

To Do:
-convert string to int, so that they can be manipulated
-make auxilliary functions to change the different parameters by own choice or at random
-save the changed parameters to a new .mtl file
-test this and the rotation and translation function
Can find more detail in the following link : https://web.cse.ohio-state.edu/~shen.94/581/Site/Lab3_files/Labhelp_Obj_parser.htm
