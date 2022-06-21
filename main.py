from codecs import IncrementalDecoder
from obj_lib import *
import numpy as np

#the list stores all the obj files in it and will be used for the main loop

objects=["A.obj", "B.obj", "C.obj"]


#wipes the file of any pre-existing data
with open( "source/new.obj", 'w' ) as ofile:
    ofile.write("")


#checks the list for the objects and appends them to the same one 
count = 0
faces_increment=False
increment=0
faces=[]

max_face=0

for obj in objects:
   
     

       print("oo",max_face)
       obj = load_obj("source/"+obj,max_face)
       
       
       max_face=np.max(obj.polygons)
       
       
       
    
  
    

       save_obj(obj, "output/new.obj")
        

    

