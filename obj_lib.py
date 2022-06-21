# wavefront.py
from ast import Num
import numpy as np
from test import *


class WavefrontOBJ:
    def __init__( self, default_mtl='default_mtl' ):
        self.path      = None               # path of loaded object
        self.mtllibs   = []                 # .mtl files references via mtllib
        self.mtls      = [ default_mtl ]    # materials referenced
        self.mtlid     = []                 # indices into self.mtls for each polygon
        self.vertices  = []                 # vertices as an Nx3 or Nx6 array (per vtx colors)
        self.normals   = []                 # normals
        self.texcoords = []                 # texture coordinates
        self.polygons  = []                 # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)
        self.faces     = []                 #stores all faces
        
def load_obj( filename: str , max_face, default_mtl='default_mtl', triangulate=False) -> WavefrontOBJ:
    """Reads a .obj file from disk and returns a WavefrontOBJ instance
    Handles only very rudimentary reading and contains no error handling!
    Does not handle:
        - relative indexing
        - subobjects or groups
        - lines, splines, beziers, etc.
    """
    # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
    # and returns a 3-tuple where unparsed values are replaced with -1
    """def parse_vertex( vstr ):
        vals = vstr.split('//')
        print(vstr)
        vid = int(vals[0]) 
        tid = int(vals[1]) if len(vals) > 1 and vals[1] else 0
        nid = int(vals[2]) if len(vals) > 2 else 0
        return (vid,tid,nid)
    """
 
    def parse_vector( s ):
        v1=s[0].split("//")
        v2=s[1].split("//")
        v3=s[2].split("//")
        
        v1=int(v1[0])    
        v2=int(v2[0])
        v3=int(v3[0])
        
        list1=[v1,v2,v3]
        return list1
    


    with open( filename, 'r' ) as objf:
        
        
        obj = WavefrontOBJ(default_mtl=default_mtl)
        obj.path = filename
        cur_mat = obj.mtls.index(default_mtl)
        for line in objf:
            toks = line.split()
            if not toks:
                continue
            if toks[0] == 'v':
                obj.vertices.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vn':
                obj.normals.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vt':
                obj.texcoords.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'f':
                #obj.faces.append( [ float(v) for v in toks[1:]] )
                #poly = [ parse_vertex(vstr) for vstr in toks[1:] ]
                a = [parse_vector(toks[1:])]
                
                poly=a[0]
              
              
                if triangulate:
                    for i in range(2,len(poly)):
                        obj.mtlid.append( cur_mat )
                        obj.polygons.append( (poly[0], poly[i-1], poly[i] ) )
                        
                else:
                    obj.mtlid.append(cur_mat)
                    obj.polygons.append( poly )
                    
                            
            elif toks[0] == 'mtllib':
                obj.mtllibs.append( toks[1] )
            elif toks[0] == 'usemtl':
                if toks[1] not in obj.mtls:
                    obj.mtls.append(toks[1])
                cur_mat = obj.mtls.index( toks[1] )
        
        for i in range (len(obj.polygons)):
                j=0
                while(j<3):
                    obj.polygons[i][j]+=max_face
                    j+=1
                                 
        print(max_face)
        return obj

