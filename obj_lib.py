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
        
    def load_obj(self, filename: str , max_face, default_mtl='default_mtl', triangulate=False) -> WavefrontOBJ:
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
 ## this function will take the individual 3d coordinate for the vertex
    #and rotate it and translate it according to input
    def rotate_obj( s, angle_x = 0, angle_y = 0,angle_z= 0, trans_x = 0, trans_y = 0, trans_z = 0 ):
                #angle_x,angle_y,angle_z are inputs 
        #which tell amount of rotation in each specific axis
        #then we multiply our vertcies with the transformation matrix
        # for rotation in each matrix
        v1=s[0].split("//") # x-cord
        v2=s[1].split("//") # y- cord
        v3=s[2].split("//") # z- cord
     # translation by adding value to each vertex
        v1=int(v1[0])
        v1 += trans_x
        v2=int(v2[0])
        v2 += trans_y
        v3=int(v3[0])
        v3+= trans_z
        list1=[v1,v2,v3]
        #rotation by multiplying each 3x1 vertex vector by rotation matrix
        # using np to calculate sin,cos
        #angle input in degrees
        r_x =[[1,0,0],[0,np.cos(angle_x),-np.sin(angle_x)], [0,np.sin(angle_x),np.cos(angle_x)]]
        r_y = [[np.cos(angle_y),0,np.sin(angle_y)],[0,1,0], [-np.sin(angle_y),0,np.cos(angle_y)]]
        r_z = [[np.cos(angle_z),-np.sin(angle_z),0],[np.sin(angle_z),np.cos(angle_z),0], [0,0,1]]
        # the list1 is being updated as it is being dotted by the 3 matrices
        list1 = np.dot(list1, r_x)
        list1 = np.dot(list1, r_y)
        list1 = np.dot(list1, r_z)
        return list1
    # complete this so we know what to do with the saved list of vertices
    #list 1 is basically the 3d verter points after being rotated 

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
                #a = [parse_vector(toks[1:])]
                #--------------------------------------
                #instead of calling the parse vector, we are calling the rotate object function
                #the object has 6 additional parameters
                # angles for rotation along x,y,z axis
                # and value for translation x , y , or z direction
                a = [rotate_obj(toks[1:], 45,45,45, 10,10,-5)]
                
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


# CLASS FOR MATERIAL OBJECT FILES
class mtlobj:
    def __init__(self):
        self.path = None
        #the material file has the following values
        self.name = []
        self.Ka = [] #s a 3 integer value ex. 3.000 2.000 1.000
        self.Ks = [] #all values that start with K have 3 float values
        self.Kd = []
        self.Ke = []
        self.illum = [] #a single float
        self.Ns = [] #a single float
        self.d = [] #a single float
        self.Ni = [] #a single float
        self.map_Kd = [] #file path to image for texture

    def load_mtl(self, filename: str):
        #file is being read and each value being stored
        with open( filename, 'r' ) as mtl:
            lines = mtl.readlines()
            for line in range(len(lines)):
                lines[line].strip()
                lines[line].strip("\n")
                ## right now values are being stored as strings,
                #if we want to manipulate, will need to convert to floats
                 if lines[line][0] == "n" and lines[line][1] == "e":
                    self.name.append(lines[line][:-1])
                if lines[line][0] == 'N' and lines[line][1] == 's':
                    val = lines[line][3:-1]
                    self.Ns.append(val)
                if lines[line][0] == "N" and lines[line][1] == "i":
                    self.Ni.append([lines[line][3:-1]])
                if lines[line][0] == "d":
                    self.d.append([lines[line][2:-1]])
                if lines[line][0] == "K" and lines[line][1] == "a":
                    self.Ka.append([lines[line][3:-1]])
                if lines[line][0] == "K" and lines[line][1] == "s":
                    self.Ks.append([lines[line][3:-1]])
                if lines[line][0] == "K" and lines[line][1] == "e":
                    self.Ke.append([lines[line][3:-1]])
                if lines[line][0] == "K" and lines[line][1] == "d":
                    self.Kd.append([lines[line][3:-1]])
                if lines[line][0] == "m" and lines[line][1] == "a":
                    self.map_Kd.append([lines[line][7:-1]])
                if lines[line][0] == "i":
                    self.illum.append([lines[line][6:-1]])

    def save_mtl(self, name: str):
    """Saves values in material file to new file
    Warning: Contains no error checking
    """
    # store the values in a string in the right order, and write it to the file
    #TO-Do, add the labels within the string such as Ka, Ks etc
    filename = name
    with open( filename, 'a' ) as ofile:
        for i in range len(self.name):
            material =  "\n" + str(self.name[i] + "\n" self.Ns[i] + "\n" + self.Ka[i] + "\n" self.Kd[i] + "\n" + self.Ks[i] + "\n" + self.Ke[i] + "\n"  + self.Ni[i]+ "\n" + self.d[i] + "\n" + self.illum[i]+ "\n" +self.map_Kd[i] + "\n"
            ofile.write(material)
        #helper functions, allow user to change value of texture parameters
        # have to enter the number in array of material file which they want to access 
    def ambient_clr(self, num: int, r:int,g:int,b:int):
        self.Ka[num][0] = r
        self.Ka[num][1] = r
        self.Ka[num][2] = r
        
    def diffuse_clr(self, num: int, r:int,g:int,b:int):
        self.Kd[num][0] = r
        self.Kd[num][1] = r
        self.Kd[num][2] = r
        
    def spec_clr(self, num: int, r:int,g:int,b:int):
        self.Ks[num][0] = r
        self.Ks[num][1] = r
        self.Ks[num][2] = r

    def illum(self, num:int, illumination: int):
        self.illum[num] = illumination
    def shine(self, num:int, shine: int):
        self.Ns[num] = shine

    def transparency(self, num:int, Tr: int):
        self.d[num] = Tr

    def texture(self, path: str, num: int):
        self.map_Ka[num] = path
        

        
