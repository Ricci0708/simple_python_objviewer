###############################
# page 27
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

flag = 0 #vaiable for whether the obj file is dropped
gCamAng = 0. 
gCamHeight = 1.
zoom = 0.5
z_toggle = 1
vertex = [] #list of obj's vertex
vertexnormal = [] #list of obj's vertex normal
face = [] #list of obj's faces

'''
variables for glDrawArrays() or glDrawElements() to render a triangle mesh
추후에 더해보겠음...
'''
gVertexArrayIndexed = None
gIndexArray = None

#test case
def drawUnitCube_glVertex():
    glBegin(GL_TRIANGLES)

    glNormal3f(0,1,0)   # v0, v1, ... v5 normal
    glVertex3f( 0.5, 0.5,-0.5)  # v0 position
    glVertex3f(-0.5, 0.5,-0.5)  # v1 position
    glVertex3f(-0.5, 0.5, 0.5)  # v2 position
 
    glVertex3f( 0.5, 0.5,-0.5)  # v3 position
    glVertex3f(-0.5, 0.5, 0.5)  # v4 position
    glVertex3f( 0.5, 0.5, 0.5)  # v5 position
                              
    glNormal3f(0,-1,0)  # v6, v7, ... v11 normal
    glVertex3f( 0.5,-0.5, 0.5)  # v6 position
    glVertex3f(-0.5,-0.5, 0.5)  # v7 position
    glVertex3f(-0.5,-0.5,-0.5)  # v8 position
 
    glVertex3f( 0.5,-0.5, 0.5)  # v9 position
    glVertex3f(-0.5,-0.5,-0.5)  # v10 position
    glVertex3f( 0.5,-0.5,-0.5)  # v11 position

    glNormal3f(0,0,1)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)

    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glNormal3f(0,0,-1)
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)

    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
                             
    glNormal3f(-1,0,0)
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 

    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glNormal3f(1,0,0)
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)

    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)

    glEnd()

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            [ 1.5, 0.0, 0.0],
            [ 0.0, 1.5, 0.0],
            [ 0.0, 0.0, 1.5],
            [ 0.0, 0.0, 0.0],
            ], 'float32')
    iarr = np.array([
            [0,1,3],
            [1,2,3],
            [0,2,3],
            ])
    return varr, iarr 

def drawUnitCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)



def render(ang):
    global gCamAng, gCamHeight, flag, zoom, z_toggle
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION) # use projection matrix stack for projection transformation for correct lighting
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()
    #if z_toggle is on solid mode else wire frame
    if z_toggle:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)

    # light position
    glPushMatrix()

    # glRotatef(ang,0,1,0)  # try to uncomment: rotate light
    lightPos = (1.,0.,0.,0.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    lightPos = (0.,1.,0.,0.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    lightPos = (0.,0.,1.,0.)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
    lightPos = (-1.,-1.,-1.,0.)
    glLightfv(GL_LIGHT3, GL_POSITION, lightPos)
  
    glPopMatrix()

    # light intensity for each color channel
    ambientLightColor = (.1,0,.0,1.)
    diffuseLightColor = (1.,0.,0.,1.)
    specularLightColor = (1.,0.,0.,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor)

    ambientLightColor = (0.,.1,0.,1.)
    diffuseLightColor = (0.,1.,0.,1.)
    specularLightColor = (0.,1.,0.,1.)

    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specularLightColor)

    ambientLightColor = (0.,.0,1.,1.)
    diffuseLightColor = (0.,0.,1.,1.)
    specularLightColor = (0.,0.,1.,1.)

    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, specularLightColor)

    ambientLightColor = (.1,.0,.1,1.)
    diffuseLightColor = (1.,0.,1.,1.)
    specularLightColor = (1.,0.,1.,1.)

    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT3, GL_SPECULAR, specularLightColor)

    # material reflectance for each color channel
    diffuseObjectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,0.,0.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, diffuseObjectColor)
    # glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    # glRotatef(ang,0,1,0)    # try to uncomment: rotate object

    glColor3ub(255, 0, 0) # glColor*() is ignored if lighting is enabled

    # drawUnitCube_glVertex()
    # drawUnitCube_glDrawArray()
    if (flag == 0):
        # print("flag")
        drawUnitCube_glVertex()

    # usin glScalef make zoom in/out
    # if zoom out scale smaller
    # if zoom in scale larger
    glScalef(zoom, zoom, zoom)


    for i in range(len(face)):
        v = 0
        vn = 0
        glBegin(GL_POLYGON)
        for j in range(len(face[i])):
            # print(face[j])
            if("//" in face[i][j]):
                t = face[i][j].split("//")
                v = int(t[0])
                if (len(t) == 3):
                    vn = int(t[2])
                else:
                    vn = int(t[1])
            elif("/" in face[i][j]):
                t = face[i][j].split("/")
                v = int(t[0])
                if (len(t) == 3):
                    vn = int(t[2])
                else:
                    vn = int(t[1])
            glNormal3fv(vertex[vn - 1])
            glVertex3fv(vertex[v - 1])
        glEnd()
    glPopMatrix()

    glDisable(GL_LIGHTING)
	


