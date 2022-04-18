from obj_lib import *

#the list stores all the obj files in it and will be used for the main loop

objects=["A.obj"]


#wipes the file of any pre-existing data
with open( "new.obj", 'w' ) as ofile:
    ofile.write("")


#checks the list for the objects and appends them to the same one 
count = 0
for obj in objects:
   
   
    obj = load_obj(obj, count)
    print(len(obj.polygons))
    save_obj(obj, "new.obj")
    
    