def save_obj( obj: WavefrontOBJ, filename: str ):
    """Saves a WavefrontOBJ object to a file
    Warning: Contains no error checking!
    """
    with open( filename, 'a' ) as ofile:
        ofile.write("o B"+'\n')
        
        
        #for mlib in obj.mtllibs:
        #    ofile.write('mtllib {}\n'.format(mlib))
        for vtx in obj.vertices:
            ofile.write('v '+' '.join(['{}'.format(v) for v in vtx])+'\n')
        for tex in obj.texcoords:
            ofile.write('vt '+' '.join(['{}'.format(vt) for vt in tex])+'\n')
        for nrm in obj.normals:
            ofile.write('vn '+' '.join(['{}'.format(vn) for vn in nrm])+'\n')
        if not obj.mtlid:
            obj.mtlid = [-1] * len(obj.polygons)
        poly_idx = np.argsort( np.array( obj.mtlid ) )
        cur_mat = -1
        
        for face in obj.polygons:
            #print(face)
            ofile.write('f '+' '.join (['{}'.format(f) for f in face])+'\n')
        """
        for pid in poly_idx:
            if obj.mtlid[pid] != cur_mat:
                cur_mat = obj.mtlid[pid]
                ofile.write('usemtl {}\n'.format(obj.mtls[cur_mat]))
            pstr = 'f '
            for v in obj.polygons[pid]:
                # UGLY!
                vstr = '{}/{}/{} '.format(v[0]+1,v[1]+1 if v[1] >= 0 else 'X', v[2]+1 if v[2] >= 0 else 'X' )
                vstr = vstr.replace('/X/','//').replace('/X ', ' ')
                pstr += vstr
            ofile.write( pstr+'\n')
        """
# usemtl 
#################################################################################################################

def rotate_obj( obj: WavefrontOBJ, angle_x = 0, angle_y = 0,angle_z= 0):
    for vtx in range(len(obj.vertices)):
        list1= obj.vertices[vtx]
            #rotation by multiplying each 3x1 vertex vector by rotation matrix
            # using np to calculate sin,cos
            #angle input in degrees v = [1,2,3]
        r_x =[[1,0,0],[0,np.cos(angle_x),-np.sin(angle_x)], [0,np.sin(angle_x),np.cos(angle_x)]]
        r_y = [[np.cos(angle_y),0,np.sin(angle_y)],[0,1,0], [-np.sin(angle_y),0,np.cos(angle_y)]]
        r_z = [[np.cos(angle_z),-np.sin(angle_z),0],[np.sin(angle_z),np.cos(angle_z),0], [0,0,1]]
            # the list1 is being updated as it is being dotted by the 3 matrices
        list1 = np.dot(list1, r_x)
        list1 = np.dot(list1, r_y)
        list1 = np.dot(list1, r_z)
        obj.vertices[vtx] = list1
def translate_obj(obj: WavefrontOBJ, trans_x = 0, trans_y = 0, trans_z = 0 ):
      for vtx in range(len(obj.vertices)):
        v1= obj.vertices[vtx][0]
        v1 += trans_x
        v2= obj.vertices[vtx][1]
        v2 += trans_y
        v3= obj.vertices[vtx][2]
        v3+= trans_z
        list1=[v1,v2,v3]
        obj.vertices[vtx] = list1
    ##############




# CLASS FOR MATERIAL OBJECT FILES


class mtlobj:
    def __init__(self):
        self.path = None
        #the material file has the following values
        self.name = [""]
        self.Ka = [["0","0","0"]] #s a 3 integer value ex. 3.000 2.000 1.000
        self.Ks = [["0","0","0"]] #all values that start with K have 3 float values
        self.Kd = [["0","0","0"]]
        self.Ke = [["0","0","0"]]
        self.illum = ["0","0"] #a single float
        self.Ns = ["0","0"] #a single float
        self.d = ["0","0"] #a single float
        self.Ni = ["0","0"] #a single float
        self.map_Kd = [""] #file path to image for texture