# def drawUnitCube_glDrawElements():
#     global gVertexArrayIndexed, gIndexArray
#     varr = gVertexArrayIndexed
#     iarr = gIndexArray
#     glEnableClientState(GL_VERTEX_ARRAY)
#     glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
#     glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

# def drawUnitCube_glDrawArray():
#     global gVertexArraySeparate
#     varr = gVertexArraySeparate
#     glEnableClientState(GL_VERTEX_ARRAY)
#     glEnableClientState(GL_NORMAL_ARRAY)
#     glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
#     glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
#     glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, zoom, z_toggle
    if action == glfw.PRESS or action==glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key == glfw.KEY_2:
            gCamHeight += .1
        elif key == glfw.KEY_W:
            gCamHeight += -.1
        elif key == glfw.KEY_A:
            zoom += .1
        elif key == glfw.KEY_S:
            zoom -= .1
        elif key == glfw.KEY_Z:
            if z_toggle:
                z_toggle = 0
            else:
                z_toggle = 1
'''
the argument of drop_callback function is the list of path
if the arguments is larger than 1 print error message
else render the obj file in the window

'''


def createVertexAndIndexArrayIndexed2():
    global vertex, vertexnormal, face
    varr = []
    iarr = []

    for i in range(len(vertex)):
        varr.append(vertex[i])
    for j in range(len(face)):
        iarr.append(face[j])


    varr0 = np.asarray(varr)
    iarr0 = np.asarray(iarr)


    return varr0, iarr0 



def drop_callback(window, path):
    global vertex, vertexnormal, face, gVertexArrayIndexed, gIndexArray, flag
    if (len(path) > 1):
        print("error drop 1 file")
    else:
        face = []
        vertex = []
        vertexnormal = []
        tri = 0
        quad = 0
        n_obj = 0
        f = open(path[0],'r')


        lines = f.readlines()
        for line in lines:
            line = line.split()
            # add vertex 
            if (line == []):
                continue

            elif(line[0] == "v"):
                vertex.append([float(line[1]),float(line[2]),float(line[3])])
            #add vertex normal vectors
            elif(line[0] == "vn"):
                vertexnormal.append([float(line[1]),float(line[2]),float(line[3])])
            #add faces
            elif(line[0] == "f"):
                i = 1
                p = []

                if (len(line) == 4):
                    tri += 1
                elif(len(line) == 5):
                    quad += 1
                elif(len(line) >= 6):
                    n_obj += 1

                while (i < len(line)):
                    p.append(line[i])
                    # if("//" in line[i]):
                    #     p.append(int(line[i].split("//")[0]))
                    # elif("/" in line[i]):
                    #     p.append(int(line[i].split("/")[0]))

                    i += 1

                face.append(p)

        # print(face)
        # gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed() 
        flag = 1  
        if ("/" in path[0]):
            f_name = path[0].split("/")
        elif("\\" in path[0]):
            f_name = path[0].split("\\")

        print("1. File name: " + f_name[len(f_name) - 1])
        print("2. Total number of faces: "+ str(len(face)))
        print("3. Number of faces with 3 vertices: " + str(tri))
        print("4. Number of faces with 4 vertices: " + str(quad))
        print("5. Number of faces with more than 5 vertices: " + str(n_obj))
        print("")

        f.close()

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2016025641', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)

    count = 0
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()   

    while not glfw.window_should_close(window):
        glfw.poll_events()
        ang = count % 360
        render(ang)
        count += 1
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
			
