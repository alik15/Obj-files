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
def rotate_obj( filename: str , max_face, angle_x, angle_y,angle_z, default_mtl='default_mtl', triangulate=False ) -> WavefrontOBJ:
    def parse_vector( s ):
        v1=s[0].split("//")
        v2=s[1].split("//")
        v3=s[2].split("//")
        #angle_x,angle_y,angle_z are inputs 
        #which tell amount of rotation in each specific axis
        #then we multiply our vertcies with the transformation matrix
        # for rotation in each matrix
        v1=int(v1[0])    
        v2=int(v2[0])
        v3=int(v3[0])
        list1=[v1,v2,v3]
        r_x =[[1,0,0],[0,np.cos(angle_x),-np.sin(angle_x)], [0,np.sin(angle_x),np.cos(angle_x)]]
        r_y = [[np.cos(angle_y),0,np.sin(angle_y)],[0,1,0], [-np.sin(angle_y),0,np.cos(angle_y)]]
        r_z = [[np.cos(angle_z),-np.sin(angle_z),0],[np.sin(angle_z),np.cos(angle_z),0], [0,0,1]]
        rotate_x = np.dot(list1, r_x)
        rotate_y = np.dot(list1, r_y)
        rotate_z = np.dot(list1, r_z)
        return list1     
#Function for stroing multiple obj files in one

#Function for rotating Obj file given angle

#Function for transforming Obj file given plane and face ???

#Add randomised material applier

