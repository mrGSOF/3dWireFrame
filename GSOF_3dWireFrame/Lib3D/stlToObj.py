from GSOF_3dWireFrame.Lib3D import Lib3D as L
try:
    import pymeshlab as ml
except:
    print("could not find pymeshlab. DO NOT USE STL FILES!!\nTo install, run ```pip install pymeshlab```")

def stlToObj(filename, faceCount=-1, color=(0,0,0)):
    # Load the STL file
    ms = ml.MeshSet()
    ms.load_new_mesh(filename)

    # Simplify the mesh
    if faceCount > 0:
        ms.apply_filter('meshing_decimation_quadric_edge_collapse', 
                        targetfacenum=faceCount)

    # Get the simplified mesh
    simplified_mesh = ms.current_mesh()
    faceMatrix = simplified_mesh.face_matrix()
    vertexMatrix = simplified_mesh.vertex_matrix()

    # Initialize lists for points and lines
    points = []
    lines = []

    for i in range(simplified_mesh.face_number()):
        # Get the vertices of the triangle
        vertexes = faceMatrix[i]

        # Add the vertices (points) to the list
        for vertex in vertexes:
            points.append(vertexMatrix[vertex].tolist())
        
        # Add the edges (lines) to the list
        lines.append([i*3, i*3+1])
        lines.append([i*3+1, i*3+2])
        lines.append([i*3+2, i*3])

    # Now you have a list of points and lines
    return L.dataToDict(points, lines, scale=100.0, color=color)