###
    def load_mtl(self, filename: str):
        #file is being read and each value being stored
        with open( filename, 'r' ) as mtl:
            lines = mtl.readlines()
            for line in range(len(lines)):
                lines[line].strip()
                lines[line].strip("\n")
                if lines[line][0] == "n" and lines[line][1] == "e":
                    self.name.append(lines[line][:-1])
                elif lines[line][0] == 'N' and lines[line][1] == 's':
                    val = lines[line][3:-1]
                    self.Ns.append(val)
                elif lines[line][0] == "N" and lines[line][1] == "i":
                    self.Ni.append([lines[line][3:-1]])
                elif lines[line][0] == "d":
                    self.d.append([lines[line][2:-1]])
                elif lines[line][0] == "K" and lines[line][1] == "a":
                    self.Ka.append([lines[line][3:-1]])
                elif lines[line][0] == "K" and lines[line][1] == "s":
                    self.Ks.append([lines[line][3:-1]])
                elif lines[line][0] == "K" and lines[line][1] == "e":
                    self.Ke.append([lines[line][3:-1]])
                elif lines[line][0] == "K" and lines[line][1] == "d":
                    self.Kd.append([lines[line][3:-1]])
                elif lines[line][0] == "m" and lines[line][1] == "a":
                    self.map_Kd.append([lines[line][7:-1]])
                elif lines[line][0] == "i":
                    self.illum.append([lines[line][6:-1]])
                else:
                    print("Unidentified Programming Object")
 
    def save_mtl(self, name: str):
        """Saves values in material file to new file
        Warning: Contains no error checking
        """
        filename = name
        # store the values in a string in the right order, and write it to the file
        #TO-Do, add the labels within the string such as Ka, Ks etc
        with open( filename, 'w' ) as ofile:
            for i in range(len(self.name)): 
                material =  ("\n" + "newmtl " + 
                             str(self.name[i]) + "\n"+
                             "Ns " + str(self.Ns[i]) + "\n" + 
                             "Ka " + str(self.Ka[i][0])+" " + str(self.Ka[i][1])+" " + str(self.Ka[i][2])+"\n"+
                             "Kd " + str(self.Kd[i][0])+" " + str(self.Kd[i][1])+" " + str(self.Kd[i][2])+"\n"+
                             "Ks " + str(self.Ks[i][0])+" " + str(self.Ks[i][1])+" " + str(self.Ks[i][2])+"\n"+ 
                             "Ke "+str(self.Ke[i][0])+" " + str(self.Ke[i][1])+" " + str(self.Ke[i][2])+"\n"+
                             "Ni "+str(self.Ni[i])+ "\n" + 
                             "d "+str(self.d[i]) + "\n" + 
                             "illum "+str(self.illum[i]) +"\n" + 
                             "map_Kd C:\\\\Users\\\\Hassaan\\\\Documents\\\\" + str(self.map_Kd[i]))
                ofile.write(material)
            #helper functions, allow user to change value of texture parameters
            # have to enter the number in array of material file which they want to access 
    def ambient_clr(self, num: int, r:int,g:int,b:int):
        if(num >= len(self.Ka)):
            self.Ka.append([r,g,b])
        else:
            self.Ka[num] = [r,g,b]
        
    def diffuse_clr(self, num: int, r:int,g:int,b:int):
        if(num >= len(self.Kd)):
            self.Kd.append([r,g,b])
        else:
            self.Kd[num] = [r,g,b]
        
    def spec_clr(self, num: int, r:int,g:int,b:int):
        if(num >= len(self.Ks)):
            self.Ks.append([r,g,b])
        else:
            self.Ks[num] = [r,g,b]
    
    def setKe(self, num: int, r:int,g:int,b:int):
        if(num >= len(self.Ke)):
            self.Ke.append([r,g,b])
        else:
            self.Ke[num] = [r,g,b]
            
    def illumi(self, num, illumination):
        if(num >= len(self.illum)):
            self.illum.append(illumination)
        else:
            self.illum[num] = str(illumination)
    def shine(self, num:int, shine: int):
        if(num >= len(self.Ns)):
            self.Ns.append(shine)
        else:
            self.Ns[num] = str(shine)

    def transparency(self, num:int, Tr: int):
        if(num >= len(self.d)):
            self.d.append(Tr)
        else:
            self.d[num] = str(Tr)

    def texture(self, path: str, num: int):
        if(num >= len(self.map_Kd)):
            self.map_Kd.append(path)
        else:
            self.map_Kd[num] = str(path)
    def set_name(self, num: int, path: str):
        if(num >= len(self.name)):
            self.name.append(path)
        else:
            self.name[num] = str(path)
        


           



